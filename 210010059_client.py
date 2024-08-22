import socket
import threading 
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import cv2
from pathlib import Path

def list_items_in_folder(folder_path):
    folder = Path(folder_path)
    items = [item.name for item in folder.iterdir()]
    return items

dict_client = {}

key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

def client_receiver_thread():
    global dict_client
    try:
        while True:
            data = client_socket.recv(4096)
            try:
                new_dict_client = json.loads(data.decode())
                dict_client = {i: j for i, j in new_dict_client.items()}
                
            except:
                msg = decryptMessage(data, private_key)
                if msg != "":
                    print(f"\nMessage accepted from {msg}\n")
            print("Number of Clients connected: ", len(dict_client))
    except:
        pass
    
def encryptMessage(message, public_key, client_name):
    cipher = PKCS1_OAEP.new(public_key)
    message = client_name + ": " + message
    encrypted_message = cipher.encrypt(message.encode())
    return encrypted_message

def decryptMessage(encrypted_message, private_key):
    try:
        cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
        decrypted_message = cipher.decrypt(encrypted_message)
        return decrypted_message.decode()
    except:
        return ""

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
locahost = "localhost"
PORT = 12345
client_socket.connect((locahost, PORT))

name = input("Enter your name:")
global myname
myname = name
client_socket.send(name.encode())
client_socket.send(public_key)
print("\n",public_key,"\n")

threading.Thread(target=client_receiver_thread).start()

while True:
    try:
        
        print("Commands\n")
        print("Enter client name to whom you have to message for ex. john\n")
        print("To quit the connection enter 'QUIT'\n")
        print("To list available videos enter 'LIST'\n")
        print("Which video to play. Please enter video name as 'VIDEO_1'. to terminate a video forcefully press 'q'\n")

        alias = input()
        if alias.lower() == 'quit':
            client_socket.send(alias.encode())
            break
        if alias.lower() == "list":
            folder_path = "./video"
            items = list_items_in_folder(folder_path)
            print("Available videos:")
            for item in items:
                print(item)            
            continue
        if "VIDEO" in alias:
            if alias == "VIDEO_1":
                video_240p = cv2.VideoCapture(f"video/{alias}_240p.mp4")
                video_720p = cv2.VideoCapture(f"video/{alias}_720p.mp4")
                video_1440p = cv2.VideoCapture(f"video/{alias}_1440p.mp4")

                total_frames = int(video_1440p.get(cv2.CAP_PROP_FRAME_COUNT))

                one_third = total_frames // 3
                print(total_frames)
                for i in range(3):
                    for _ in range(one_third):
                        ret1, frame1 = video_240p.read()
                        ret2, frame2 = video_720p.read()
                        ret3, frame3 = video_1440p.read()
                        if i==0:
                            frame = frame1
                        if i==1:
                            frame = frame2
                        if i==2:
                            frame = frame3
                        frame = cv2.resize(frame, (600, 400))
                        cv2.imshow(f"Video sent by server for {name}", frame)
                        if cv2.waitKey(25) & 0xFF == ord('q'):
                            break
                cv2.destroyAllWindows()
            else: 
                print("Invalid Video File.")
            continue
        message = input("Enter your message:")
        print("Available clients")
        for key in dict_client.keys():
            print(key)
        if alias in dict_client:
            print("Recipient found!")
            encrypted_message = encryptMessage(message, RSA.import_key(dict_client[alias]), myname)
            client_socket.send(encrypted_message)
        else:
            print("Recipient not found!")

    except:
        break

client_socket.close()