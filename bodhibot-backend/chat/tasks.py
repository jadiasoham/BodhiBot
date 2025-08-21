import multiprocessing as mp
mp.set_start_method('spawn', force=True) # This avoids issues with cuda initializations

import time
from celery import shared_task
from .services.model_manager import inference_model
from .services.gatekeeper_service.layers.keyword_filter_layer import KeywordBasedFilteringLayer
from .services.gatekeeper_service.layers.toxicity_detection_layer import ToxicityDetectionLayer
from .services.gatekeeper_service.layers.policy_enforcement_layer import PolicyEnforcementLayer
from .services.gatekeeper_service.gatekeeper_service import GatekeeperService
from .services.utils.utility import generate_response, format_prompt_for_qwen
from .services.chat_service import create_message
from .models import Message
from django.conf import settings

@shared_task
def generate_response_task(chat_id, sender, user_prompt, context= None, summary= None):
    """Does the following:
    1. Creates a message object with the given user_prompt
    2. Sends it to the gatekeeper
    3. Proceeds according to the gatekeeper's outcome
    """
    response = None

    try:
        tokenizer = inference_model.tokenizer
        model = inference_model.model

        if not model or not tokenizer:
            raise ValueError("Model or tokenizer not initialized. Exiting task.")
        
        # Create the message object:
        msg = create_message(chat_id= chat_id, sender= sender, content= user_prompt)
        
        # Now retrieve the message using serializer obj's id
        # msg_obj = Message.objects.get(id= msg.id)

        # Send this to gatekeeper now:
        # breakpoint()
        gk = GatekeeperService(
            msg, 
            kw_filter= KeywordBasedFilteringLayer,
            toxicity_detector = ToxicityDetectionLayer,
            policy_enforcer = PolicyEnforcementLayer
        )

        blocked, reason = gk.run()

        if not blocked:
            system_prompt = settings.INFERENCE_SYSTEM_PROMPT
            formatted_prompt = format_prompt_for_qwen(
                user_prompt, 
                system_prompt= system_prompt,
                context= context,
                summary= summary
            )
            print("+++++++++++++++++++++++++++")
            print(formatted_prompt)
            print("+++++++++++++++++++++++++++")

            start_time = time.time()
            response = generate_response(
                model= model,
                tokenizer= tokenizer,
                formatted_prompt= formatted_prompt,
                # device= device,
            )
            end_time = time.time()
            res_list = response.strip().lower().split()
            if len(res_list) < 2 and len(response.strip()) < 3 and 'no' not in res_list:
                print("Actual response: ", response, "\nModifying...")
                response = "I don't understand. Can you clarify?"
            print(f"Response generated in {end_time - start_time:.2f} seconds")
        
        else:
            response = f"Sorry, your prompt was found to be violating our usage policy and blocked with the reason:\n{reason}"
    
    except Exception as e:
        print(f"Error in generate_response_task: {e}")
        response = "I am unable to generate a response at the moment. Please try again later."
    
    finally:
        return response


