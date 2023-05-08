import socket
import threading
from tkinter import *


def login():
    global username, login_button, login_screen

    # Create login screen
    login_screen = Tk()
    login_screen.title("Login")
    login_screen.configure(bg='#333333')  # Set background color

    # Create input field for username
    login_screen.geometry("400x300")
    login_label = Label(login_screen, text="Username:", bg='#333333', fg='#FFFFFF', font=('Arial', 14) )
    login_label.place(relx=0.5, rely=0.35, anchor=CENTER)  # Center the label
    username = Entry(login_screen, width=20, font=('Arial', 12))  # Set width and font size
    username.place(relx=0.5, rely=0.47, anchor=CENTER)  # Center the entry field and adjust vertical position

    # Create login button
    login_button = Button(login_screen, text="Login", bg='#0099CC', fg='#FFFFFF', command=start_chat, font=('Arial', 12), width=10, height=1)  # Set font size, width and height
    login_button.place(relx=0.5, rely=0.6, anchor=CENTER)  # Center the button

    # Bind 'Return' key to login button
    login_screen.bind("<Return>", lambda event: login_button.invoke())

    login_screen.mainloop()



def start_chat():
    global username, login_button, login_screen, client, text_area, entry, root

    # Get username from input field
    username = username.get()

    # Close login screen and create chat screen
    login_screen.destroy()
    root = Tk()
    root.title("Chat Application")
    root.configure(bg='#333333')  # Set background color

    # Create chat UI
    frame = Frame(root)
    scrollbar = Scrollbar(frame)
    text_area = Text(frame, wrap=WORD, yscrollcommand=scrollbar.set, state=DISABLED, bg='#333333', fg='#FFFFFF', font=('Arial', 12))
    scrollbar.pack(side=RIGHT, fill=Y)
    text_area.pack(side=LEFT, fill=BOTH, expand=True)
    frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    entry = Entry(root, width=40, bg='#FFFFFF', fg='#000000', font=('Arial', 12))
    entry.bind("<Return>", write)
    entry.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

    #  bg=button_color  fg=text_color
    send_button = Button(root, text="Send", bg='#0099CC', fg='#FFFFFF', command=write, font=('Arial', 12), padx=15, pady=5)
    send_button.pack(side=RIGHT, fill=BOTH, padx=10, pady=10)

    # Connect to server
    # socket.AF_INET, this case to use IPv4
    # socket.SOCK_STREAM, this to use TCP socket
    # socket.SOCK_DGRAM, this to use UDP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = "192.168.56.1"
    port = 14217
    client.connect((host, port))

    # Bind closing event to on_closing function
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Start receiving messages in a thread
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    # Send username to server
    # client.send(username.encode("utf-8"))

    root.mainloop()



def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "USER":
                client.send(username.encode("utf-8"))
            else:
                text_area.config(state=NORMAL)
                text_area.insert(END, message + "\n")
                text_area.config(state=DISABLED)
        except:
            print("An error occurred!")
            client.close()
            break

def write(event=None):
    message = f"{username}: {entry.get()}"
    entry.delete(0, END)
    client.send(message.encode("utf-8"))

def on_closing(event=None):
    client.close()
    root.quit()


login()
