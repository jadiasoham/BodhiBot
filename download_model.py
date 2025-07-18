import os
import sys
from transformers import AutoModelForCausalLM, AutoTokenizer
# from peft import PeftModel, PeftConfig

def download_qwen_model(model_name: str, save_path: str):
    """
    Downloads the specified Qwen model and its tokenizer to the given path.
    It handles creating the directory if it doesn't exist.

    Args:
        model_name (str): The name of the model to download from Hugging Face
                          (e.g., "Qwen/Qwen2.5-Coder-7b-Instruct").
        save_path (str): The local directory path where the model and tokenizer
                         will be saved.
    """
    if not os.path.exists(save_path):
        try:
            os.makedirs(save_path, exist_ok=True)
            print(f"Created directory: {save_path}")
        except OSError as e:
            print(f"Error creating directory {save_path}: {e}")
            sys.exit(1) # Exit if directory cannot be created

    print(f"Attempting to download model: {model_name}...")
    print(f"Target download path: {save_path}")

    try:
        # --- Download Tokenizer ---
        print("\n--- Downloading Tokenizer ---")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer_path = os.path.join(save_path, "tokenizer")
        tokenizer.save_pretrained(tokenizer_path)
        print(f"Tokenizer downloaded and saved to: {tokenizer_path}")

        # --- Download Model ---
        print("\n--- Downloading Model ---")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
        )
        model_dir_path = os.path.join(save_path, "model")
        model.save_pretrained(model_dir_path)
        print(f"Model downloaded and saved to: {model_dir_path}")

        # --- Adapter Handling (Optional) ---
        # If you have a separate PEFT (Parameter-Efficient Fine-Tuning) adapter
        # (e.g., LoRA weights) that needs to be loaded on top of this base model,
        # you would typically do it here.
        # Example:
        # adapter_id = "your/specific-adapter-repo-id" # Replace with the actual Hugging Face ID or local path of your adapter
        # try:
        #     print(f"\n--- Attempting to load separate adapter: {adapter_id} ---")
        #     # Load the adapter weights
        #     adapter_model = PeftModel.from_pretrained(model, adapter_id)
        #     adapter_path = os.path.join(save_path, "adapter")
        #     adapter_model.save_pretrained(adapter_path)
        #     print(f"Adapter downloaded and saved to: {adapter_path}")
        #
        #     # If you want to merge the adapter weights directly into the base model
        #     # (making it a single, larger model), you can call:
        #     # model = adapter_model.merge_and_unload()
        #     # print("Adapter merged into the base model.")
        #
        # except Exception as e:
        #     print(f"Could not load separate adapter from {adapter_id}. It might not exist or an error occurred: {e}")
        #     print("If you don't have a separate adapter, you can ignore this message.")
        # -----------------------------------

        print(f"\nSuccessfully downloaded '{model_name}' to '{save_path}'")
        print("You can now load the model and tokenizer from these local paths.")

    except Exception as e:
        print(f"\nAn error occurred during the download process: {e}")
        print("Please check the following:")
        print(f"1. Is the model name '{model_name}' correct on Hugging Face?")
        print("2. Do you have an active internet connection?")
        print("3. Have you installed the necessary libraries? (e.g., `pip install transformers accelerate peft`)")
        sys.exit(1) # Exit with an error code

if __name__ == "__main__":
    # Define the model ID you want to download
    MODEL_ID = "Qwen/Qwen2.5-Coder-7b-Instruct"

    DOWNLOAD_PATH = os.path.join("/home/soham/Downloads/Qwen", "Qwen2.5-Coder-7b-Instruct")

    print("--- Starting Qwen Model Download Script ---")
    download_qwen_model(MODEL_ID, DOWNLOAD_PATH)
    print("\n--- Download script finished ---")