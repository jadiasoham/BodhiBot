import multiprocessing as mp
mp.set_start_method('spawn', force=True) # This avoids issues with cuda initializations

import time
import os, sys
from celery import shared_task
from .model_manager import ModelManager
from .services.utils.utility import generate_response, format_prompt_for_qwen
from django.conf import settings

@shared_task
def generate_response_task(user_prompt, context= None, summary= None):
    """Celery task to generate a response using the ModelManager."""

    try:
        # print("loading model")
        ModelManager.initialize() # <- This will initialize the model only if it isn't yet initialized.

        tokenizer = ModelManager.get_tokenizer()
        model = ModelManager.get_model()
        device = ModelManager.get_device()
        # print("model loaded.")
        # print(str(model))

        if not model or not tokenizer:
            raise ValueError("Model or tokenizer not initialized. Exiting task.")
        
        system_prompt = settings.SYSTEM_PROMPT
        formatted_prompt = format_prompt_for_qwen(
            user_prompt, 
            system_prompt= system_prompt,
            context= context,
            summary= summary
        )

        start_time = time.time()
        response = generate_response(
            model= model,
            tokenizer= tokenizer,
            formatted_prompt= formatted_prompt,
            device= device,
        )
        end_time = time.time()
        print(f"Response generated in {end_time - start_time:.2f} seconds")
    except Exception as e:
        print(f"Error in generate_response_task: {e}")
        response = "I am unable to generate a response at the moment. Please try again later."
    finally:
        return response


