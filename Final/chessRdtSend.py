#!/usr/bin/python3

# Simple "RDT over UDP" protocol sender
# See rdt.py for the packet format

from socket import *
from rdt import *
from queue import SimpleQueue
import sys, json
import threading

class Sender:
    def __init__(self):
        self.data = []
        self.n_pkts = 0
        # Get receiver IP and port from command line arg. Default to localhost, port 12000
        self.receiverIP = '127.0.0.1'
        self.receiverPort = 12000
        try:
            self.receiverIP = sys.argv[1]
            self.receiverPort = int(sys.argv[2])
        except IndexError:
            pass
        self.commandQueue = SimpleQueue()
    def initializeSenderThread():
        senderThread = threading.Thread(target=startSendProgram)
        senderThread.daemon = True
        senderThread.start()
    def timeoutOccured(self):
        print("TIMEOUT ERROR. RETRANSMITTING")
        #Start new timer and retransmit all unACKed data, where base represents
        #start of window where data is not yet fully ACKed after it
        timer = newTimer()
        currIndex = base
    def makeNewLink(self,receiverIP, receiverPort):
        self.receiverIP = receiverIP
        self.receiverPort = receiverPort
    def sendRecvAddress(self,recvIP, recvPort):
        running = True
        self.data.append(recvIP)
        self.data.append(recvPort)
        self.n_pkts += 2
    
    def newTimer(self):
        #Must be global or else it running into issue of not actually cancelling after program stops
        global timer
        #try to cancel timer if one is running
        try:
            timer.cancel()
        except:
            pass
        timer = threading.Timer(timeoutInterval, timeoutOccured)
        #timer.daemon ensures the timer object is cancelled once program terminates
        timer.daemon = True
        timer.start(self)

    def sendData(self, pieceID, posx, posy):
        running = True
        self.data.append(pieceID)
        self.data.append(posx)
        self.data.append(posy)
        self.n_pkts += 3

    def shutdown(self):
        global running
        running = False

    def startSendProgram(self):
        running = False
        #Set instance variables:
            #global so that they can be altered within timeoutOccured()
        global currIndex, base
        timeoutInterval = 2
            #standard num of bits available for sequence number
        seqBitsAvailable = 4

        maxSeqNum = 3
        windowSize = maxSeqNum


        # Data to send: "We want to test this reliable data transfer protocol."
        #index of current data to be sent
        currIndex = 0

        # Initialize sender state
        base = 1
        nextseqnum = 0
        lastAckNum = 0
        timerRunning = False

        # Initialize timeout mechanism which uses threading.timer
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)

        print("Starting Transmission")
        while running:
            #If there are more packets to send and were still in the window size
            #while self.commandQueue.empty() == False:
                #runCommand(
                
            if (currIndex < self.n_pkts) & (currIndex < base+windowSize):
                # Get some data from the send buffer and make a packet
                packet = make_data_pkt(nextseqnum, data[currIndex])
                currIndex += 1
                print('\nSending ' + str(packet))
                nextseqnum += 1
                if(nextseqnum == maxSeqNum):
                    nextseqnum = 0

                # Send the packet using our underlying 'unreliable' transport
                # 'packet' must be a dict, as specified in the 'packet format' in rdt.py
                udt_send(clientSocket, packet, (receiverIP, receiverPort))
                if timerRunning == False:
                    newTimer()
                    timerRunning = True

            #Attempt to recieve ACK. Runs basically constantly, alongside the sending rather than in a
            #nested while loop like previously since it might take a while before we receive the ACK if one is lost
            packet, peer = rdt_rcv(clientSocket)
            # We have received an ACK packet
            # Set base (representing the index ACKed up until base) 
            print('Received ' + str(packet))
            if notcorrupt(packet):
                currAckNum = getSeqNum(packet)+1
                #If currAckNum < lastAckNum, then max seq num must have been reached so we can
                #find the amount of ACKed packets this indicates with some simply arithmetic.
                #Otherwise, seq num hasnt been reset so the number of ACKed packets is just the
                #difference between currAckNum and lastAckNum
                if(currAckNum < lastAckNum):
                    base = base + (currAckNum+(maxSeqNum-1) - lastAckNum)
                else:
                    base = base + (currAckNum - lastAckNum)
                lastAckNum = currAckNum
                if(base == n_pkts):
                    timer.cancel()
                    timerRunning = False
            else:
                print('RECEIVED CORRUPT ACK')
                
        #All data sent. close everything down
        try:
            timer.cancel()
        except:
            pass
        clientSocket.close()

