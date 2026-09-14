import json
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict
from utils.logger import Logger

class LearningModule:
    """Self-learning engine that improves through interactions"""
    
    # Pre-compiled stop words as frozenset for O(1) lookup
    STOP_WORDS = frozenset({
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might'
    })
    
    POSITIVE_WORDS = frozenset({
        'good', 'great', 'excellent', 'awesome', 'amazing', 'wonderful',
        'fantastic', 'perfect', 'love', 'happy', 'glad', 'thanks', 'thank',
        'best', 'brilliant', 'superb', 'outstanding', 'excellent'
    })
    
    NEGATIVE_WORDS = frozenset({
        'bad', 'terrible', 'awful', 'horrible', 'poor', 'hate', 'dislike',
        'angry', 'sad', 'disappointed', 'frustrating', 'annoying', 'worst',
        'dreadful', 'lousy', 'miserable', 'useless'
    })
    
    def __init__(self, memory_manager):
        self.memory = memory_manager
        self.logger = Logger()
        self.interaction_patterns = defaultdict(list)
        self.response_effectiveness = defaultdict(float)
        self.learning_rate = 0.1
        
        self.logger.info("Learning Module initialized with pre-compiled word sets")
    
    def learn_from_interaction(self, user_input: str, intent: str, response: str) -> None:
        """Learn from user interactions"""
        try:
            patterns = self._extract_patterns(user_input, intent)
            
            for pattern in patterns:
                self.interaction_patterns[intent].append(pattern)
            
            self._update_response_effectiveness(intent, response)
            self._optimize_knowledge(intent, response)
            
            self.logger.info(f"Learned from interaction: {intent}")
            
        except Exception as e:
            self.logger.error(f"Error learning from interaction: {str(e)}")
    
    def _extract_patterns(self, user_input: str, intent: str) -> List[Dict[str, Any]]:
        """Extract patterns from user input"""
        patterns = []
        
        keywords = self._extract_keywords(user_input)
        if keywords:
            patterns.append({
                'type': 'keywords',
                'data': keywords,
                'intent': intent
            })
        
        phrases = self._extract_phrases(user_input)
        if phrases:
            patterns.append({
                'type': 'phrases',
                'data': phrases,
                'intent': intent
            })
        
        return patterns
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords efficiently using frozenset"""
        words = text.lower().split()
        keywords = [w for w in words if w not in self.STOP_WORDS and len(w) > 3]
        return keywords[:5]
    
    def _extract_phrases(self, text: str) -> List[str]:
        """Extract phrases from text"""
        sentences = text.split('.')
        phrases = [s.strip() for s in sentences if len(s.strip()) > 10]
        return phrases[:3]
    
    def _update_response_effectiveness(self, intent: str, response: str) -> None:
        """Update response effectiveness score using exponential moving average"""
        effectiveness_score = self._calculate_effectiveness(response)
        current = self.response_effectiveness.get(intent, 0)
        self.response_effectiveness[intent] = current + (effectiveness_score - current) * self.learning_rate
    
    def _calculate_effectiveness(self, response: str) -> float:
        """Calculate effectiveness score for response"""
        score = 0.5
        
        # Length bonus
        if len(response) > 100:
            score += 0.2
        
        # Helpful indicators
        helpful_indicators = ['help', 'solution', 'answer', 'suggest', 'recommend', 'guide', 'explain']
        if any(indicator in response.lower() for indicator in helpful_indicators):
            score += 0.15
        
        # Penalize very short responses
        if len(response) < 20:
            score -= 0.2
        
        return min(1.0, max(0.0, score))
    
    def _optimize_knowledge(self, intent: str, response: str) -> None:
        """Add high-effectiveness responses to knowledge base"""
        if self.response_effectiveness[intent] > 0.7:
            self.memory.add_learned_response(intent, response)
    
    def process_feedback(self, feedback: str) -> None:
        """Process user feedback to adjust learning rate"""
        try:
            is_positive = self._is_positive_feedback(feedback)
            
            self.memory.store_feedback({
                'feedback': feedback,
                'positive': is_positive,
                'timestamp': datetime.now().isoformat()
            })
            
            # Adjust learning rate based on feedback
            if is_positive:
                self.learning_rate = min(0.5, self.learning_rate + 0.05)
            else:
                self.learning_rate = max(0.01, self.learning_rate - 0.02)
            
            self.logger.info(f"Processed feedback. New learning rate: {self.learning_rate:.3f}")
            
        except Exception as e:
            self.logger.error(f"Error processing feedback: {str(e)}")
    
    def _is_positive_feedback(self, feedback: str) -> bool:
        """Determine if feedback is positive using frozensets"""
        feedback_lower = feedback.lower()
        
        positive_count = sum(1 for word in self.POSITIVE_WORDS if word in feedback_lower)
        negative_count = sum(1 for word in self.NEGATIVE_WORDS if word in feedback_lower)
        
        return positive_count > negative_count
    
    def get_learning_metrics(self) -> Dict[str, Any]:
        """Get learning metrics"""
        return {
            'total_patterns': sum(len(v) for v in self.interaction_patterns.values()),
            'patterns_by_intent': {k: len(v) for k, v in self.interaction_patterns.items()},
            'response_effectiveness': dict(self.response_effectiveness),
            'current_learning_rate': self.learning_rate
        }
