#!/usr/bin/env python3
"""
Jarvis AI Assistant - Main Entry Point
Standalone AI that learns from interactions and self-improves
"""

import sys
import json
from core.ai_engine import Jarvis
from utils.logger import Logger

def print_banner():
    banner = """
    ╔════════════════════════════════════════════════════════╗
    ║         JARVIS - AI Assistant with Self-Learning        ║
    ║              Standalone Intelligent System              ║
    ╚════════════════════════════════════════════════════════╝
    
    Welcome! I'm Jarvis, your AI assistant.
    I learn from every interaction and continuously improve.
    
    Commands:
    - Type your query or message
    - Type 'stats' to see performance metrics
    - Type 'learn' to show what I've learned
    - Type 'history' to show recent interactions
    - Type 'clear' to clear conversation context
    - Type 'export' to save my knowledge
    - Type 'help' for more commands
    - Type 'exit' to quit
    """
    print(banner)

def print_help():
    help_text = """
    Available Commands:
    ==================
    
    Interactive:
    - Any message will be processed by Jarvis
    - Give feedback like "That was helpful!" for learning
    
    System Commands:
    - stats       : Show performance metrics
    - learn       : Display learned patterns
    - history     : Show recent interactions
    - clear       : Clear conversation context
    - status      : Get current system status
    - export      : Export knowledge base
    - import <file> : Import knowledge base
    - help        : Show this help message
    - exit        : Exit the application
    """
    print(help_text)

def handle_command(command: str, jarvis: Jarvis, logger: Logger) -> bool:
    cmd = command.lower().strip()
    
    if cmd == 'exit':
        print("\nShutting down Jarvis...")
        jarvis.shutdown()
        return False
    
    elif cmd == 'stats':
        print("\n=== Performance Metrics ===")
        metrics = jarvis.memory.get_metrics()
        print(json.dumps(metrics, indent=2))
        print()
    
    elif cmd == 'learn':
        print("\n=== Learned Patterns ===")
        patterns = jarvis.get_learned_patterns()
        print(patterns)
        print()
    
    elif cmd == 'history':
        print("\n=== Recent Interactions ===")
        history = jarvis.get_conversation_history()
        if history:
            for i, interaction in enumerate(history[-10:], 1):
                role = interaction.get('role', 'unknown').upper()
                content = interaction.get('content', '')[:100]
                print(f"{i}. [{role}] {content}")
        else:
            print("No interactions yet.")
        print()
    
    elif cmd == 'clear':
        jarvis.clear_context()
        print("Conversation context cleared.\n")
    
    elif cmd == 'status':
        print("\n=== System Status ===")
        status = jarvis.get_status()
        print(json.dumps(status, indent=2))
        print()
    
    elif cmd == 'export':
        filepath = jarvis.export_knowledge_base()
        print(f"Knowledge base exported to: {filepath}\n")
    
    elif cmd.startswith('import '):
        filepath = cmd.replace('import ', '').strip()
        success = jarvis.import_knowledge_base(filepath)
        if success:
            print(f"Knowledge base imported from: {filepath}\n")
        else:
            print(f"Failed to import from: {filepath}\n")
    
    elif cmd == 'help':
        print_help()
    
    else:
        return True
    
    return True

def main():
    logger = Logger()
    
    try:
        print_banner()
        
        print("Initializing Jarvis AI Engine...")
        jarvis = Jarvis()
        print("✓ Jarvis ready!\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.startswith('/'):
                    command = user_input[1:]
                    if not handle_command(command, jarvis, logger):
                        break
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("\nShutting down Jarvis...")
                    jarvis.shutdown()
                    break
                
                if user_input.lower() == 'help':
                    print_help()
                    continue
                
                response = jarvis.process(user_input)
                print(f"\nJarvis: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\nShutting down Jarvis...")
                jarvis.shutdown()
                break
            
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                print(f"\nError: {str(e)}\n")
    
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
