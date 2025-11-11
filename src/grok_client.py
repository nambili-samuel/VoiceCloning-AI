import requests
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

if __name__ == "__main__":
    # Test the Grok client
    api_key = input("Enter your Grok API key to test: ")
    test_grok_connection(api_key)