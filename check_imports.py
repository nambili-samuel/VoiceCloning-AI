import sys
import os

print("Python path:")
for path in sys.path:
    print(f"  {path}")

print("\nCurrent directory:", os.getcwd())
print("Files in current directory:")
for file in os.listdir('.'):
    print(f"  {file}")

print("\nFiles in src directory:")
if os.path.exists('src'):
    for file in os.listdir('src'):
        print(f"  {file}")
else:
    print("  src directory doesn't exist!")

print("\nTrying to import GrokClient...")
try:
    from src.grok_client import GrokClient
    print("✓ SUCCESS: GrokClient imported!")
except ImportError as e:
    print(f"✗ FAILED: {e}")
    print("\nCreating missing files...")
    
    # Create src directory if it doesn't exist
    os.makedirs('src', exist_ok=True)
    
    # Create __init__.py in src
    with open('src/__init__.py', 'w') as f:
        f.write('')
    
    print("✓ Created src/__init__.py")