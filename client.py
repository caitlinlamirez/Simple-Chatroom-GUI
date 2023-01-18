import socket 
from threading import *
from tkinter.constants import END
from tkinter.font import Font
import customtkinter
from tkinter import *
from PIL import Image
import time
from customtkinter.windows.ctk_toplevel import CTkToplevel
from customtkinter.windows.widgets.ctk_label import CTkLabel
from customtkinter.windows.widgets.image.ctk_image import CTkImage

# Define constants
PORT = 10000
SERVER = "localhost" 
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
JOIN_MSG = "!JOINED"
BYTE_SIZE = 1024

# Client's socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(ADDR)

# Sets GUI theme to dark

customtkinter.set_appearance_mode("dark")
class GUI:

    def __init__(self, window):
        # Create the window
        self.window = window
        self.window.geometry("460x475") # width x length
        self.window.title("Chat Room")

        self.login_frame()
        self.recvThread = Thread(target=self.recvMessage)
        self.recvThread.daemon = True
        self.recvThread.start()


        self.window.mainloop()


    def login_frame(self):
        # Frame
        self.loginFrame = customtkinter.CTkFrame(self.window)
        self.loginFrame.pack(pady=20, padx = 70, fill="both", expand=True)

        # Title Label
        titleLbl = customtkinter.CTkLabel(master=self.loginFrame, text="Welcome to the Chat Room", font=("Calibri", 25, "bold"))
        titleLbl.pack(pady=15, padx=10)

        # Image
        self.chatImg = customtkinter.CTkImage(dark_image=Image.open("chat.png"), size = (235,220))
        self.chatImgLbl = customtkinter.CTkLabel(master=self.loginFrame, image = self.chatImg, text="")
        self.chatImgLbl.pack(pady=15)

        # Instructions
        instructLbl = customtkinter.CTkLabel(master=self.loginFrame, text="Before you enter, please enter a nickname", font=("Arial", 12))
        instructLbl.pack(pady=5, padx=10)
        
        # Nickname entry
        self.nicknameEntry = customtkinter.CTkEntry(self.loginFrame, placeholder_text = "Nickname")
        self.nicknameEntry.pack(pady=5, padx=10)

        # Enter button
        button = customtkinter.CTkButton(self.loginFrame, text="Enter", command=self.login, fg_color="#5B1A8D")
        button.pack(pady=5, padx=10)

    def chatroom_frame(self):
        # Frame
        self.chatFrame = customtkinter.CTkFrame(self.window)
        self.chatFrame.pack(pady=20, padx = 70, fill="both", expand=True)

        # Title label
        titleLbl = customtkinter.CTkLabel(master=self.chatFrame, text="Chat Room", font=("Calibri", 18, "bold"))
        titleLbl.pack(pady=1, padx=10)

        # Messages Box
        self.messagesBox = customtkinter.CTkTextbox(self.chatFrame, width=345, height=300, activate_scrollbars=True)
        self.messagesBox.pack(pady=5, padx=10)
        self.messagesBox.configure(state='disabled')

        # Message entry
        self.messageEntry = customtkinter.CTkEntry(self.chatFrame, width=345, height=30, placeholder_text="Enter your message", font=("Calibri", 12,))
        self.messageEntry.pack(pady=10, padx=10)

        # Send message button
        send_button= customtkinter.CTkButton(self.chatFrame, text="Enter", command=self.sendMessage, fg_color="#5B1A8D")
        send_button.pack(pady=5, padx=10)


    # Sends message to server
    def sendToServer(self, client, msg):
        message = msg.encode(FORMAT)
        client.send(message)


    # Event when send message button is clicked
    def sendMessage(self):
        # Get entry
        clientMsg = self.messageEntry.get()
        
        # Clear entry
        self.messageEntry.delete(0, END)
        self.messagesBox.configure(state='normal')
        self.messagesBox.insert(END, f"{self.nickname} (you): {clientMsg}\n")
        self.messagesBox.configure(state='disabled')
        
        clientSocket.send(clientMsg.encode(FORMAT))


    # Receives messages
    def recvMessage(self):
        try: 
            while True:
                # Receive message from server
                serverMsg = clientSocket.recv(1024).decode(FORMAT)

                # Insert it into text box
                self.messagesBox.configure(state='normal')
                self.messagesBox.insert(END, serverMsg + "\n")
                self.messagesBox.configure(state='disabled')
        except:
            self.sendToServer(clientSocket, DISCONNECT_MSG)
        


    def login(self):
        # Get user's nickname
        self.nickname = self.nicknameEntry.get()
        # Clear entry
        self.nicknameEntry.delete(0, END)

        # Send nickname to server
        self.sendToServer(clientSocket, self.nickname)

        # Forget the login frame
        self.loginFrame.forget()

        # Chatroom frame
        self.chatroom_frame()

        # Send join message to server
        self.sendToServer(clientSocket, JOIN_MSG)
        
      
def page():
    window = customtkinter.CTk()
    GUI(window)
    window.mainloop()
        

if __name__ == '__main__':
    page()