import os
import sys

def setup_project():
    """Complete project setup"""
    
    print("=== Setting up Voice AI Agent Project ===\n")
    
    # Create directory structure
    directories = [
        'src',
        'config', 
        'data/raw_audio',
        'data/processed_audio',
        'data/models',
        'training',
        'examples'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created {directory}/")
    
    # Create __init__.py files
    init_files = [
        'src/__init__.py',
        'config/__init__.py',
        'training/__init__.py',
        'examples/__init__.py'
    ]
    
    for init_file in init_files:
        with open(init_file, 'w') as f:
            f.write('')
        print(f"✓ Created {init_file}")
    
    print("\n✓ Project structure created!")
    
    # Test imports
    print("\n=== Testing Imports ===")
    try:
        from src.grok_client import GrokClient
        print("✓ GrokClient import successful")
    except ImportError:
        print("✗ GrokClient import failed - creating file...")
        create_grok_client_file()
    
    try:
        from src.ai_agent import AIAgent
        print("✓ AIAgent import successful")
    except ImportError as e:
        print(f"✗ AIAgent import failed: {e}")
    
    print("\n=== Setup Complete ===")
    print("Next steps:")
    print("1. Add your Grok API key to examples/run_agent.py")
    print("2. Record your voice samples in data/raw_audio/your_voice/")
    print("3. Run: python main.py --clone-voice --audio-dir data/raw_audio/your_voice")
    print("4. Run: python main.py --run-agent")

def create_grok_client_file():
    """Create the grok_client.py file"""
    content = '''import requests
import json
from typing import Dict, List, Optional

class GrokClient:
    def __init__(self, api_key: str, base_url: str = "https://api.x.ai/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def create_chat_completion(self, 
                             messages: List[Dict[str, str]],
                             model: str = "grok-beta",
                             temperature: float = 0.7,
                             max_tokens: int = 500,
                             stream: bool = False) -> Optional[str]:
        """Create chat completion using Grok API"""
        try:
            url = f"{self.base_url}/chat/completions"
            
            payload = {
                "messages": messages,
                "model": model,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": stream
            }
            
            print(f"Sending request to Grok API...")
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            print(f"Grok API request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response body: {e.response.text}")
            return None
        except KeyError as e:
            print(f"Unexpected response format from Grok API: {e}")
            return None
        except Exception as e:
            print(f"Error in Grok API call: {e}")
            return None
    
    def list_models(self) -> List[str]:
        """List available Grok models"""
        try:
            url = f"{self.base_url}/models"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return [model['id'] for model in data.get('data', [])]
            
        except Exception as e:
            print(f"Error listing Grok models: {e}")
            return []
'''
    
    with open('src/grok_client.py', 'w') as f:
        f.write(content)
    print("✓ Created src/grok_client.py")

if __name__ == "__main__":
    setup_project()