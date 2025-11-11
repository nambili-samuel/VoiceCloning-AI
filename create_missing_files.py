import os

def create_grok_client_file():
    """Create the missing grok_client.py file"""
    
    grok_client_content = '''import requests
import json
from typing import Dict, List, Optional
import os

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
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            print(f"Grok API request failed: {e}")
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

def test_grok_connection(api_key: str) -> bool:
    """Test if Grok API connection works"""
    try:
        client = GrokClient(api_key)
        models = client.list_models()
        if models:
            print(f"✓ Grok connection successful. Available models: {models}")
            return True
        else:
            print("✗ No models found")
            return False
    except Exception as e:
        print(f"✗ Grok connection failed: {e}")
        return False
'''

    # Create src directory if it doesn't exist
    os.makedirs('src', exist_ok=True)
    
    # Write the file
    with open('src/grok_client.py', 'w') as f:
        f.write(grok_client_content)
    
    print("✓ Created src/grok_client.py")

def check_all_files():
    """Check if all required files exist"""
    required_files = [
        'src/__init__.py',
        'src/grok_client.py',
        'src/voice_cloning.py', 
        'src/ai_agent.py',
        'src/tts_engine.py',
        'src/audio_processing.py',
        'src/utils.py'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} is missing")
    
    print("\nRunning quick test...")
    try:
        from src.grok_client import GrokClient
        print("✓ GrokClient import successful!")
    except ImportError as e:
        print(f"✗ Import failed: {e}")

if __name__ == "__main__":
    create_grok_client_file()
    check_all_files()
    print("\nNow you can run: python main.py --run-agent")