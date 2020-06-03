#Client.py
import socket
import sys
import struct


SeqNum = 0 #Sequence number for client to keep track of
AckNum = 0 #Acknowledgement Number for client to keep track of
window = 1 #window size starts at 1
i = 0


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", 19991))


def send(c,num):  #c is data, num is sequence num/header/flag (SYN, SYN-ACK, ACK, FIN, FIN-ACK), for first 3 numbers. After first 3 numbers its just sequence number
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ss = struct.pack("!50si",c.encode(),num)
    s.sendto(ss,("127.0.0.1",19990))
    s.close()
    #print("Send:%s,%d" % (c,num))

def recv():
    global server_socket
    data, addr = server_socket.recvfrom(1024)
    str,num = struct.unpack("!50si",data)
    str = str.decode("utf-8").replace("\0","")
    #print("Receive:%s,num:%d" % (str,num))
    return str,num
    
str = "a"
num = 1
while True:
    if num == 1: #this is the flag number
        print("Path establishment... Sending: SYN, Flag Number: 1")
    send(str, num)
    str,num  = recv()
    if num == 2:
        print("Path establishment... Recveived: SYN-ACK, Flag Number: 2")
        print("Path establishment... Sending: ACK, Flag Number: 3")
    if str == "d":
        break
    str = chr(ord(str)+1)
    num = num + 1

message = "I love Fordham University in the New York City."
str = message

while i < len(str): #index over the entire message. While i is less than length of the message
    while window < 4: #this is congestion control and shows additive increase
        send(str[i:i+window], SeqNum) #send chars starting from i index to the size of the window
        print("Sending: %s, Sequence Number: %d" % (str[i:i+window], SeqNum))
        warning,AckNum1 = recv()  #receive Acknowledgement
        print("Received: %s, Acknowledgement Number: %d" % (warning, AckNum1))
        print(" ")
        if AckNum != AckNum1:  #compare ACK numbers to determine if package was lost
            print("Sending packet again")  #packet was lost so send again
            send(str[i:i+window], SeqNum)
        else:
            print("Correct Acknowledgement Number received")
            SeqNum = SeqNum + 1  #increase sequence number by 1
            AckNum = AckNum + 1  #increase ACK number by 1
            window = window + 1  #increase window, when the window reaches 4 this loop will end and we will increase i

    send(str[i:i+window], SeqNum) #now sending 4 chars at a time. Window stays at 4
    print("Sending: %s, Sequence Number: %d" % (str[i:i+window], SeqNum))
    warning,AckNum1 = recv()
    print("Received: %s, Acknowledgement Number: %d" % (warning, AckNum1))
    print(" ")
    if AckNum != AckNum1:  #compare ACK numbers to determine if package was lost
        print("Sending packet again")   #packet was lost so send again
        send(str[i:i+window], SeqNum)
    else:
        print("Correct Acknowledgement Number received")
        SeqNum = SeqNum + 1  #increase sequence number by 1
        AckNum = AckNum + 1  #increase ACK number by 1
        i = i + 1  #increase i to slide window

print("End of message, sending FIN flag")
finFlag = "FIN"
send(finFlag, SeqNum)
print("Recieved FIN-ACK from server, closing connection")
server_socket.close()
print(message)


"""
THESE ARE MY NOTES

#when we established connectiont there is no data
#1 is SYN 2 is SYNACK 3 = ACK ...etc. c/data intially can just be "path establishment"
Server responds: "The message type is path establishment" num=2
Then sender replies with ACK. The data type is path establishment. This will be 3rd message in path establishment.
#Similar to Lab1. if data rquals hello fordham then...
Then sender needs to send out actual payload ("I love Fordham University in the New York City.")
Want to set window size to 4 (4 char including space). First package is "I lo", this is window to send
The chars will be sent individually, byte by byte. 1st byte we send is "I". Wait until we
get ACK to send next byte. Send out 4 bytes, recieve 4 ACK. When sender/client sends out last byte (".")
then we need to tear down the connection by sending out a FIN message, then the server will respond with FIN-ACK 
then the connection is done. once done we need to print out message on both sides.
The base code sends messages "a" "b" "c" "d" back and forth... we need to change these indicators
First 3 messagaes are for path establishment. change "a" to "Path establishment" then server checks 
using if statement if the message is correct and if sequence number is 1 2 or 3. if its 1 server
needs to replay with SYN-ACK 
At the end change the strings to "path closure" or "FIN" just some indicator name, 
then "FIN-ACK". The seq numbers for the last 2 are (1 or 2 maybe)

The characters we send will be a data structure we design and then print them all out at the end
this is what we did in Lab 1


Can print out "waiting for ACK"

Want window size to be 4, 4 chars. Message to send is "I love fordham or something"
space counts as a package, one space, window size is 4. so first package is "I lo". 
send then haave to wait until get ACK. when we do we need to send another byte/one char
last byte will be period"." When done we need to print out the whole message on both sides.
first 3 messages are for path establishment. If data=a and num=1.
need to change a to path establishment.
on server side need to decide if "a" is path establishment. 
change string to indicator that you want.
1 is FIN 2 is FINACK
at end need to print out closed and actually close connection then have both sides print out message
want to print out message char by char at end

if else.. not passed estanlishment and passed closure.
if else
"""


