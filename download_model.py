import os
import sys
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import argparse

def download_model(model_name: str, save_path: str, adapter_id: str = ""):
    """
    Downloads the specified model and its tokenizer to the given path.
    It handles creating the directory if it doesn't exist.

    Args:
        model_name (str): The name of the model to download from Hugging Face
                          (e.g., "Qwen/Qwen2.5-Coder-7b-Instruct").
        save_path (str): The local directory path where the model and tokenizer
                         will be saved.
        adapter_id (str): If provided, this adapter will be downloaded as well
    """
    save_path = os.path.join(save_path, model_name)

    if not os.path.exists(save_path):
        try:
            os.makedirs(save_path, exist_ok=True)
            print(f"Created directory: {save_path}")
        except OSError as e:
            print(f"Error creating directory {save_path}: {e}")
            sys.exit(1)

    print(f"Attempting to download model: {model_name}...")
    print(f"Target download path: {save_path}")

    try:
        # --- Download Tokenizer ---
        print("\n--- Downloading Tokenizer ---")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer_path = os.path.abspath(save_path)
        tokenizer.save_pretrained(tokenizer_path)
        print(f"Tokenizer downloaded and saved to: {tokenizer_path}")

        # --- Download Model ---
        print("\n--- Downloading Model ---")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
        )
        model_dir_path = os.path.abspath(save_path)
        model.save_pretrained(model_dir_path)
        print(f"Model downloaded and saved to: {model_dir_path}")

        # --- Adapter Handling (Optional) ---
        if adapter_id:
            try:
                print(f"\n--- Attempting to load separate adapter: {adapter_id} ---")
                # Load the adapter weights
                adapter_model = PeftModel.from_pretrained(model, adapter_id)
                adapter_path = os.path.join(save_path, "adapter")
                adapter_model.save_pretrained(adapter_path)
                print(f"Adapter downloaded and saved to: {adapter_path}")            
            except Exception as e:
                print(f"Could not load separate adapter from {adapter_id}. It might not exist or an error occurred: {e}")
        # -----------------------------------

        print(f"\nSuccessfully downloaded '{model_name}' to '{save_path}'")
        print("You can now load the model and tokenizer from these local paths.")

    except Exception as e:
        print(f"\nAn error occurred during the download process: {e}")
        print("Please check the following:")
        print(f"1. Is the model name '{model_name}' correct on Hugging Face?")
        print("2. Do you have an active internet connection?")
        print("3. Have you installed the necessary libraries? (e.g., `pip install transformers accelerate peft`)")
        print("4. Models can be very large, make sure you have sufficient space on your disk. (Typically > 15 GB)")
        sys.exit(1) # Exit with an error code

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Downloads the given model from Hugging Face with its tokenizer and optionally adapters.")
    parser.add_argument(
        '--model-name', 
        type=str, 
        help="The namespace and name of the model (e.g., Qwen/Qwen2.5-Coder-7b-Instruct)"
    )
    parser.add_argument(
        '--savepath', 
        type=str, 
        help="The directory where the model will be saved"
    )
    parser.add_argument(
        '--adapter-id', 
        type=str, 
        default="", 
        help="(Optional) The adapter ID from Hugging Face, if applicable"
    )
    parser.add_argument(
        '--skip-if-exists', 
        action='store_true',
        help="Skips download if model/tokenizer already exist in savepath"
    )

    args = parser.parse_args()

    # Interactive fallback for missing args
    model_id = args.model_name or input("Enter model name (e.g., Qwen/Qwen2.5-Coder-7b-Instruct):\n> ").strip()
    download_path = args.savepath or input("Enter the local directory to save the model:\n> ").strip()
    
    # Adapter is optional; prompt only if completely missing
    if args.adapter_id == "":
        adapter = input("Enter adapter ID [optional]:\n> ").strip()
    else:
        adapter = args.adapter_id

    skip_existing = args.skip_if_exists
    full_path = os.path.join(download_path, model_id)

    # Check for existing model/tokenizer/adapter
    if skip_existing and os.path.exists(full_path):
        files = os.listdir(full_path)
        has_model = any(f.endswith(".bin") or f.endswith(".safetensors") for f in files)
        has_tokenizer = os.path.exists(os.path.join(full_path, "tokenizer_config.json"))

        adapter_ok = True
        if adapter:
            adapter_ok = os.path.exists(os.path.join(full_path, "adapter"))

        if has_model and has_tokenizer and adapter_ok:
            print(f"\nModel, tokenizer{' and adapter' if adapter else ''} already exist at '{full_path}'. Skipping download.")
            sys.exit(0)

    # Proceed with download
    download_model(model_id, download_path, adapter)