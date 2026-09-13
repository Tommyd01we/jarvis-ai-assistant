import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict
from utils.logger import Logger
from utils.config import Config

class MemoryManager:
    """Manages knowledge base, interaction history, and learned patterns"""
    
    def __init__(self):
        self.config = Config()
        self.logger = Logger()
        
        self.knowledge_base = self._load_or_create('data/knowledge_base.json', {})
        self.interaction_history = self._load_or_create('data/user_history.json', [])
        self.performance_metrics = self._load_or_create('data/performance_metrics.json', {})
        self.learned_responses = defaultdict(list)
        self.feedback_log = []
        
        self._ensure_directories()
        self.logger.info("Memory Manager initialized")
    
    def _ensure_directories(self) -> None:
        directories = ['data', 'models', 'logs']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def _load_or_create(self, filepath: str, default: Any) -> Any:
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading {filepath}: {str(e)}")
        
        return default
    
    def store_interaction(self, interaction: Dict[str, Any]) -> None:
        try:
            self.interaction_history.append(interaction)
            
            if len(self.interaction_history) > 1000:
                self.interaction_history = self.interaction_history[-1000:]
            
        except Exception as e:
            self.logger.error(f"Error storing interaction: {str(e)}")
    
    def retrieve_relevant(self, intent: str, entities: List[str]) -> Dict[str, Any]:
        try:
            relevant = {}
            
            if intent in self.knowledge_base:
                relevant = self.knowledge_base[intent].copy()
            
            for entity in entities:
                if entity in self.knowledge_base:
                    relevant.update(self.knowledge_base[entity])
            
            return relevant
            
        except Exception as e:
            self.logger.error(f"Error retrieving knowledge: {str(e)}")
            return {}
    
    def add_to_knowledge_base(self, info: Dict[str, Any]) -> None:
        try:
            key = info.get('topic', 'general')
            
            if key not in self.knowledge_base:
                self.knowledge_base[key] = {}
            
            self.knowledge_base[key].update(info)
            
        except Exception as e:
            self.logger.error(f"Error adding to knowledge base: {str(e)}")
    
    def add_learned_response(self, intent: str, response: str) -> None:
        try:
            if response not in self.learned_responses[intent]:
                self.learned_responses[intent].append(response)
            
        except Exception as e:
            self.logger.error(f"Error adding learned response: {str(e)}")
    
    def get_learned_response(self, intent: str) -> Optional[str]:
        try:
            responses = self.learned_responses.get(intent, [])
            if responses:
                return responses[-1]
        except Exception as e:
            self.logger.error(f"Error retrieving learned response: {str(e)}")
        
        return None
    
    def get_learned_patterns(self) -> Dict[str, Any]:
        return {
            'total_interactions': len(self.interaction_history),
            'knowledge_topics': list(self.knowledge_base.keys()),
            'learned_responses_count': len(self.learned_responses),
            'feedback_entries': len(self.feedback_log)
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'total_interactions': len(self.interaction_history),
            'knowledge_base_size': len(self.knowledge_base),
            'learned_patterns': self.get_learned_patterns(),
            'memory_status': 'healthy'
        }
        
        if self.interaction_history:
            metrics['interactions_today'] = self._count_today()
        
        return metrics
    
    def _count_today(self) -> int:
        today = datetime.now().date()
        count = 0
        
        for interaction in self.interaction_history[-100:]:
            try:
                timestamp = datetime.fromisoformat(interaction.get('timestamp', ''))
                if timestamp.date() == today:
                    count += 1
            except:
                pass
        
        return count
    
    def store_feedback(self, feedback: Dict[str, Any]) -> None:
        try:
            self.feedback_log.append(feedback)
        except Exception as e:
            self.logger.error(f"Error storing feedback: {str(e)}")
    
    def export_knowledge(self, filepath: str = None) -> str:
        try:
            if filepath is None:
                filepath = f"data/knowledge_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            export_data = {
                'knowledge_base': self.knowledge_base,
                'learned_responses': dict(self.learned_responses),
                'metrics': self.get_metrics(),
                'exported_at': datetime.now().isoformat()
            }
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            self.logger.info(f"Knowledge exported to {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error exporting knowledge: {str(e)}")
            return None
    
    def import_knowledge(self, filepath: str) -> bool:
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            self.knowledge_base.update(data.get('knowledge_base', {}))
            self.learned_responses.update(data.get('learned_responses', {}))
            
            self.logger.info(f"Knowledge imported from {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error importing knowledge: {str(e)}")
            return False
    
    def save_all(self) -> None:
        try:
            self._save_json('data/knowledge_base.json', self.knowledge_base)
            self._save_json('data/user_history.json', self.interaction_history)
            self._save_json('data/performance_metrics.json', self.performance_metrics)
            
            self.logger.info("All data saved to disk")
            
        except Exception as e:
            self.logger.error(f"Error saving data: {str(e)}")
    
    def _save_json(self, filepath: str, data: Any) -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
