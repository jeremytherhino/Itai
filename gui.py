import sys
import socket
import threading
import time
import uuid
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QTextEdit, QPushButton, QLabel, QMessageBox

from firebaseRTDB import create_document
# from firestoreCRUD import FirestoreManager
from test import register_user, check_user_exists


class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 300)

        # Email Input
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter email")
        self.email_input.setGeometry(100, 50, 200, 40)
        self.email_input.setText(f"d@a.com")

        # Password Input
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setGeometry(100, 100, 200, 40)
        self.password_input.setText(f"123456")

        # Register Button
        self.register_button = QPushButton('Register', self)
        self.register_button.setGeometry(100, 150, 200, 40)
        self.register_button.clicked.connect(self.register_user)

        # Login Button
        self.login_button = QPushButton('Login', self)
        self.login_button.setGeometry(100, 200, 200, 40)
        self.login_button.clicked.connect(self.login_user)

    def register_user(self):
        email = self.email_input.text()
        password = self.password_input.text()
        if register_user(email, password):
            QMessageBox.information(self, "Success", "User registered successfully!")
        else:
            QMessageBox.critical(self, "Error", "Failed to register user")

    def login_user(self):
        email = self.email_input.text()
        password = self.password_input.text()
        if check_user_exists(email, password):
            self.open_chat_window(email)
        else:
            QMessageBox.critical(self, "Error", "Invalid email or password")

    def open_chat_window(self, user_email):
        self.chat_window = ChatWindow(user_email)
        self.chat_window.show()
        self.close()


class ChatWindow(QMainWindow):
    def __init__(self, user_email):
        super(ChatWindow, self).__init__()
        self.user_email = user_email  # Store user email
        self.client_email = ""
        self.server_socket = None
        # self.firestore = FirestoreManager()  # Initialize FirestoreManager
        # self.chat_id = str(uuid.uuid4())  # Unique ID for this chat session
        self.initUI()
        self.init_chat()
        self.client_socket = None
        self.send_socket = None

    def initUI(self):
        self.setWindowTitle(f"P2P Chat - {self.user_email}")
        self.setGeometry(100, 100, 600, 440)

        # Display Server IP
        self.ip_label = QLabel(self)
        self.ip_label.setText(f"Your IP: 127.0.0.1")
        self.ip_label.setGeometry(20, 390, 200, 20)

        # Display Server Port
        self.port_label = QLabel(self)
        self.port_label.setText(f"Your Port: 12345")
        self.port_label.setGeometry(230, 390, 200, 20)

        # IP Address Input
        self.ip_input = QLineEdit(self)
        self.ip_input.setPlaceholderText("Enter IP address")
        self.ip_input.setGeometry(20, 10, 200, 40)
        self.ip_input.setText("127.0.0.1")

        # Port Input
        self.port_input = QLineEdit(self)
        self.port_input.setPlaceholderText("Enter Port")
        self.port_input.setGeometry(230, 10, 100, 40)
        self.port_input.setText("12346")

        # Connect Button
        self.connect_button = QPushButton('Connect', self)
        self.connect_button.setGeometry(340, 10, 100, 40)
        self.connect_button.clicked.connect(self.connect_to_peer)

        # Disconnect Button
        self.connect_button = QPushButton('Disonnect', self)
        self.connect_button.setGeometry(450, 10, 100, 40)
        self.connect_button.clicked.connect(self.disconnect)

        # Chat Display
        self.chat_display = QTextEdit(self)
        self.chat_display.setGeometry(20, 60, 560, 270)
        self.chat_display.setReadOnly(True)

        # Message Input
        self.message_input = QLineEdit(self)
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.setGeometry(20, 340, 450, 40)

        # Send Button
        self.send_button = QPushButton('Send', self)
        self.send_button.setGeometry(480, 340, 100, 40)
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setEnabled(False)

    def init_chat(self):
        # Initialize server socket for listening to incoming connections
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('0.0.0.0', 12345)
        self.server_socket.bind(server_address)
        self.server_socket.listen()
        print("Listening on port 12345")
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        while True:
            self.client_socket, addr = self.server_socket.accept()
            self.client_socket.send(self.user_email.encode())
            print(addr, "is connected")
            threading.Thread(target=self.listen_for_messages,  daemon=True).start()

    def listen_for_messages(self):
        while True:
            msg = self.client_socket.recv(1024)
            if msg:
                decoded_msg = msg.decode()
                self.chat_display.append(decoded_msg)
                # data = "{'from': "+self.client_email +", 'to':"+ self.user_email +", 'msg'+"+decoded_msg+"}"
                
                data = {
                    'from': self.client_email,
                    'to': self.user_email,
                    'msg': decoded_msg
                }
                create_document("messages", data)
                # self.save_message_to_firebase(decoded_msg, self.client_email,self.user_email)

    def connect_to_peer(self):
        ip = self.ip_input.text()
        port = int(self.port_input.text())
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.send_socket.connect((ip, port))
            print("server port:", self.send_socket.getsockname()[1])
            self.client_email = self.send_socket.recv(1024).decode()
            self.load_chat_history()  # Load chat history when the app starts
            self.send_button.setEnabled(True)


        except Exception as e:
            print(f"Error connecting to peer: {e}")

    def send_message(self):
        message = self.message_input.text()
        if message:  # Check if the message is not empty
            try:
                if self.send_socket:  # Check if the client socket is initialized
                    self.send_socket.sendall(message.encode('utf-8'))
                    self.chat_display.append(f"You: {message}")  # Display the sent message in the chat
                    self.message_input.clear()  # Clear the message input field
                    data = {
                        'from': self.user_email,
                        'to': self.client_email,
                        'msg': message
                    }                    
                    create_document("messages", data)
                    # self.save_message_to_firebase(self.user_email+":"+message, self.user_email,self.client_email)
            except Exception as e:
                self.chat_display.append(f"Failed to send message: {str(e)}")

    def disconnect(self):
        self.client_socket.close()
        self.server_socket.close()
        self.send_socket.close()
    
    def load_chat_history(self):
        None
        # # Load chat history from Firebase
        # messages = self.firestore.get_all_data("chats")
        # print(messages)
        # for doc_id, data in sorted(messages.items(), key=lambda x: x[0]):
        #     if data.get("sender") == self.user_email:
        #         self.chat_display.append(f"You: {data.get('message')}")
        #     else:
        #         self.chat_display.append(data.get('message'))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
