#Server.py
import socket
import sys
import struct

finalMsg = []
AckNum1 = 0
SeqNum1 = 0


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", 19990))


def send(c,num):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ss = struct.pack("!50si",c.encode(),num)
    s.sendto(ss,("127.0.0.1",19991))
    s.close()


def recv():
    global server_socket
    data, addr = server_socket.recvfrom(1024)
    str,num = struct.unpack("!50si",data)
    str = str.decode("utf-8").replace("\0","")
    return str,num


while True: 
    str,num = recv()
    if num == 1: #the flag sent by client side
        print("Path establishment... Received: SYN, Flag Number: 1")
        print("Path establishment... Sending: SYN-ACK, Flag Number: 2")
    if num == 3:
        print("Path establishment... Received: ACK, Flag Number: 3")
        print("Ready to receive payload.")
    num = num + 1    #server has number plus 1, this number simulates sequnce number. sequence number means you send out package with number one1, receiver will send back ACK which is #2/package 2
    str = chr(ord(str)+1)
    send(str,num)
    if str == "d":
        break

while True:
    str,SeqNum = recv() #first packet of data received 
    if str == "FIN":
        print("Received FIN flag. Sending FYN-ACK.")
        break
    print("Received: %s, Sequence Number: %d" % (str, SeqNum))
    print("Preparing Acknowledgement message number")
    if SeqNum1 != SeqNum:  #checking if sequence number sent by client is whats expected
        warning = "Package lost"
        send(warning,AckNum1) #send client message that packet was lost, sends ACK number
        print("Sending: %s, Acknowledgement Number: %d" % (warning, AckNum1))
    else:
        warning = "ACK"
        send(warning,AckNum1) #send client ACK message and ack number
        print("Sending: %s, Acknowledgement Number: %d" % (warning, AckNum1))
        print(" ")
        finalMsg.append(str)
        SeqNum1 = SeqNum1 + 1  #increase expected sequence number
        AckNum1 = AckNum1 + 1  #increase ACK number


server_socket.close()
print(finalMsg[0:SeqNum1])
print("I love Fordham University in the New York City.")
