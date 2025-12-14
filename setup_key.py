"""
Quick script to generate encryption key for the file transfer system.
Run this once and copy secret.key to both sender and receiver machines.
"""

from cryptography.fernet import Fernet
import os
import sys

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def generate_key():
    """Generate a new encryption key."""
    print("=" * 60)
    print("ENCRYPTION KEY GENERATOR")
    print("=" * 60)
    
    # Check if key already exists
    if os.path.exists("secret.key"):
        response = input("\nWARNING: secret.key already exists. Overwrite? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled. Using existing key.")
            return
    
    # Generate new key
    key = Fernet.generate_key()
    
    # Save to file
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    
    print("\nSUCCESS: Encryption key generated successfully!")
    print(f"Saved to: {os.path.abspath('secret.key')}")
    print("\n" + "=" * 60)
    print("IMPORTANT INSTRUCTIONS:")
    print("=" * 60)
    print("1. Copy 'secret.key' to BOTH sender and receiver machines")
    print("2. Keep this key SECRET - anyone with it can decrypt files")
    print("3. Store it securely - losing it means you can't decrypt files")
    print("4. Never commit this key to version control (git)")
    print("=" * 60)
    
    # Display key for manual copying if needed
    print("\nKey content (for manual copying):")
    print("-" * 60)
    print(key.decode('utf-8'))
    print("-" * 60)

if __name__ == "__main__":
    generate_key()