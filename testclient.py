import socket

testserver_ip = "127.0.0.1"
testserver_port = 5005

my_port = 5006

my_id = 1
my_type = 1

sock = None

def main():
    print("starting...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.bind(('', my_port)) # specify UDP_IP or INADDR_ANY
    
    data = bytearray(b'\x46\x53\x00\x00\x00') # ping
    data[2] = my_type
    data[3] = my_id
    sock.sendto(data, (testserver_ip, testserver_port ))
    
    udpdata, addr = sock.recvfrom(4096) # buffer size is 1024 bytes
    print("received: "+str(len(udpdata))+" bytes: "+str(udpdata)+" from: "+str(addr))
    
main()
