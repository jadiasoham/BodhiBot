import torch
import gc
import os, sys
import time
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from django.conf import settings

class ModelManager:
    _model = None
    _tokenizer = None
    _device = None
    _initialized = False
    _model_name = None

    @classmethod
    def load_model(cls, model_path, adapter_path, device= "cuda:0"):
        try:
            torch.cuda.empty_cache()
            gc.collect()
            start_time = time.time()

            tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code= True)
            tokenizer.pad_token = tokenizer.eos_token
            tokenizer.padding_side = "right"

            model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype= torch.bfloat16, device_map= device, trust_remote_code= True).eval()
            if os.path.exists(adapter_path):
                if os.listdir(adapter_path): # Dir not empty
                    model = PeftModel.from_pretrained(model, adapter_path)
                else:
                    print(f"Adapter path {adapter_path} is empty, not loading adapter.")
            
            cls._model = model
            cls._tokenizer = tokenizer
            cls._device = device
            cls._initialized = True
            cls._model_name = os.path.basename(model_path)
            
            end_time = time.time()
            print(f"Model loaded in {end_time - start_time:.2f} seconds")

        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")
        

    @classmethod
    def initialize(cls):
        if not cls._initialized:
            try:
                cls.load_model(
                    settings.MODEL_PATH,
                    settings.ADAPTER_PATH,
                )
            except RuntimeError as e:
                print(f"Error during model initialization: {e}")
                sys.exit(1)
            except Exception as e:
                print(f"Unexpected error during model initialization: {e}")
                sys.exit(1)

    @classmethod
    def get_model(cls):
        return cls._model
    
    @classmethod
    def get_tokenizer(cls):
        return cls._tokenizer
    
    @classmethod
    def get_device(cls):
        return cls._device
    
    @classmethod
    def reload_model(cls, new_model_path= None, new_adapter_path= None):
        if not new_model_path and not new_adapter_path:
            print("No new model or adapter path provided, cannot reload...")
            return
        
        cls.load_model(
            new_model_path,
            new_adapter_path,
        )
