# Secure Encrypted Network Communication System

This project is a Python-based secure communication system that allows users from different networks to send data safely over the internet using encrypted connections. The system ensures data confidentiality, authentication, and reliable transmission by combining cryptography with network tunneling via ngrok.

---

## Features
- End-to-end encrypted data transfer
- Secure communication across different networks
- Token-based sender authentication
- Client–server architecture
- Supports multiple clients
- Internet exposure using ngrok tunneling

---

## Tech Stack
- Python
- Socket Programming
- Cryptography (Fernet – Symmetric Encryption)
- ngrok
- Client–Server Networking

---

##  How It Works
1. A secret encryption key is generated and shared securely.
2. The sender encrypts the data using the shared key.
3. Encrypted data is transmitted over the network using sockets.
4. ngrok exposes the receiver to the public internet.
5. The receiver authenticates the sender using a token.
6. The received data is decrypted securely at the receiver end.

---

##  Project Structure
- `generate_key.py` – Generates encryption key
- `sender_client.py` – Encrypts and sends data
- `receiver_ngrok.py` – Receives and decrypts data
- `allowed_tokens.txt` – Authorized sender tokens
- `secret.key` – Encryption key

---

## Use Cases
- Secure file sharing over public networks
- Encrypted communication systems
- Networking and cybersecurity projects
- Academic and learning purposes

---

## Note
This project uses symmetric encryption. The encryption key must be kept secure and shared only with trusted users.

---

## License
This project is for educational and learning purposes.
