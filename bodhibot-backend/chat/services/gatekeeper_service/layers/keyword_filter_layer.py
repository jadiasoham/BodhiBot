import re
from rapidfuzz import fuzz
from ...utils.blocked_keywords import BLOCKED_PHRASES, BLOCKED_WORDS

class KeywordBasedFilteringLayer:
    def __init__(self, input_prompt, *, fuzzy_threshold = 60):
        self.prompt = input_prompt
        self.fuzzy_threshold = fuzzy_threshold
        self.blocked = False # Assumed false initially
        self.fuzzy_ratio = 0.0
        self.reason = ""
    

    def regex_filter(self):
        text = self.prompt
        for word in BLOCKED_WORDS:
            pattern = re.compile(rf"\b{re.escape(word)}\b", re.IGNORECASE)
            if re.search(pattern, text):
                self.reason = f"Blocked by regex filter as the query contains a blocked word: '{word}'"
                self.blocked = True
                return
        
        for phrase in BLOCKED_PHRASES:
            if re.search(re.escape(phrase), text, re.IGNORECASE):
                self.reason = f"Blocked by regex filter as the query contains a blocked phrase: '{phrase}'"
                self.blocked = True
                return
            
        # Incase passes both the loops:
        return True
    
    def fuzzy_check(self):
        text = self.prompt

        if self.blocked:
            return

        
        max_ratio = 0

        for phrase in BLOCKED_PHRASES:
            score = fuzz.WRatio(phrase, text)
            max_ratio = max(max_ratio, score)
            if score >= self.fuzzy_threshold:
                self.blocked = True
                self.reason = (
                    f"Blocked by fuzzy check: '{phrase}' matched with score {score} (Threshold set to {self.fuzzy_threshold})."
                )
                return False
        
        # If passes the test
        return True
    
    def run(self):
        if not self.regex_filter():
            return self.blocked, self.reason

        self.fuzzy_check()
        return self.blocked, self.reason
