import time
import warnings
from ...serializers import GatekeeperLogsSerializer, MessageSerializer

class GatekeeperService:
    """
    The Gatekeeper layer that manages and runs all configured filtering layers.

    Each layer must be instantiated with the user prompt ONLY and implement a 
    `run` method that takes no arguments and returns a tuple:
        (blocked: bool, reason: str).

    The Gatekeeper itself is instantiated with:
        - `message`: a message object (required).
        - layers as keyword arguments in the form `layer_name=layer_obj`.

    Each `layer_obj` must be a callable accepting exactly one argument: `user_prompt: str`.

    **Note:**
        - Layers are executed sequentially in the order they are passed to the Gatekeeper.
        - This ordering is important for the fail-fast mechanism, allowing lighter or cheaper compute layers to be run first, potentially short-circuiting more expensive layers.
    """

    def __init__(self, message, **layers):
        self.message = message
        self.layers = dict(layers)
        self.blocked = False
        self.blocked_at = None  # Name of the layer that blocked the message
        self.reason = ""

    def get_message_content(self):
        serializer = MessageSerializer(self.message)
        return serializer.data.get('content', '')

    def run(self):
        start = time.time()
        msg = self.get_message_content()

        if not self.layers:
            warnings.warn(
                "No layers are passed to the Gatekeeper. This will always allow any input message without any checks."
            )

        for layer_name, layer in self.layers.items():
            s = time.time()
            try:
                curr_layer = layer(msg)
                blocked, reason = curr_layer.run()
            except Exception as e:
                print(f"Layer '{layer_name}' failed: {e}")
                # Continue to next layer even if one fails
                continue

            if blocked:
                self.blocked = blocked
                self.reason = reason
                self.blocked_at = layer_name
                break
            e = time.time()
            print(f"{layer_name} took {e - s:.3f} seconds to run.")

        end = time.time()
        print(f"Gatekeeper processed user input in {end - start:.3f} seconds.")

        data = {
            "message": self.message.id,
            "blocked_at": self.blocked_at,
            "reason": self.reason,
        }

        serializer = GatekeeperLogsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(f"GatekeeperLogsSerializer validation errors: {serializer.errors}")

        return self.blocked, self.reason
