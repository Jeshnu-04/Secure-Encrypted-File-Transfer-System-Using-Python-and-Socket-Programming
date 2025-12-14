import socket
import json
from cryptography.fernet import Fernet


# --- CONFIGURATION ---
HOST = "0.0.0.0"  # Listen on all available network interfaces
PORT = 9999
BUFFER_SIZE = 4096
# ---------------------

def handle_transfer(client_socket):
    """Receives, decrypts, and saves a file from a single connection."""
    try:
        # 1. Read the header length (4 bytes)
        header_len_bytes = client_socket.recv(4)
        if not header_len_bytes:
            print("Connection closed before header length received.")
            return
        header_len = int.from_bytes(header_len_bytes, 'big')

        # 2. Read the header
        header_bytes = client_socket.recv(header_len)
        header = json.loads(header_bytes.decode('utf-8'))
        filename = header['filename']
        filesize = header['filesize']
        
        # Sanitize filename for security
        safe_filename = "".join(c for c in filename if c.isalnum() or c in ('.', '_', '-')).rstrip()
        output_filename = f"decrypted_{safe_filename}"
        
        print(f"\n[CONTROL] Receiving file '{safe_filename}' ({filesize} bytes).")

        # 3. Read the encrypted file data from the stream
        encrypted_data = b""
        bytes_received = 0
        while bytes_received < filesize:
            chunk = client_socket.recv(BUFFER_SIZE)
            if not chunk:
                break  # Connection closed
            encrypted_data += chunk
            bytes_received += len(chunk)
            print(f"Received {bytes_received}/{filesize} bytes", end='\r')
        
        print("\n[DATA] Encrypted data received successfully.")

        if bytes_received != filesize:
            print(f"Error: Expected {filesize} bytes, but received {bytes_received}.")
            return

        # 4. Decrypt the data
        print("[DECRYPT] Decrypting file...")
        with open("secret.key", "rb") as key_file:
            key = key_file.read()
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        
        # 5. Save the decrypted file
        with open(output_filename, "wb") as file:
            file.write(decrypted_data)
        print(f"[SUCCESS] File decrypted and saved as {output_filename}")

    except json.JSONDecodeError:
        print("Error: Could not decode header. Invalid format.")
    except FileNotFoundError:
        print("Error: secret.key not found. Cannot decrypt.")
    except Exception as e:
        print(f"An error occurred during transfer: {e}")

def main():
    """Main function to listen for a single file transfer."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"Receiver listening on {HOST}:{PORT} for a single stream connection...")

    while True:
        try:
            client, addr = server.accept()
            print(f"Accepted connection from {addr}")
            with client:
                handle_transfer(client)
            print("\nTransfer complete. Ready for next connection.")
        except KeyboardInterrupt:
            print("\nServer shutting down.")
            break
        except Exception as e:
            print(f"A server error occurred: {e}")
    
    server.close()

if __name__ == "__main__":
    main()