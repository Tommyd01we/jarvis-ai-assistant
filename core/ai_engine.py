import json
import os
from datetime import datetime
from typing import Dict, List, Any
import uuid
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
        
        # Bounded conversation context
        self.conversation_context = []
        self.max_context_size = Config.MAX_CONTEXT_SIZE
        self.interaction_count = 0
        
        self.logger.info(f"Jarvis AI Engine initialized with max context size: {self.max_context_size}")
    
    def process(self, user_input: str) -> str:
        """Main processing pipeline for user input"""
        try:
            interaction_id = self._generate_id()
            intent, entities, sentiment = self.nlp.analyze(user_input)
            
            # Add to bounded context
            self._add_to_context({
                'role': 'user',
                'content': user_input,
                'intent': intent,
                'entities': entities,
                'sentiment': sentiment
            })
            
            relevant_knowledge = self.memory.retrieve_relevant(intent, entities)
            response = self._generate_response(user_input, intent, entities, relevant_knowledge)
            
            # Store interaction
            self.memory.store_interaction({
                'id': interaction_id,
                'timestamp': datetime.now().isoformat(),
                'user_input': user_input,
                'intent': intent,
                'entities': entities,
                'response': response,
                'sentiment': sentiment
            })
            
            # Learn from interaction
            self.learner.learn_from_interaction(user_input, intent, response)
            
            # Add response to bounded context
            self._add_to_context({
                'role': 'assistant',
                'content': response
            })
            
            self.interaction_count += 1
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing input: {str(e)}")
            return "I encountered an error processing your request. Please try again."
    
    def _add_to_context(self, entry: Dict[str, Any]) -> None:
        """Add entry to context with size enforcement"""
        self.conversation_context.append(entry)
        
        # Enforce maximum context size
        if len(self.conversation_context) > self.max_context_size:
            self.conversation_context = self.conversation_context[-self.max_context_size:]
    
    def _generate_response(self, user_input: str, intent: str, entities: List[str], knowledge: Dict) -> str:
        """Generate response based on intent and knowledge"""
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
        """Handle greeting intent"""
        greetings = [
            "Hello! I'm Jarvis, your AI assistant. How can I help you today?",
            "Hi there! I'm here to assist. What would you like to know?",
            "Greetings! Ready to help with whatever you need.",
            "Welcome! How can I be of service?"
        ]
        return greetings[self.interaction_count % len(greetings)]
    
    def _handle_query(self, user_input: str, entities: List[str], knowledge: Dict) -> str:
        """Handle query intent"""
        if knowledge and 'answer' in knowledge:
            return f"Based on my knowledge: {knowledge['answer']}"
        return self._generate_contextual_response(user_input, entities)
    
    def _handle_feedback(self, user_input: str, entities: List[str], knowledge: Dict) -> str:
        """Handle feedback intent"""
        self.learner.process_feedback(user_input)
        return "Thank you for your feedback! I've learned from this interaction and will improve."
    
    def _handle_learning_request(self, user_input: str, entities: List[str], knowledge: Dict) -> str:
        """Handle learning request"""
        info = self._extract_learning_info(user_input)
        self.memory.add_to_knowledge_base(info)
        return f"I've learned: {info}. This will help me provide better responses in the future."
    
    def _handle_system_query(self, user_input: str, entities: List[str], knowledge: Dict) -> str:
        """Handle system query"""
        if 'stats' in user_input.lower():
            metrics = self.memory.get_metrics()
            return json.dumps(metrics, indent=2)
        elif 'learned' in user_input.lower():
            patterns = self.memory.get_learned_patterns()
            return json.dumps(patterns, indent=2)
        return "System query processed."
    
    def _handle_unknown(self, user_input: str, entities: List[str], knowledge: Dict) -> str:
        """Handle unknown intent"""
        return self._generate_contextual_response(user_input, entities)
    
    def _generate_contextual_response(self, user_input: str, entities: List[str]) -> str:
        """Generate response based on context"""
        if entities:
            return f"I understand you're asking about {', '.join(entities[:3])}. Let me help with that."
        return "I'm processing your query. Could you provide more details to help me assist better?"
    
    def _extract_learning_info(self, user_input: str) -> Dict[str, Any]:
        """Extract learning information from input"""
        return {
            'content': user_input,
            'timestamp': datetime.now().isoformat(),
            'learned_at': self.interaction_count
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics (returns dict, not JSON string)"""
        return self.memory.get_metrics()
    
    def get_learned_patterns(self) -> Dict[str, Any]:
        """Get learned patterns (returns dict, not JSON string)"""
        return self.memory.get_learned_patterns()
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_context.copy()
    
    def clear_context(self):
        """Clear conversation context"""
        self.conversation_context = []
        self.logger.info("Conversation context cleared")
    
    def get_status(self) -> Dict[str, Any]:
        """Get system status"""
        return {
            'interactions': self.interaction_count,
            'context_size': len(self.conversation_context),
            'max_context_size': self.max_context_size,
            'learned_patterns': len(self.memory.get_learned_patterns()),
            'system_ready': True,
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_id(self) -> str:
        """Generate unique interaction ID"""
        return str(uuid.uuid4())[:8]
    
    def shutdown(self):
        """Shutdown Jarvis gracefully"""
        self.memory.save_all()
        self.logger.info("Jarvis AI Engine shut down")
