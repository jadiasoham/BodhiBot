import json
from django.conf import settings

def deserialize_messages_for_context(data):
    """
    Deserializes the message's serializer.data for injecting into chat prompt's context
    the message serializer (i.e., each element of data) contains fields: id, sender, content, timestamp
    """
    chat_history = list()
    for message in data:
        this_item = {}
        this_item["role"] = "user" if message["sender"].lower() != "bodhibot" else "assistant"
        this_item["content"] = message["content"]
        chat_history.append(this_item)

    return chat_history

    

def format_prompt_for_qwen(user_prompt, system_prompt=None, context=None, summary=None):
    """
    Formats the prompt string for Qwen-style models using system/user role markers.
    (context is expected as a json.dumps compatible)
    (summary isn't expected and is adviced to be ignored so as not to exceed the token limit)
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    if context:
        serializable_context = deserialize_messages_for_context(context)
        for msg in serializable_context:
            messages.append(msg)
        # messages.append({"role": "user", "content": "[Context]\n" + context_str})

    if summary:
        messages.append({"role": "user", "content": "[Summary]\n" + summary})
    
    messages.append({"role": "user", "content": user_prompt})

    return messages

def generate_response(model, tokenizer, formatted_prompt, device, max_length= 512):
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
        top_p= 0.7,
        temperature= settings.TEMPERATURE,
        max_new_tokens= settings.MAX_NEW_TOKENS,
    )

    # Extract only the new tokens as the response
    new_tokens = output[0][inputs["input_ids"].shape[1]:]
    response = tokenizer.decode(new_tokens, skip_special_tokens= True)

    return response
