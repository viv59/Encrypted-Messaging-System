import socket
import threading
import json
import cv2

client_dict = {}
dict_client_socket = []


def broadcast(message, dict_client_socket):
    # Broadcasts a message to all connected clients.
    for client_socket in dict_client_socket:
        client_socket.send(message)

def connection_status(name, status_string):
    if status_string == "connected":
        print(f"{name} has connected to the chat")
    elif status_string == "disconnected":
        print(f"{name} is disconnected from the chat")
    else:
        print("Invalid status_string provided.")

def handle_client(client_socket):
    # Handles communication with a client.
    try:
        name = client_socket.recv(1024).decode()
        public_key = client_socket.recv(1024).decode()
        connection_status(name,"connected")

    except Exception as e:
        print("Error!", e)
        return

    while True:
        try:
            client_dict[name] = public_key
            print("Number of clients connected: ", len(client_dict))
            print("Available clients")
            for key in client_dict.keys():
                print(key)
            clients_dict = json.dumps(client_dict).encode()
            broadcast(clients_dict, dict_client_socket)
            message = client_socket.recv(16384)
            try:
                if message.decode().upper() == "QUIT":
                    break
            except:
                broadcast(message, dict_client_socket)

        except Exception as e:
            print("Error while receiving encrypted message", e)
            break

    del client_dict[name]
    dict_client_socket.remove(client_socket)
    clients_dict = json.dumps(client_dict).encode()
    broadcast(clients_dict, dict_client_socket)
    connection_status(name,"disconnected")
    print("Number of clients connected: ", len(client_dict))
    client_socket.close()

def stream_video():
    video_paths = {
        "240p": "video/video_240p.mp4",
        "720p": "video/video_720p.mp4",
        "1440p": "video/video_1440p.mp4"
    }

    video_captures = {res: cv2.VideoCapture(path) for res, path in video_paths.items()}

    while True:
        try:
            for res, video_capture in video_captures.items():
                ret, frame = video_capture.read()
                if not ret:
                    video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, frame = video_capture.read()

                _, encoded_frame = cv2.imencode('.jpg', frame)
                frame_data = encoded_frame.tobytes()

                for client_socket in dict_client_socket.values():
                    broadcast(frame_data, client_socket)

        except Exception as e:
            print("Error occurred during video streaming:", e)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    localhost = "localhost"
    PORT = 12345
    server_socket.bind((localhost, PORT))
    server_socket.listen(5)
    print("Server is listening at port 12345...")

    while True:
        client_socket, addr = server_socket.accept()
        dict_client_socket.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
