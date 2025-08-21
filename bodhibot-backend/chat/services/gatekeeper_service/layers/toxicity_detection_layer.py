from ...model_manager import detox_original, detox_unbiased
import numpy as np

class ToxicityDetectionLayer:

    def __init__(self, input_prompt, *, threshold=0.7):
        self.prompt = input_prompt
        self.threshold = threshold
        self.results = []
        self.blocked = False
        self.reason = ""

    def layer_1(self):
        """Process the input text through Detoxify['original']"""
        res = detox_original.predict(self.prompt)
        self.results.append(res)

    def layer_2(self):
        """Process the input text through Detoxify['unbiased']"""
        res = detox_unbiased.predict(self.prompt)
        self.results.append(res)

    def process_results(self):
        """Combine results from both models and check threshold"""
        master_result = {}
        blocked_for = []

        # Average scores across both models
        for result in self.results:
            for param, score in result.items():
                if param in master_result:
                    master_result[param] = np.mean([master_result[param], score])
                else:
                    master_result[param] = score

        # Threshold check
        for param, mean_score in master_result.items():
            if mean_score >= self.threshold:
                blocked_for.append(param)

        if blocked_for:
            self.blocked = True
            violations = ", ".join(blocked_for) if len(blocked_for) > 1 else blocked_for[0]
            self.reason = (
                f"Blocked by toxicity filter for violating: {violations}."
            )

        return self.blocked, self.reason

    def run(self):
        """Run both layers and evaluate"""
        self.layer_1()
        self.layer_2()
        return self.process_results()
