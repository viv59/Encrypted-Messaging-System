#Description:

This project contains a client-server chat application with additional features for sending encrypted messages and streaming videos.

It has two files namely 210010059_server.py and 210010059_client.py

#Feature:

server.py:

1. This Python script implements the server side of the chat application.
2. It listens for incoming connections from clients, handles client requests, broadcasts messages to all connected clients, and manages client disconnections.
3. The server also maintains a dictionary of client names and their public keys for secure communication.

client.py:

1. This Python script implements the client side of the chat application.
2. It allows users to connect to the server, send messages to specific clients, list available videos, and stream selected videos from the server.
3. The client also supports encryption of messages using RSA encryption.

RSA Implementation:

1. An RSA key pair is generated using the RSA.generate() method, which creates an RSA key object. The generated key pair consists of a public key and a private key. The public key is used for encryption, while the private key is used for decryption.

2. To encrypt a message, the encryptMessage() function is defined. It takes the message to be encrypted and the recipient's public key as input. Inside the function, a PKCS1_OAEP cipher object is created using the recipient's public key. The message is then encrypted using the encrypt() method of the cipher object.

3. To decrypt an encrypted message received from the server, the decryptMessage() function is defined. It takes the encrypted message and the client's private key as input. Inside the function, a PKCS1_OAEP cipher object is created using the client's private key. The encrypted message is then decrypted using the decrypt() method of the cipher object.

4. When sending a message to a recipient, the message is encrypted using the encryptMessage() function before being sent over the network. When a message is received from the server, it may be encrypted. The client_receiver_threa() function continuously receives data from the server and decrypts it using the decryptMessage() function.

#Setup / Demo Instruction:

1. Run the server.py script in a terminal
2. Run the client.py script on every other new terminal as many times as many clients you want
3. Enter your name when prompted by the client script.
4. Use commands like LIST to view available videos and VIDEO\_<name> to stream a specific video.
   To send encrypted messages, enter the recipient's name followed by your message.

#Dependencies:

socket library for socket handling and threading for multiple client connection
json for data handling
OpenCV (cv2)
Crypto library for RSA encryption

#Link

https://youtu.be/PVCJjG2QVnU