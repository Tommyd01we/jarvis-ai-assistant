import json
import os
from datetime import datetime
from typing import Dict, List, Any, Tuple
import re
from .nlp_processor import NLPProcessor
from .learning_module import LearningModule
from .memory_manager import MemoryManager
from utils.logger import Logger
from utils.config import Config

class Jarvis:
    """Main AI Engine - Core reasoning and interaction system"""
    
    def __init__(self):
        self.config = Config()
        self.logger = Logger()
        self.nlp = NLPProcessor()
        self.memory = MemoryManager()
        self.learner = LearningModule(self.memory)
        self.conversation_context = []
        self.interaction_count = 0
        
        self.logger.info("Jarvis AI Engine initialized")
    
    def process(self, user_input: str) -> str:
        """Main processing pipeline for user input"""
        try:
            interaction_id = self._generate_id()
            intent, entities, sentiment = self.nlp.analyze(user_input)
            
            self.conversation_context.append({
                'role': 'user',
                'content': user_input,
                'intent': intent,
                'entities': entities,
                'sentiment': sentiment
            })
            
            relevant_knowledge = self.memory.retrieve_relevant(intent, entities)
            response = self._generate_response(user_input, intent, entities, relevant_knowledge)
            
            self.memory.store_interaction({
                'id': interaction_id,
                'timestamp': datetime.now().isoformat(),
                'user_input': user_input,
                'intent': intent,
                'entities': entities,
                'response': response,
                'sentiment': sentiment
            })
            
            self.learner.learn_from_interaction(user_input, intent, response)
            
            self.conversation_context.append({
                'role': 'assistant',
                'content': response
            })
            
            self.interaction_count += 1
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing input: {str(e)}")
            return "I encountered an error processing your request. Please try again."
    
    def _generate_response(self, user_input: str, intent: str, entities: List[str], knowledge: Dict) -> str:
        learned_response = self.memory.get_learned_response(intent)
        if learned_response:
            return learned_response
        
        response_templates = {
            'greeting': self._handle_greeting,
            'query': self._handle_query,
            'feedback': self._handle_feedback,
            'learning_request': self._handle_learning_request,
            'system_query': self._handle_system_query,
            'unknown': self._handle_unknown
        }
        
        handler = response_templates.get(intent, self._handle_unknown)
        return handler(user_input, entities, knowledge)
    
    def _handle_greeting(self, user_input: str, entities: List[str], knowledge: Dict) -> str:
        greetings = [
            "Hello! I'm Jarvis, your AI assistant. How can I help you today?",
            "Hi there! I'm here to assist. What would you like to know?",
            "Greetings! Ready to help with whatever you need."
        ]
        return greetings[self.interaction_count % len(greetings)]
    
    def _handle_query(self, user_input: str, entities: List[str], knowledge: Dict) -> str:
        if knowledge and 'answer' in knowledge:
            return f"Based on my knowledge: {knowledge['answer']}"
        return self._generate_contextual_response(user_input, entities)
    
    def _handle_feedback(self, user_input: str, entities: List[str], knowledge: Dict) -> str:
        self.learner.process_feedback(user_input)
        return "Thank you for your feedback! I've learned from this interaction and will improve."
    
    def _handle_learning_request(self, user_input: str, entities: List[str], knowledge: Dict) -> str:
        info = self._extract_learning_info(user_input)
        self.memory.add_to_knowledge_base(info)
        return f"I've learned: {info}. This will help me provide better responses in the future."
    
    def _handle_system_query(self, user_input: str, entities: List[str], knowledge: Dict) -> str:
        if 'stats' in user_input.lower():
            return self.get_performance_metrics()
        elif 'learned' in user_input.lower():
            return self.get_learned_patterns()
        return "System query processed."
    
    def _handle_unknown(self, user_input: str, entities: List[str], knowledge: Dict) -> str:
        return self._generate_contextual_response(user_input, entities)
    
    def _generate_contextual_response(self, user_input: str, entities: List[str]) -> str:
        if entities:
            return f"I understand you're asking about {', '.join(entities[:3])}. Let me help with that."
        return "I'm processing your query. Could you provide more details to help me assist better?"
    
    def _extract_learning_info(self, user_input: str) -> Dict[str, Any]:
        return {
            'content': user_input,
            'timestamp': datetime.now().isoformat(),
            'learned_at': self.interaction_count
        }
    
    def get_performance_metrics(self) -> str:
        metrics = self.memory.get_metrics()
        return json.dumps(metrics, indent=2)
    
    def get_learned_patterns(self) -> str:
        patterns = self.memory.get_learned_patterns()
        return json.dumps(patterns, indent=2)
    
    def get_conversation_history(self) -> List[Dict]:
        return self.conversation_context.copy()
    
    def clear_context(self):
        self.conversation_context = []
        self.logger.info("Conversation context cleared")
    
    def get_status(self) -> Dict[str, Any]:
        return {
            'interactions': self.interaction_count,
            'context_size': len(self.conversation_context),
            'learned_patterns': len(self.memory.get_learned_patterns()),
            'system_ready': True,
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_id(self) -> str:
        import uuid
        return str(uuid.uuid4())[:8]
    
    def shutdown(self):
        self.memory.save_all()
        self.logger.info("Jarvis AI Engine shut down")
