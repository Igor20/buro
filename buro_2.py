import serial
import socket
import time


class COM():
    def __init__(self):
        self.port = COM5    #For Example
        self.baud = 115200  #For Example
        self.timeout = 3
        self.com = serial.Serial(port, baud, timeout=1)  #Serial port configuration

    def recv(size=100):
        tic = time.time()
        
        while time.time() - tic < self.timeout:
            out = self.com.read(size)
            return out.decode("ascii")

        print("Timeout in TCP")
        return "Timeout"

    def write(message):
        self.com.write(message)
    
    def close():
        self.com.close()


class TCP():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.timeout = 3
        self.port = 1001 #For Example
        self.host = 'localhost'     #For Example
        self.sock.connect(self.host, self.port)

    def write(message):
        self.sock.sendall(message)
        
    def recv(size=100):
        tic = time.time()
        
        while time.time() - tic < self.timeout:
            out = self.sock.recv(100)
            return out.decode("ascii")

        print("Timeout in TCP")
        return "Timeout"

    def close():
        self.sock.close()

        
def _print(out,req):
    if ref[req] == out:
        print('Received:',out)
    else:
        print('Something occurred wrong')

def operation(interfaces, ref):
    while True:
        interface = input() #Input type of interface
        request = input() #Input command
        

        if interface:
            if interface in interfaces.keys():
                interface = interfaces[interface]
            else:
                print("Write some interface 'serial' or 'tcp'")
                continue
        
        if request == 'exit':
            interface.close()
            exit()

        elif request in ref.keys():
            interface.write(request.encode("utf-8"))
            output = interface.recv()
            _print(output, request)
            
        else:
            print(r'Sorry it support only the commands: {ref.keys()}')


if __name__ == "__main__":
    interfaces = {"serial":COM(),"tcp":TCP()}   #Interface's objects
    ref = {"GET_A":"A_10V","GET_B":"B_5V","GET_C":"C_15A"}  #Reference data

    operation(interfaces, ref)  #Operation in terminal
        
