#!/usr/bin/python3

# "RDT over UDP" protocol receiver
# See rdt.py for the packet format

from socket import *
from rdt import *
from boardModel import *
import json

def getRecvBoard(Board):
    global board
    board = Board

PORT = 12000

#Initialize variables
#We'll assume 4 bytes as is standard according to google
seqBitsAvailable = 4
maxSeqNum = 3

# Listen for UDP datagrams on port# PORT
# SO_REUSEADDR eliminates "port already in use" errors
recvSock = socket(AF_INET, SOCK_DGRAM)
recvSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
recvSock.bind(('', PORT))

# Initialize receiver state
expectedseqnum = 1
sndpkt = make_ack_pkt(0)
currMoveData = [0 for i in range(3)]

# Run forever, processing received UDP datagrams
while True:

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
        currMoveData[expectedseqnum] = data
        expectedseqnum +=1
        #Ensure expected sequence number is within range of maxSeqNum
        if(expectedseqnum == maxSeqNum):
            board.make_networkMove(currMoveData[0],currMoveData[1],currMoveData[2])
        udt_send(recvSock, sndpkt, peer)
        print('Sending ' + str(sndpkt))
        
    else:
        # Send the last ACK
        print("RECEIVED CORRUPT PACKET OR WRONG SEQNUM!")
        udt_send(recvSock, sndpkt, peer)
        print('Sending ' + str(sndpkt))
