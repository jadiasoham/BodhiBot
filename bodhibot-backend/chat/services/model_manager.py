import torch
import gc
import os
import time
from transformers import AutoModelForCausalLM, AutoTokenizer
from django.conf import settings
from detoxify import Detoxify

class ModelManager:
    def __init__(self, model_path, *, get_tokenizer = True, device = None):
        self.model_path = model_path
        self.get_tokenizer = get_tokenizer
        self.device = device
        
        # <-- These will be non-None once model is successfully loaded. -->
        self.model = None
        self.tokenizer = None
        self.initialized = False
        self.model_name = None

        # <-- Run once per instance -->
        # self.initialize()

    def load_model(self):
        try:
            torch.cuda.empty_cache()
            gc.collect()
            start_time = time.time()

            tokenizer = None
            model = None

            if self.get_tokenizer:
                tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code= True)
                # tokenizer.pad_token = tokenizer.eos_token
                # tokenizer.padding_side = "right"

            if self.device:
                model = AutoModelForCausalLM.from_pretrained(
                    self.model_path,
                    dtype= torch.bfloat16,
                    # trust_remote_code = True
                ).to(self.device).eval()
            else:
                model = AutoModelForCausalLM.from_pretrained(
                    self.model_path, 
                    dtype= torch.bfloat16, 
                    device_map= "auto", 
                    # trust_remote_code= True
                ).eval()
            
            self.model = model
            self.tokenizer = tokenizer
            self.initialized = True
            self.model_name = os.path.basename(self.model_path)
            
            end_time = time.time()
            print(f"Model loaded in {end_time - start_time:.2f} seconds")

        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")
        

    def initialize(self):
        if not self.initialized:
            try:
                self.load_model()
            except RuntimeError as e:
                print(f"Error during model initialization: {e}")
                raise e
            except Exception as e:
                print(f"Unexpected error during model initialization: {e}")
                raise e


# Create Singleton-like instances of required models:
# 1. The main LLM:
inference_model = ModelManager("openai/gpt-oss-20b")

# 2. The Detoxify Models (just for the sake of having all models here...)
detox_original = Detoxify("original", device= "cpu")
detox_unbiased = Detoxify("unbiased", device= "cpu")

# 3. The Policy Enforcer mini LLM:
# policy_llm = ModelManager(settings.POLICY_ENFORMCEMENT_MODEL_PATH)
