import os
import sys
sys.path.append('..')

from src.voice_cloning import BarkVoiceCloner
from src.ai_agent import AIAgent

def run_grok_agent():
    """Run the AI agent with Grok and Bark cloned voice"""
    
    # Initialize Bark voice cloner
    voice_cloner = BarkVoiceCloner()
    speaker_name = "your_voice"  # Change to your cloned voice name
    
    # Load voice prompt
    if not voice_cloner.load_voice_prompt(speaker_name):
        print(f"Voice prompt for {speaker_name} not found. Please train first.")
        print("Run: python main.py --clone-voice --audio-dir data/raw_audio/your_voice --speaker-name your_voice")
        return
    
    # Initialize Grok AI agent (replace with your xAI API key)
    grok_api_key = "put your Grok API key here"  # Get from https://api.x.ai/
    
    if grok_api_key == "put your Grok API key here":
        print("Please set your Grok API key in the script")
        print("You can get one from: https://api.x.ai/")
        return
    
    agent = AIAgent(
        grok_api_key=grok_api_key,
        voice_cloner=voice_cloner,
        cloned_voice_name=speaker_name,
        model="grok-beta"
    )
    
    print("=== Grok AI Agent with Voice Cloning ===")
    print("Choose mode:")
    print("1. Wake word mode (say 'assistant' to activate)")
    print("2. Interactive text mode")
    print("3. Voice interactive mode (voice only)")
    
    choice = input("Enter choice (1, 2, or 3): ").strip()
    
    try:
        if choice == "2":
            print("\n=== Interactive Text Mode ===")
            print("Grok's personality: Witty, humorous, and authentic")
            print("Type 'quit' to exit\n")
            agent.interactive_mode()
        elif choice == "3":
            print("\n=== Voice Interactive Mode ===")
            print("Speak naturally. Say 'goodbye' to exit")
            agent.voice_interactive_mode()
        else:
            print("\n=== Wake Word Mode ===")
            print("Say 'assistant' to activate Grok")
            agent.start_continuous_listening()
    except KeyboardInterrupt:
        print("\nStopping Grok AI Agent...")
        agent.stop()

if __name__ == "__main__":
    run_grok_agent()