import speech_recognition as sr
import threading
import time
from typing import Optional
import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from src.tts_engine import BarkTTSEngine
    from src.voice_cloning import BarkVoiceCloner
    from src.grok_client import GrokClient
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"Import error: {e}")
    DEPENDENCIES_AVAILABLE = False

class AIAgent:
    def __init__(self, grok_api_key: str, voice_cloner: 'BarkVoiceCloner', 
                 cloned_voice_name: str = "user",
                 model: str = "grok-beta"):
        
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("Required dependencies are not available. Please check all files exist.")
        
        self.grok_api_key = grok_api_key
        self.voice_cloner = voice_cloner
        self.cloned_voice_name = cloned_voice_name
        self.model = model
        self.tts_engine = BarkTTSEngine(voice_cloner)
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.wake_word = "assistant"
        self.conversation_history = []
        
        # Initialize Grok client
        self.grok_client = GrokClient(grok_api_key)
        
        # Improve microphone settings for better recognition
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        # Grok-specific personality traits
        self.system_prompt = """You are Grok, an AI assistant with a sense of humor and a rebellious streak. 
        You're helpful, witty, and occasionally sarcastic. You have opinions and aren't afraid to show them.
        Keep your responses concise, engaging, and human-like. Be authentic and don't shy away from humor when appropriate.
        Remember: you're talking to a real person, so be engaging and natural in your conversation."""
    
    def listen_for_wake_word(self, timeout: int = None) -> bool:
        """Listen for wake word to activate agent"""
        with sr.Microphone() as source:
            print(f"Listening for wake word '{self.wake_word}'...")
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=3)
                text = self.recognizer.recognize_google(audio).lower()
                
                if self.wake_word in text:
                    print("Wake word detected!")
                    return True
                    
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except Exception as e:
                print(f"Error in wake word detection: {e}")
            
            return False
    
    def listen_for_speech(self, timeout: int = 10) -> Optional[str]:
        """Listen for user speech and convert to text"""
        with sr.Microphone() as source:
            print("Listening...")
            try:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text
            except sr.WaitTimeoutError:
                print("Listening timeout")
                return None
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None
            except Exception as e:
                print(f"Error in speech recognition: {e}")
                return None
    
    def generate_response(self, user_input: str) -> str:
        """Generate AI response using Grok"""
        try:
            # Add user input to conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Keep only recent conversation to manage context length
            if len(self.conversation_history) > 12:
                self.conversation_history = self.conversation_history[-10:]
            
            # Create system message with Grok's personality
            system_message = {
                "role": "system", 
                "content": self.system_prompt
            }
            
            # Prepare messages for Grok
            messages = [system_message] + self.conversation_history[-8:]
            
            print("Calling Grok API...")
            # Generate response using Grok
            response = self.grok_client.create_chat_completion(
                messages=messages,
                model=self.model,
                temperature=0.8,  # Slightly higher temperature for more creative responses
                max_tokens=200
            )
            
            if response:
                ai_response = response.strip()
                print(f"Grok response: {ai_response}")
                
                # Add AI response to conversation history
                self.conversation_history.append({"role": "assistant", "content": ai_response})
                
                return ai_response
            else:
                return "I apologize, but I'm having trouble generating a response right now. Please try again."
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def speak_response(self, text: str):
        """Speak the response using Bark with cloned voice"""
        self.tts_engine.speak(text, self.cloned_voice_name)
    
    def run_conversation_cycle(self):
        """Run one conversation cycle"""
        user_input = self.listen_for_speech()
        if user_input:
            response = self.generate_response(user_input)
            print(f"Grok: {response}")
            self.speak_response(response)
    
    def start_continuous_listening(self):
        """Start continuous listening for wake word"""
        self.is_listening = True
        print("Grok AI Agent started. Say the wake word to activate.")
        print("Press Ctrl+C to stop.")
        
        while self.is_listening:
            if self.listen_for_wake_word(timeout=5):
                print("How can I help you?")
                self.speak_response("Hey there! What's on your mind?")
                self.run_conversation_cycle()
            time.sleep(0.1)
    
    def interactive_mode(self):
        """Run in interactive mode without wake word"""
        self.is_listening = True
        print("Grok Interactive mode started. Type your queries or say 'quit' to exit.")
        print("Grok's personality: Witty, humorous, and occasionally sarcastic")
        
        while self.is_listening:
            user_input = input("You: ")
            if user_input.lower() in ['quit', 'exit', 'stop']:
                break
            
            response = self.generate_response(user_input)
            print(f"Grok: {response}")
            self.speak_response(response)
    
    def voice_interactive_mode(self):
        """Run in voice-only interactive mode"""
        self.is_listening = True
        print("Grok Voice Interactive mode started.")
        print("Speak your queries. Say 'goodbye' to exit.")
        self.speak_response("Hey! I'm Grok. What would you like to chat about?")
        
        while self.is_listening:
            user_input = self.listen_for_speech(timeout=30)
            
            if not user_input:
                continue
                
            if any(word in user_input.lower() for word in ['goodbye', 'exit', 'stop', 'quit']):
                self.speak_response("Alright, catch you later! Don't do anything I wouldn't do.")
                break
            
            response = self.generate_response(user_input)
            print(f"You: {user_input}")
            print(f"Grok: {response}")
            self.speak_response(response)
    
    def stop(self):
        """Stop the AI agent"""
        self.is_listening = False
        self.tts_engine.stop()