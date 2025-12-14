from flask import Flask, render_template, request, flash
import os
import socket
import threading
from cryptography.fernet import Fernet
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# --- CONFIGURATION ---
PORT = 9999
BUFFER_SIZE = 4096
# ---------------------

def transfer_file(file_data, original_filename, receiver_address, receiver_port):
    """Encrypts and sends the file over a single, reliable stream."""
    try:
        # 1. Load encryption key
        print("[Transfer Thread] Loading encryption key...")
        with open("secret.key", "rb") as key_file:
            key = key_file.read()
        fernet = Fernet(key)

        # 2. Encrypt the file data
        print("[Transfer Thread] Encrypting file data...")
        encrypted_data = fernet.encrypt(file_data)

        # Save the encrypted file for demonstration purposes
        encrypted_filename = f"encrypted_{original_filename}"
        with open(encrypted_filename, "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)
        print(f"[Transfer Thread] Encrypted file saved as {encrypted_filename}")
        
        # 3. Establish a single connection to the receiver
        print(f"[Transfer Thread] Connecting to {receiver_address}:{receiver_port}...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(45)
            s.connect((receiver_address, receiver_port))
            print("[Transfer Thread] Connected. Sending file...")

            # 4. Prepare and send the header
            header = {
                "filename": original_filename,
                "filesize": len(encrypted_data)
            }
            header_bytes = json.dumps(header).encode('utf-8')
            
            s.sendall(len(header_bytes).to_bytes(4, 'big'))
            s.sendall(header_bytes)

            # 5. Send the encrypted file data in a stream
            offset = 0
            while offset < len(encrypted_data):
                chunk = encrypted_data[offset:offset+BUFFER_SIZE]
                s.sendall(chunk)
                offset += len(chunk)
            
            print("[Transfer Thread] SUCCESS: File sent successfully!")

    except FileNotFoundError:
        print("[Transfer Thread] ERROR: secret.key not found. Ensure key is generated.")
    except ConnectionRefusedError:
        print(f"[Transfer Thread] ERROR: Connection refused by {receiver_address}:{receiver_port}. Is the receiver running?")
    except socket.timeout:
        print(f"[Transfer Thread] ERROR: Connection timed out after 45 seconds. Unable to connect to {receiver_address}:{receiver_port}.")
    except Exception as e:
        print(f'[Transfer Thread] ERROR: An unexpected error occurred: {e}')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    receiver_address = request.form['receiver_address']
    receiver_port = int(request.form['receiver_port'])
    if 'file' not in request.files:
        flash('No file part', 'error')
        return render_template('index.html')
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return render_template('index.html')

    if file and receiver_address and receiver_port:
        file_data = file.read()
        original_filename = file.filename
        
        # Run the transfer in a background thread to not block the web response
        transfer_thread = threading.Thread(target=transfer_file, args=(file_data, original_filename, receiver_address, receiver_port))
        transfer_thread.start()
        
        flash(f'Sending {original_filename} to {receiver_address}:{receiver_port}...', 'success')
        return render_template('index.html')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)