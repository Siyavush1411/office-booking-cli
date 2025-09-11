import socket
import ssl
import base64

HOST = "smtp.gmail.com"
PORT = 587
USERNAME = "siyavushmirzaev375@gmail.com"
PASSWORD = ""


def send_cmd(sock, cmd):
    sock.send((cmd + "\r\n").encode())
    return sock.recv(1024).decode()


def send_email(to, subject, body):
    FROM = USERNAME

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.recv(1024)

    send_cmd(s, "EHLO localhost")
    send_cmd(s, "STARTTLS")

    context = ssl.create_default_context()
    s = context.wrap_socket(s, server_hostname=HOST)
    send_cmd(s, "EHLO localhost")

    b64_user = base64.b64encode(USERNAME.encode()).decode()
    b64_pass = base64.b64encode(PASSWORD.encode()).decode()
    send_cmd(s, "AUTH LOGIN")
    send_cmd(s, b64_user)
    send_cmd(s, b64_pass)

    send_cmd(s, f"MAIL FROM:<{FROM}>")
    send_cmd(s, f"RCPT TO:<{to}>")

    send_cmd(s, "DATA")

    encoded_subject = base64.b64encode(subject.encode("utf-8")).decode()
    s.send(f"Subject: =?utf-8?B?{encoded_subject}?=\r\n".encode())
    s.send(f"From: {FROM}\r\n".encode())
    s.send(f"To: {to}\r\n".encode())
    s.send("Content-Type: text/plain; charset=utf-8\r\n".encode())
    s.send("\r\n".encode())
    s.send(body.encode("utf-8"))
    s.send("\r\n.\r\n".encode())

    send_cmd(s, "QUIT")
    s.close()
