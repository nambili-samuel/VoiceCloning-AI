import argparse
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description='Grok Voice AI Agent System')
    parser.add_argument('--clone-voice', action='store_true',
                       help='Clone voice from audio files using Bark')
    parser.add_argument('--run-agent', action='store_true',
                       help='Run Grok AI agent with cloned voice')
    parser.add_argument('--audio-dir', type=str,
                       help='Directory containing audio files for cloning')
    parser.add_argument('--speaker-name', type=str, default="user",
                       help='Name for the cloned voice')
    parser.add_argument('--test-voice', action='store_true',
                       help='Test cloned voice without running agent')
    
    args = parser.parse_args()
    
    if args.clone_voice:
        if not args.audio_dir:
            print("Please specify audio directory with --audio-dir")
            return
        
        from training.train_voice_clone import train_voice_clone
        train_voice_clone(args.audio_dir, args.speaker_name)
        
    elif args.run_agent:
        from examples.run_agent import run_grok_agent
        run_grok_agent()
        
    elif args.test_voice:
        from src.voice_cloning import BarkVoiceCloner
        
        voice_cloner = BarkVoiceCloner()
        speaker_name = args.speaker_name
        
        if not voice_cloner.load_voice_prompt(speaker_name):
            print(f"Voice prompt for {speaker_name} not found. Please train first.")
            print("Run: python main.py --clone-voice --audio-dir data/raw_audio/your_voice --speaker-name your_voice")
            return
        
        print("Testing cloned voice...")
        test_texts = [
            "Hello! I'm testing my cloned voice with Bark.",
            "This is pretty amazing technology, don't you think?",
            "I can't believe how natural this sounds!",
            "The future of voice AI is here, and it's incredible."
        ]
        
        for i, text in enumerate(test_texts):
            output_path = f"data/processed_audio/voice_test_{i+1}.wav"
            print(f"Generating: '{text}'")
            success = voice_cloner.synthesize_speech(
                text=text,
                speaker_name=speaker_name,
                output_path=output_path
            )
            if success:
                print(f"Saved to: {output_path}")
            else:
                print("Generation failed")
        
    else:
        print("Grok Voice AI Agent System")
        print("==========================")
        print("Available commands:")
        print("--clone-voice --audio-dir ./your_voice -- Clone your voice")
        print("--run-agent                    -- Run Grok AI agent")
        print("--test-voice --speaker-name your_voice -- Test cloned voice")
        print("\nExample workflow:")
        print("1. python main.py --clone-voice --audio-dir data/raw_audio/your_voice")
        print("2. python main.py --test-voice --speaker-name your_voice")
        print("3. python main.py --run-agent")

if __name__ == "__main__":
    main()