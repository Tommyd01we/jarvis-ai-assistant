import re
from typing import Tuple, List, Dict
from utils.logger import Logger

class NLPProcessor:
    """Natural Language Processing for intent recognition and entity extraction"""
    
    def __init__(self):
        self.logger = Logger()
        self.intent_patterns = self._initialize_patterns()
        self.entity_patterns = self._initialize_entities()
        
        self.logger.info("NLP Processor initialized")
    
    def analyze(self, text: str) -> Tuple[str, List[str], str]:
        intent = self._classify_intent(text)
        entities = self._extract_entities(text)
        sentiment = self._analyze_sentiment(text)
        
        return intent, entities, sentiment
    
    def _initialize_patterns(self) -> Dict[str, List[str]]:
        return {
            'greeting': [
                r'^\b(hello|hi|hey|greetings|good\s+morning|good\s+afternoon|good\s+evening)\b',
                r'\bhow\s+are\s+you\b',
                r"\bwhat's\s+up\b"
            ],
            'query': [
                r'^\b(what|why|how|when|where|who)\b',
                r'can\s+you\s+tell\s+me',
                r'i\s+need\s+to\s+know',
                r'what\s+is'
            ],
            'feedback': [
                r'\bthanks?\b',
                r'\bgood\b|\bgreat\b|\bawesome\b',
                r'\bbad\b|\bpoor\b|\bdisappointing\b',
            ],
            'learning_request': [
                r'remember\s+that',
                r'learn\s+that',
                r'note\s+that',
                r'important:'
            ],
            'system_query': [
                r'stats?\b',
                r'metrics?\b',
                r'performance\b',
                r'what\s+have\s+you\s+learned'
            ]
        }
    
    def _initialize_entities(self) -> Dict[str, List[str]]:
        return {
            'person': [r'\b([A-Z][a-z]+)\b'],
            'number': [r'\b(\d+)\b'],
            'email': [r'\b([\w\.-]+@[\w\.-]+\.\w+)\b'],
            'url': [r'https?://[^\s]+']
        }
    
    def _classify_intent(self, text: str) -> str:
        text_lower = text.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    return intent
        
        return 'unknown'
    
    def _extract_entities(self, text: str) -> List[str]:
        entities = []
        
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text)
                entities.extend(matches)
        
        words = text.split()
        for word in words:
            if word and word[0].isupper() and len(word) > 2:
                entities.append(word.strip('.,!?'))
        
        return list(set(entities))[:10]
    
    def _analyze_sentiment(self, text: str) -> str:
        positive_words = {
            'good', 'great', 'excellent', 'awesome', 'amazing', 'wonderful',
            'fantastic', 'perfect', 'love', 'happy', 'glad', 'thanks', 'thank'
        }
        
        negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'poor', 'hate', 'dislike',
            'angry', 'sad', 'disappointed', 'frustrating', 'annoying'
        }
        
        text_lower = text.lower()
        words = text_lower.split()
        
        positive_count = sum(1 for word in words if word.strip('.,!?') in positive_words)
        negative_count = sum(1 for word in words if word.strip('.,!?') in negative_words)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
