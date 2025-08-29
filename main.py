#!/usr/bin/env python3
"""
OpenAI Unified Agent - Main CLI Interface

This module provides a legendary command-line interface for interacting with
all supported OpenAI models through a unified, professional system.
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import asdict
from typing import Optional, Dict, Any

from config import ModelRegistry, AgentConfig
from agent import UnifiedOpenAIAgent, list_agents, show_agent_info
from export import export_conversation, get_supported_formats, validate_export_format
from utils import ColorUtils, ValidationUtils


class EnhancedCLI:
    """Enhanced CLI interface with legendary user experience"""
    
    def __init__(self):
        self.current_agent: Optional[UnifiedOpenAIAgent] = None
    
    def display_welcome(self):
        """Display welcome banner"""
        banner = f"""
{ColorUtils.info('╔══════════════════════════════════════════════════════════════╗')}
{ColorUtils.info('║')}            {ColorUtils.success('🤖 OpenAI Unified Agent System')}                 {ColorUtils.info('║')}
{ColorUtils.info('║')}               {ColorUtils.warning('Professional AI Chat Interface')}             {ColorUtils.info('║')}
{ColorUtils.info('╠══════════════════════════════════════════════════════════════╣')}
{ColorUtils.info('║')} {ColorUtils.success('Supported Models:')}                                         {ColorUtils.info('║')}
{ColorUtils.info('║')}   • GPT-4.1       - Advanced model with comprehensive capabilities  {ColorUtils.info('║')}
{ColorUtils.info('║')}   • GPT-4.1 Mini  - Balanced performance and efficiency            {ColorUtils.info('║')}
{ColorUtils.info('║')}   • GPT-4.1 Nano  - Lightweight model optimized for speed        {ColorUtils.info('║')}
{ColorUtils.info('║')}                                                                  {ColorUtils.info('║')}
{ColorUtils.info('║')} {ColorUtils.success('Features:')}                                                 {ColorUtils.info('║')}
{ColorUtils.info('║')}   • File inclusion with {{filename}} syntax                      {ColorUtils.info('║')}
{ColorUtils.info('║')}   • Multi-format exports (JSON, TXT, MD, HTML)                 {ColorUtils.info('║')}
{ColorUtils.info('║')}   • Conversation history with search                            {ColorUtils.info('║')}
{ColorUtils.info('║')}   • Advanced configuration management                           {ColorUtils.info('║')}
{ColorUtils.info('╚══════════════════════════════════════════════════════════════╝')}
        """
        print(banner)
    
    def display_models_info(self):
        """Display detailed information about available models"""
        print(f"\n{ColorUtils.info('📊 Available Models:')}")
        print("-" * 80)
        
        for model_key, model_info in ModelRegistry.SUPPORTED_MODELS.items():
            timeout = model_info['timeout']
            print(f"{ColorUtils.success(f'• {model_info['name']}:')} {ColorUtils.warning(model_key)}")
            print(f"  Description: {model_info['description']}")
            print(f"  Timeout: {ColorUtils.info(f'{timeout}s ({timeout//60}m {timeout%60}s)')}")
            print(f"  Max Tokens: {ColorUtils.info(str(model_info['max_tokens']))}")
            print(f"  Cost Tier: {ColorUtils.warning(model_info['cost_tier'].title())}")
            print()
    
    def create_agent_interactive(self) -> Optional[UnifiedOpenAIAgent]:
        """Interactive agent creation"""
        print(f"\n{ColorUtils.info('🚀 Creating New Agent')}")
        print("-" * 40)
        
        # Get agent ID
        while True:
            agent_id = input(ColorUtils.info("Enter agent ID (alphanumeric, hyphens, underscores): ")).strip()
            if not agent_id:
                print(ColorUtils.error("Agent ID cannot be empty"))
                continue
            if not ValidationUtils.validate_agent_id(agent_id):
                print(ColorUtils.error("Invalid agent ID format"))
                continue
            break
        
        # Select model
        print(f"\n{ColorUtils.success('Available Models:')}")
        models = ModelRegistry.list_models()
        for i, model in enumerate(models, 1):
            model_info = ModelRegistry.get_model_info(model)
            print(f"  {i}. {ColorUtils.warning(model_info['name'])} ({model}) - {model_info['description']}")
        
        while True:
            try:
                choice = input(f"\nSelect model (1-{len(models)}) [1]: ").strip()
                if not choice:
                    choice = "1"
                model_index = int(choice) - 1
                if 0 <= model_index < len(models):
                    selected_model = models[model_index]
                    break
                else:
                    print(ColorUtils.error(f"Please enter a number between 1 and {len(models)}"))
            except ValueError:
                print(ColorUtils.error("Please enter a valid number"))
        
        # Create and configure agent
        try:
            agent = UnifiedOpenAIAgent(agent_id, selected_model)
            model_display = ModelRegistry.get_model_display_name(selected_model)
            print(ColorUtils.success(f"\n✅ Agent '{agent_id}' created successfully with {model_display}!"))
            
            # Ask for configuration
            if input(ColorUtils.info("Would you like to configure the agent now? (y/N): ")).strip().lower() in ['y', 'yes']:
                self.configure_agent_interactive(agent)
            
            return agent
            
        except Exception as e:
            print(ColorUtils.error(f"Failed to create agent: {e}"))
            return None
    
    def configure_agent_interactive(self, agent: UnifiedOpenAIAgent):
        """Interactive agent configuration"""
        print(f"\n{ColorUtils.info('⚙️ Configuring Agent')}")
        print("-" * 30)
        
        config_updates = {}
        
        # Temperature
        current_temp = agent.config.temperature
        temp_input = input(f"Temperature (0.0-2.0) [{current_temp}]: ").strip()
        if temp_input:
            try:
                temp_value = float(temp_input)
                if ValidationUtils.validate_temperature(temp_value):
                    config_updates['temperature'] = temp_value
                else:
                    print(ColorUtils.error("Invalid temperature value"))
            except ValueError:
                print(ColorUtils.error("Invalid temperature format"))
        
        # System prompt
        current_prompt = agent.config.system_prompt or "None"
        print(f"Current system prompt: {ColorUtils.warning(current_prompt[:50] + '...' if len(current_prompt) > 50 else current_prompt)}")
        system_prompt = input("System prompt (press Enter to keep current): ").strip()
        if system_prompt:
            config_updates['system_prompt'] = system_prompt
        
        # Max tokens
        current_tokens = agent.config.max_tokens
        tokens_input = input(f"Max tokens [{current_tokens}]: ").strip()
        if tokens_input:
            try:
                tokens_value = int(tokens_input)
                if ValidationUtils.validate_max_tokens(tokens_value):
                    config_updates['max_tokens'] = tokens_value
                else:
                    print(ColorUtils.error("Invalid max tokens value"))
            except ValueError:
                print(ColorUtils.error("Invalid max tokens format"))
        
        # Streaming
        current_stream = agent.config.stream
        stream_input = input(f"Enable streaming (y/n) [{'y' if current_stream else 'n'}]: ").strip().lower()
        if stream_input in ['y', 'yes', 'true']:
            config_updates['stream'] = True
        elif stream_input in ['n', 'no', 'false']:
            config_updates['stream'] = False
        
        # Apply updates
        if config_updates:
            try:
                agent.update_config(**config_updates)
                print(ColorUtils.success("✅ Configuration updated successfully!"))
            except Exception as e:
                print(ColorUtils.error(f"Configuration update failed: {e}"))
        else:
            print(ColorUtils.info("No configuration changes made"))
    
    def interactive_chat(self, agent: UnifiedOpenAIAgent):
        """Enhanced interactive chat session"""
        model_display = ModelRegistry.get_model_display_name(agent.model)
        model_info = agent.get_model_info()
        
        # Chat header
        print(f"\n{ColorUtils.success('╔══════════════════════════════════════════════════════════════╗')}")
        print(f"{ColorUtils.success('║')}            {ColorUtils.info('💬 Interactive Chat Session')}                    {ColorUtils.success('║')}")
        print(f"{ColorUtils.success('╚══════════════════════════════════════════════════════════════╝')}")
        print(f"{ColorUtils.success('Agent:')} {ColorUtils.warning(agent.agent_id)}")
        print(f"{ColorUtils.success('Model:')} {ColorUtils.warning(f'{model_display} ({agent.model})')}")
        print(f"{ColorUtils.success('Timeout:')} {ColorUtils.info(f'{model_info.get("timeout", "Unknown")}s')}")
        print(f"{ColorUtils.success('Commands:')} Type {ColorUtils.info('help')} for available commands, {ColorUtils.info('quit')} to exit")
        print("-" * 80)
        
        while True:
            try:
                user_input = input(f"\n{ColorUtils.info('You:')} ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith('/') or user_input in ['help', 'quit', 'exit']:
                    if user_input.startswith('/'):
                        command = user_input[1:]
                    else:
                        command = user_input
                    
                    if self.handle_chat_command(command, agent):
                        break  # Exit chat
                    continue
                
                # Regular message - send to API
                print(f"\n{ColorUtils.success('Assistant:')} ", end="", flush=True)
                
                response_text = ""
                try:
                    for chunk in agent.call_api(user_input):
                        print(chunk, end="", flush=True)
                        response_text += chunk
                    print()  # New line after response
                    
                except KeyboardInterrupt:
                    print(f"\n{ColorUtils.warning('Response interrupted')}")
                except Exception as e:
                    print(f"\n{ColorUtils.error(f'Error: {e}')}")
                
            except KeyboardInterrupt:
                print(f"\n{ColorUtils.warning('Use \"quit\" command to exit gracefully')}")
            except Exception as e:
                print(f"\n{ColorUtils.error(f'Unexpected error: {e}')}")
    
    def handle_chat_command(self, command: str, agent: UnifiedOpenAIAgent) -> bool:
        """Handle chat commands. Returns True if should exit chat."""
        parts = command.split()
        cmd = parts[0].lower()
        
        if cmd in ['help', 'h']:
            self.show_chat_help()
        
        elif cmd in ['quit', 'exit', 'q']:
            print(ColorUtils.success("👋 Goodbye!"))
            return True
        
        elif cmd in ['history', 'hist']:
            limit = 5
            if len(parts) > 1:
                try:
                    limit = int(parts[1])
                except ValueError:
                    print(ColorUtils.error("Invalid number for history limit"))
                    return False
            
            self.show_history(agent, limit)
        
        elif cmd == 'search':
            if len(parts) < 2:
                print(ColorUtils.error("Usage: search <term>"))
                return False
            
            search_term = ' '.join(parts[1:])
            self.search_history(agent, search_term)
        
        elif cmd in ['stats', 'statistics']:
            self.show_statistics(agent)
        
        elif cmd in ['config', 'configuration']:
            self.show_configuration(agent)
        
        elif cmd == 'export':
            if len(parts) < 2:
                print(ColorUtils.error(f"Usage: export <{'/'.join(get_supported_formats().keys())}>"))
                return False
            
            format_type = parts[1].lower()
            self.export_conversation(agent, format_type)
        
        elif cmd == 'clear':
            self.clear_history(agent)
        
        elif cmd in ['files', 'file']:
            self.list_files(agent)
        
        elif cmd in ['info', 'agent-info']:
            show_agent_info(agent.agent_id)
        
        elif cmd == 'model':
            self.show_model_info(agent)
        
        elif cmd == 'switch':
            if len(parts) < 2:
                print(ColorUtils.error("Usage: switch <model>"))
                self.display_models_info()
                return False
            
            new_model = parts[1]
            self.switch_model(agent, new_model)
        
        else:
            print(ColorUtils.error(f"Unknown command: {cmd}"))
            print(ColorUtils.info("Type 'help' for available commands"))
        
        return False
    
    def show_chat_help(self):
        """Display chat help information"""
        help_text = f"""
{ColorUtils.success('📚 Available Commands:')}
{'-' * 40}
{ColorUtils.info('help, h')}              - Show this help message
{ColorUtils.info('history [n]')}          - Show last n messages (default: 5)
{ColorUtils.info('search <term>')}        - Search conversation history
{ColorUtils.info('stats')}                - Show conversation statistics
{ColorUtils.info('config')}               - Show current configuration
{ColorUtils.info('export <format>')}      - Export conversation (json/txt/md/html)
{ColorUtils.info('clear')}                - Clear conversation history
{ColorUtils.info('files')}                - List available files for inclusion
{ColorUtils.info('info')}                 - Show agent information
{ColorUtils.info('model')}                - Show current model information
{ColorUtils.info('switch <model>')}       - Switch to different model
{ColorUtils.info('quit, exit, q')}        - Exit chat

{ColorUtils.success('📁 File Inclusion:')}
Use {{filename}} in your messages to include file contents.
Supported: Programming files, config files, documentation, etc.

{ColorUtils.success('🎨 Models Available:')}"""
        
        for model in ModelRegistry.list_models():
            model_info = ModelRegistry.get_model_info(model)
            help_text += f"\n{ColorUtils.warning(model)} - {model_info['description']}"
        
        print(help_text)
    
    def show_history(self, agent: UnifiedOpenAIAgent, limit: int):
        """Show conversation history"""
        recent_messages = agent.messages[-limit:]
        if not recent_messages:
            print(ColorUtils.warning("No messages in history"))
            return
        
        print(f"\n{ColorUtils.success(f'📜 Last {len(recent_messages)} messages:')}")
        print("-" * 50)
        
        for i, msg in enumerate(recent_messages, 1):
            timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M:%S")
            role = msg["role"]
            content = msg["content"]
            preview = content[:100] + "..." if len(content) > 100 else content
            
            role_color = ColorUtils.info if role == "user" else ColorUtils.success
            print(f"{ColorUtils.warning(f'[{timestamp}]')} {role_color(role.title())}: {preview}")
    
    def search_history(self, agent: UnifiedOpenAIAgent, term: str):
        """Search conversation history"""
        results = agent.search_history(term)
        
        if not results:
            print(ColorUtils.warning(f"No matches found for '{term}'"))
            return
        
        print(f"\n{ColorUtils.success(f'🔍 Found {len(results)} matches for \"{term}\":')}")
        print("-" * 50)
        
        for result in results:
            msg = result["message"]
            timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M:%S")
            role = msg["role"]
            preview = result["preview"]
            
            role_color = ColorUtils.info if role == "user" else ColorUtils.success
            print(f"{ColorUtils.warning(f'[{timestamp}]')} {role_color(role.title())}: {preview}")
    
    def show_statistics(self, agent: UnifiedOpenAIAgent):
        """Show conversation statistics"""
        stats = agent.get_statistics()
        model_display = ModelRegistry.get_model_display_name(agent.model)
        
        print(f"\n{ColorUtils.success('📊 Conversation Statistics:')}")
        print("-" * 40)
        print(f"Model: {ColorUtils.warning(f'{model_display} ({agent.model})')}")
        print(f"Total Messages: {ColorUtils.info(str(stats['total_messages']))}")
        print(f"User Messages: {ColorUtils.info(str(stats['user_messages']))}")
        print(f"Assistant Messages: {ColorUtils.info(str(stats['assistant_messages']))}")
        print(f"Total Characters: {ColorUtils.info(f'{stats['total_characters']:,}')}")
        print(f"Average Message Length: {ColorUtils.info(f"{stats['average_message_length']:,}")}")
        
        if stats['first_message']:
            print(f"First Message: {ColorUtils.warning(stats['first_message'])}")
            print(f"Last Message: {ColorUtils.warning(stats['last_message'])}")
            print(f"Duration: {ColorUtils.info(stats['conversation_duration'])}")
    
    def show_configuration(self, agent: UnifiedOpenAIAgent):
        """Show current agent configuration"""
        print(f"\n{ColorUtils.success('⚙️ Agent Configuration:')}")
        print("-" * 30)
        
        config_dict = asdict(agent.config)
        for key, value in config_dict.items():
            if key not in ['created_at', 'updated_at'] and value is not None:
                display_key = key.replace('_', ' ').title()
                
                if key == 'model':
                    model_name = ModelRegistry.get_model_display_name(str(value))
                    print(f"{display_key}: {ColorUtils.warning(f'{value} ({model_name})')}")
                elif key == 'system_prompt' and len(str(value)) > 50:
                    preview = str(value)[:47] + "..."
                    print(f"{display_key}: {ColorUtils.info(preview)}")
                else:
                    print(f"{display_key}: {ColorUtils.info(str(value))}")
    
    def export_conversation(self, agent: UnifiedOpenAIAgent, format_type: str):
        """Export conversation"""
        if not validate_export_format(format_type):
            formats = list(get_supported_formats().keys())
            print(ColorUtils.error(f"Invalid format. Supported formats: {', '.join(formats)}"))
            return
        
        try:
            filepath = export_conversation(
                agent.agent_id, 
                agent.base_dir, 
                agent.config, 
                agent.messages, 
                format_type
            )
            print(ColorUtils.success(f"✅ Conversation exported to: {filepath}"))
        except Exception as e:
            print(ColorUtils.error(f"Export failed: {e}"))
    
    def clear_history(self, agent: UnifiedOpenAIAgent):
        """Clear conversation history"""
        confirm = input(ColorUtils.warning("Clear conversation history? This cannot be undone. (y/N): ")).strip().lower()
        if confirm in ['y', 'yes']:
            agent.clear_history()
            print(ColorUtils.success("✅ Conversation history cleared"))
        else:
            print(ColorUtils.info("History clearing cancelled"))
    
    def list_files(self, agent: UnifiedOpenAIAgent):
        """List available files for inclusion"""
        files = agent.list_files()
        
        if not files:
            print(ColorUtils.warning("No supported files found for inclusion"))
            return
        
        print(f"\n{ColorUtils.success('📁 Available files for inclusion:')}")
        print("-" * 50)
        
        for i, file_info in enumerate(files[:20], 1):
            print(f"{i:2d}. {ColorUtils.info(file_info)}")
        
        if len(files) > 20:
            print(ColorUtils.warning(f"... and {len(files) - 20} more files"))
        
        print(f"\n{ColorUtils.info('Use {{filename}} in your message to include file contents')}")
    
    def show_model_info(self, agent: UnifiedOpenAIAgent):
        """Show current model information"""
        model_info = agent.get_model_info()
        
        print(f"\n{ColorUtils.success('🤖 Current Model Information:')}")
        print("-" * 40)
        print(f"Model: {ColorUtils.warning(agent.model)}")
        print(f"Name: {ColorUtils.info(model_info.get('name', 'Unknown'))}")
        print(f"Description: {ColorUtils.info(model_info.get('description', 'No description'))}")
        print(f"Timeout: {ColorUtils.info(f"{model_info.get('timeout', 'Unknown')}s")}")
        print(f"Max Tokens: {ColorUtils.info(str(model_info.get('max_tokens', 'Unknown')))}")
        print(f"Cost Tier: {ColorUtils.warning(model_info.get('cost_tier', 'Unknown').title())}")
        print(f"API Format: {ColorUtils.info(model_info.get('api_format', 'Unknown'))}")
    
    def switch_model(self, agent: UnifiedOpenAIAgent, new_model: str):
        """Switch to a different model"""
        if not ModelRegistry.is_valid_model(new_model):
            print(ColorUtils.error(f"Invalid model: {new_model}"))
            print(f"\n{ColorUtils.info('Available models:')}")
            for model in ModelRegistry.list_models():
                model_info = ModelRegistry.get_model_info(model)
                print(f"  • {ColorUtils.warning(model)} - {model_info['name']}")
            return
        
        try:
            old_model = agent.model
            agent.switch_model(new_model)
            
            old_display = ModelRegistry.get_model_display_name(old_model)
            new_display = ModelRegistry.get_model_display_name(new_model)
            
            print(ColorUtils.success(f"✅ Switched from {old_display} to {new_display}"))
        except Exception as e:
            print(ColorUtils.error(f"Failed to switch model: {e}"))
    
    def list_all_agents(self):
        """List all available agents"""
        agents = list_agents()
        
        if not agents:
            print(ColorUtils.warning("No agents found"))
            return
        
        print(f"\n{ColorUtils.success('🤖 Available Agents:')}")
        print("-" * 90)
        print(f"{'ID':<20} {'Model':<25} {'Messages':<10} {'Last Updated':<20}")
        print("-" * 90)
        
        for agent_info in agents:
            updated = agent_info.get("updated_at", "Unknown")
            if updated != "Unknown":
                try:
                    updated = datetime.fromisoformat(updated).strftime("%Y-%m-%d %H:%M")
                except:
                    pass
            
            model = agent_info.get('model', 'gpt-4.1')
            model_display = ModelRegistry.get_model_display_name(model)
            message_count = agent_info.get('message_count', 0)
            
            print(f"{agent_info['id']:<20} {model_display:<25} {message_count:<10} {updated:<20}")
    
    def run(self):
        """Main CLI entry point"""
        # Set up argument parser
        parser = argparse.ArgumentParser(
            description="OpenAI Unified Agent - Professional AI Chat Interface",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s --agent-id my-agent                    # Start interactive chat
  %(prog)s --agent-id my-agent --model gpt-4.1-mini  # Use specific model
  %(prog)s --list                                 # List all agents
  %(prog)s --agent-id my-agent --export html      # Export conversation
  %(prog)s --agent-id my-agent --config          # Configure agent
  %(prog)s --models                              # Show model information
            """
        )
        
        parser.add_argument("--agent-id", help="Agent ID for the chat session")
        parser.add_argument("--model", choices=ModelRegistry.list_models(), 
                          help="OpenAI model to use")
        parser.add_argument("--list", action="store_true", help="List all available agents")
        parser.add_argument("--info", metavar="ID", help="Show detailed agent information")
        parser.add_argument("--config", action="store_true", help="Configure agent interactively")
        parser.add_argument("--temperature", type=float, help="Override temperature (0.0-2.0)")
        parser.add_argument("--no-stream", action="store_true", help="Disable streaming")
        parser.add_argument("--export", choices=list(get_supported_formats().keys()), 
                          help="Export conversation format")
        parser.add_argument("--models", action="store_true", help="Show available models")
        parser.add_argument("--create", action="store_true", help="Create a new agent interactively")
        
        args = parser.parse_args()
        
        # Show welcome banner unless it's a simple command
        if not any([args.list, args.info, args.models]):
            self.display_welcome()
        
        try:
            # Handle various commands
            if args.models:
                self.display_models_info()
                return
            
            if args.list:
                self.list_all_agents()
                return
            
            if args.info:
                show_agent_info(args.info)
                return
            
            if args.create:
                agent = self.create_agent_interactive()
                if agent:
                    self.current_agent = agent
                    self.interactive_chat(agent)
                return
            
            # Require agent-id for other operations
            if not args.agent_id:
                if len(sys.argv) == 1:
                    # No arguments provided, show interactive help
                    parser.print_help()
                    print(f"\n{ColorUtils.info('💡 Quick start: Create a new agent with --create')}")
                    print(f"{ColorUtils.info('💡 Or use --list to see existing agents')}")
                else:
                    parser.print_help()
                    print(f"\n{ColorUtils.error('Error: --agent-id is required for most operations')}")
                return
            
            # Initialize agent
            model = args.model or "gpt-4.1"
            
            try:
                agent = UnifiedOpenAIAgent(args.agent_id, model)
                self.current_agent = agent
            except Exception as e:
                print(ColorUtils.error(f"Failed to initialize agent: {e}"))
                return
            
            # Handle config command
            if args.config:
                self.configure_agent_interactive(agent)
                return
            
            # Handle export command
            if args.export:
                self.export_conversation(agent, args.export)
                return
            
            # Apply command line overrides
            config_updates = {}
            if args.temperature is not None:
                if ValidationUtils.validate_temperature(args.temperature):
                    config_updates["temperature"] = args.temperature
                else:
                    print(ColorUtils.error(f"Invalid temperature: {args.temperature}"))
                    return
            
            if args.no_stream:
                config_updates["stream"] = False
            
            # Apply configuration updates
            if config_updates:
                try:
                    agent.update_config(**config_updates)
                    print(ColorUtils.success("✅ Configuration updated"))
                except Exception as e:
                    print(ColorUtils.error(f"Configuration update failed: {e}"))
                    return
            
            # Start interactive chat
            self.interactive_chat(agent)
            
        except KeyboardInterrupt:
            print(f"\n{ColorUtils.warning('👋 Goodbye!')}")
        except Exception as e:
            print(ColorUtils.error(f"Unexpected error: {e}"))
            sys.exit(1)


def main():
    """Main entry point"""
    cli = EnhancedCLI()
    cli.run()


if __name__ == "__main__":
    main()