from queue import SimpleQueue
from rdt import *
from socket import *
import sys, json

PORT = 12000

#Initialize variables
#We'll assume 4 bytes as is standard according to google

# Listen for UDP datagrams on port# PORT
# SO_REUSEADDR eliminates "port already in use" errors
recvSock = socket(AF_INET, SOCK_DGRAM)
recvSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
recvSock.bind(('', PORT))

# Initialize receiver state
waitingForConnection = SimpleQueue()
maxSeqNum = 2
expectedseqnum = 1
sndpkt = make_ack_pkt(0)
currData = [0 for i in range(2)]

# Run forever, processing received UDP datagrams
while True:

    if(waitingForConnection.qsize() > 1):
        ip1, port1 = waitingForConnection.get()
        ip2, port2 = waitingForConnection.get()
        packet10 = make_data_pkt(0, "MakeNewLink")
        packet11 = make_data_pkt(1, ip1)
        packet12 = make_data_pkt(2, port1)
        packet20 = make_data_pkt(0, "MakeNewLink")
        packet21 = make_data_pkt(1, ip1)
        packet22 = make_data_pkt(2, port1) 
        udt_send(clientSocket, packet10, (ip2, port2))
        udt_send(clientSocket, packet11, (ip2, port2))
        udt_send(clientSocket, packet12, (ip2, port2))
        udt_send(clientSocket, packet20, (ip1, port1))
        udt_send(clientSocket, packet21, (ip1, port1))
        udt_send(clientSocket, packet22, (ip1, port1))
        
    # Receive a packet. rdt_recv() returns a Python dict,
    # as defined in 'packet format' in rdt.py
    packet, peer = rdt_rcv(recvSock)
    print('\nReceived ' + str(packet))

    # if packet is not corrupt and has expected seqnum
    #     extract data and deliver to application layer
    #     send ACK for expectedseqnum
    # else
    #     send last ack packet

    # sequence number of 0 is only used on the FIRST packet recieved, indicating
    # a new sequence of data is being sent, so this receiver should reset its expected
    # sequence number to match it. getSeqNum is what was previously getAckNum, just better
    # named to something better which makes sense for use with receiver as well
    if getSeqNum(packet) == 0:
        expectedseqnum = 0

    if notcorrupt(packet) and hasseqnum(packet, expectedseqnum):

        # 'deliver to application  layer' means print it on the screen
        data = extract_data(packet)
        print('DELIVERED TO APP: ' + str(data))

        # Send an ACK for this newly-arrived packet
        sndpkt = make_ack_pkt(expectedseqnum)
        currData[expectedseqnum] = data
        expectedseqnum +=1
        #Ensure expected sequence number is within range of maxSeqNum
        if(expectedseqnum == maxSeqNum):
            waitingForConnection.add(currData[0], currData[1])
            expectedseqnum = 0
        udt_send(recvSock, sndpkt, peer)
        print('Sending ' + str(sndpkt))
        
    else:
        # Send the last ACK
        print("RECEIVED CORRUPT PACKET OR WRONG SEQNUM!")
        udt_send(recvSock, sndpkt, peer)
        print('Sending ' + str(sndpkt))
