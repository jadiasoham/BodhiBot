def format_prompt_for_qwen(user_prompt, system_prompt=None, context=None, summary=None):
    """
    Formats the prompt string for Qwen-style models using system/user role markers.
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    if context:
        messages.append({"role": "user", "content": "[Context]\n" + context})

    if summary:
        messages.append({"role": "user", "content": "[Summary]\n" + summary})
    
    messages.append({"role": "user", "content": user_prompt})

    return messages

def generate_response(model, tokenizer, formatted_prompt, device, max_length= 512, temperature= 0.7):
    """Generates a response from model using the provided formatted prompt."""

    text = tokenizer.apply_chat_template(
        formatted_prompt,
        tokenize= False,
        add_generation_prompt= True
    )

    inputs = tokenizer([text], return_tensors= "pt", truncation= True, max_length= max_length, add_special_tokens= False).to(device)

    output = model.generate(
        **inputs,
        pad_token_id= tokenizer.eos_token_id,
        do_sample= True,
        top_p= 0.6,
        temperature= temperature,
        max_new_tokens= 2048,
    )

    # Extract only the new tokens as the response
    new_tokens = output[0][inputs["input_ids"].shape[1]:]
    response = tokenizer.decode(new_tokens, skip_special_tokens= True)

    return response
