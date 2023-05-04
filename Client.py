import socket
import threading
from tkinter import *

nickname = input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.17.18.1"
port = 14217
client.connect((host, port))

def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "NICK":
                client.send(nickname.encode("utf-8"))
            else:
                text_area.config(state=NORMAL)
                text_area.insert(END, message + "\n")
                text_area.config(state=DISABLED)
        except:
            print("An error occurred!")
            client.close()
            break

def write(event=None):
    message = f"{nickname}: {entry.get()}"
    entry.delete(0, END)
    client.send(message.encode("utf-8"))

def on_closing(event=None):
    client.close()
    root.quit()

# GUI
# Create the root window
root = Tk()
root.title("Chat Application")

# Set the color scheme
root.configure(bg='#333333')
text_color = '#FFFFFF'
button_color = '#0099CC'

# Create the chat history display
frame = Frame(root, bg='#444444')
scrollbar = Scrollbar(frame, bg='#444444', troughcolor='#444444')
text_area = Text(frame, wrap=WORD, yscrollcommand=scrollbar.set, state=DISABLED, bg='#444444', fg=text_color)
scrollbar.pack(side=RIGHT, fill=Y)
text_area.pack(side=LEFT, fill=BOTH, expand=True)
frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Create the message input field
entry = Entry(root, width=50, bg='#444444', fg=text_color)
entry.bind("<Return>", write)
entry.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

# Create the send button
send_button = Button(root, text="Send", command=write, bg=button_color, fg=text_color, font=('Arial', 16), padx=20, pady=10)
send_button.pack(side=RIGHT, padx=10, pady=10)

# Bind the window close event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the receive thread
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Start the main event loop
root.mainloop()