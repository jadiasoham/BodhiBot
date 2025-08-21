"""Policy Aware mini LLM
Gets instructor configured usage policies in natural language.
Gets as system prompt
Provides a short ruling with a 1 - 2 sentence reason.

Models available: GPT-4o-mini, Phi3.5-mini-instruct, Mistral-7b-instruct
currently using: Phi3.5-mini-instruct
"""
import warnings
from django.conf import settings
from ...model_manager import policy_llm
import re
import spacy
from ....models import UsagePolicy

# Get the latest usage policy:
def get_current_policy():
    try:
        return UsagePolicy.objects.latest("updated_on").policy
    except UsagePolicy.DoesNotExist:
        return {
            "blocked": [],
            "allowed": []
        }

# NLP model
nlp = spacy.load("en_core_web_sm")

class PolicyEnforcementLayer:
    def __init__(self, input_prompt):
        self.prompt = input_prompt
        self.model = policy_llm.model
        self.tokenizer = policy_llm.tokenizer
        self.nlp = nlp
        self.device = policy_llm.device or "cuda:0"
        self.blocked = False
        self.reason = ""
        self.system_prompt = settings.POLICY_ENFORCER_SYSTEM_PROMPT
        self.policy = get_current_policy()

    def format_prompt(self):
        """Formats the prompt to be inputted to the LLM"""
        user_prompt = self.prompt
        system_prompt = self.system_prompt
        rules = self.policy
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        rules_prompt = ""

        if rules:
            if not "allowed" in rules or not "blocked" in rules:
                raise ValueError("Rules JSON format not as expected.")
            
            # Add allow to system prompt
            rules_prompt += "\n\nThe Rules are as follows:"
            if "allowed" in rules:
                rules_prompt += "\n\nAllowed:"
                for rule in rules["allowed"]:
                    rules_prompt += f"\n{rule}"

            # Add blocked prompts to system prompt
            if "blocked" in rules:
                rules_prompt += "\n\nBlocked:"
                for rule in rules["blocked"]:
                    rules_prompt += f"\n{rule}"

        else:
            rules_prompt += "No rules are provided explicitly. Monitor if the user's prompt is acceptable from an educational point of view."

        rules_prompt += "\n\nYou must answer in the following format ONLY:\n\n"
        rules_prompt += "Allow/ Block\nReason: [Briefly explain your ruling here in one or two sentences.]"

        final = rules_prompt + "\n\nUser's prompt:\n" + user_prompt

        messages.append({"role": "user", "content": final})
        
        return messages
    
    def inference_model(self, formatted_prompt):
        """Queries the mini LLM with the formatted prompt and gets results"""
        text = self.tokenizer.apply_chat_template(
            formatted_prompt,
            tokenize= False,
            add_generation_prompt= True
        )

        inputs = self.tokenizer([text], return_tensors= "pt", truncation= True,
                        max_length= 1024, add_special_tokens= False).to(self.device)
        
        output = self.model.generate(
            **inputs,
            # attention_mask=inputs["attention_mask"],
            pad_token_id= self.tokenizer.eos_token_id,
            do_sample=True,
            top_p=0.5,
            temperature=0.1,
            max_new_tokens=128,
            use_cache= False
        )

        # Extract the new tokens (response) from the generated tokens.
        new_tokens = output[0][inputs["input_ids"].shape[1]:]

        response = self.tokenizer.decode(new_tokens, skip_special_tokens=True)

        return response
    
    @staticmethod
    def truncate_to_25_words(text, *, nlp, buffer = 0):
        words = text.split()
        if len(words) <= 25 + buffer:
            # Since this falls within limit, return the original text itself.
            return text

        if nlp is None:
            # If no NLP model is provided, adding a warning text, just in case...
            warnings.warn("No NLP model provided. Cannot guarantee prevention of sentence getting cut off.")
            parts = words[:25 + buffer]
            ellipsis = "..." if not re.search(r"[.!?]$", parts[-1]) else ""
            return " ".join(parts) + ellipsis

        # If an NLP model is provided, continue with it.
        doc = nlp(text)

        sentences = [sent.text for sent in doc.sents]

        current_word_count = 0
        result_sentences = []

        for sentence in sentences:
            sentence_words = sentence.split()
            
            if current_word_count + len(sentence_words) <= 25 + buffer:
                result_sentences.append(sentence)
                current_word_count += len(sentence_words)

            elif current_word_count + len(sentence_words) > 25 + buffer:
                break

        return " ".join(result_sentences).strip()

    def run(self):
        """Runs the policy enforcer and returns a ruling and a reason"""
        formatted_prompt = self.format_prompt()

        result = self.inference_model(formatted_prompt)

        # Now the result needs to be scrutinized as follows:
        # The 1st line of the result will contain a ruling "Allowed / Blocked"
        # The next 1 or 2 lines will contain a short reason.
        # If the reason is long, we'll truncate it to around 25 words.
        result = result.splitlines()
        ruling = result[0]
        reason = " ".join(result[1:])
        
        match = re.search(r'(allow|block)', ruling, re.IGNORECASE)
        if match:
            self.blocked = match.group(1).lower() == "block"

        
        self.reason = self.truncate_to_25_words(reason, nlp= self.nlp, buffer= 5)
        self.reason = re.sub(r'^reason:\s*', '', self.reason, flags=re.IGNORECASE)

        return self.blocked, self.reason
