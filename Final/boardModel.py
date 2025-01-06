import pygame
from chessRdtSend import *

main_image_path = "C:\\Users\\dunca\\Downloads\\4911-Project-Images\\"
pieceDictionary = {}
sender = Sender()
sender.initializeSenderThread

class Piece:
    global pieceDictionary
    def initialize(self, startX, startY, player):
        self.value = None
        self.cost = None
        self.piece_type = None
        self.x = startX
        self.y = startY
        self.loyalty = player
        self.id = None
    def move(self, desiredX, desiredY, board):
        print("attempted: "+str(desiredX)+ " " + str(desiredY) + "\nfrom:")
        print(self.possible_moves(board))
        if(desiredX, desiredY) in self.possible_moves(board):
            board.move_piece(self.x, self.y, desiredX, desiredY)
            self.x = desiredX
            self.y = desiredY
        else:
            raise ValueError("Invalid move")
    def possible_moves(self, board):
        raise NotImplementedError
    def get_loyalty(self):
        return self.loyalty
    def get_type(self):
        return self.piece_type
    def get_image(self):
        imp = pygame.image.load(main_image_path + ("w" if self.get_loyalty() == "white" else "b") + self.piece_type + ".png")
        return imp
    def getID(self):
        return self.id
        
    

class Pawn(Piece):
    def initialize(self, startX, startY, player):
        super().initialize(startX, startY, player)
        self.value = 1
        self.cost = 1
        self.piece_type = "pawn"
        try:
            index = pieceDictionary[self.piece_type]
        except:
            index = 1
            pieceDictionary[self.piece_type] = 1
        self.id = self.loyalty+self.piece_type+str(index)
        pieceDictionary[self.id] = (startX, startY)
        self.hasMoved = False

    def possible_moves(self, board):
        moves = []
        direction = -1 if self.loyalty == "white" else 1
        # Forward move
        if board.is_empty(self.x, self.y + direction):
            moves.append((self.x, self.y + direction))
        if self.hasMoved == False:
            if board.is_empty(self.x, self.y + 2*direction):
                moves.append((self.x, self.y + 2*direction))
        # Capture moves
        for dx in [-1, 1]:
            if(dx + self.x)>7 or (dx+self.x) < 0:
                continue
            currSquare = board.get_square(self.x + dx, self.y + direction)
            if(currSquare != None):
                if currSquare.get_loyalty() != self.get_loyalty():
                    print("capture: " + str(self.x) + " " + str(self.y))
                    moves.append((self.x + dx, self.y + direction))
        return moves

    def move(self, desiredX, desiredY, board):
        print("attempted: "+str(desiredX)+ " " + str(desiredY) + "\nfrom:")
        print(self.possible_moves(board))
        if(desiredX, desiredY) in self.possible_moves(board):
            board.move_piece(self.x, self.y, desiredX, desiredY)
            self.x = desiredX
            self.y = desiredY
            self.hasMoved = True
        else:
            raise ValueError("Invalid move")

class Rook(Piece):
    def initialize(self, startX, startY, player):
        super().initialize(startX, startY, player)
        self.value = 5
        self.cost = 5
        self.piece_type = "rook"
        try:
            index = pieceDictionary[self.piece_type]
        except:
            index = 1
            pieceDictionary[self.piece_type] = 1
        self.id = self.loyalty+self.piece_type+str(index)
        pieceDictionary[self.id] = (startX, startY)
        self.hasMoved = False

    def possible_moves(self, board):
        moves = []
        direction = [(0,1), (1,0), (0,-1), (-1,0)]
        for dx, dy in direction:
            x, y = self.x, self.y
            while True:
                x, y = x+dx, y+dy
                if x<0 or x>7 or y<0 or y>7:
                    break
                curr_square = board.get_square(x,y)
                if curr_square == None:
                    moves.append((x,y))
                else:
                    if(curr_square.get_loyalty() != self.get_loyalty()):
                        moves.append((x,y))
                    break
        return moves

    def move(self, desiredX, desiredY, board):
        print("attempted: "+str(desiredX)+ " " + str(desiredY) + "\nfrom:")
        print(self.possible_moves(board))
        if(desiredX, desiredY) in self.possible_moves(board):
            board.move_piece(self.x, self.y, desiredX, desiredY)
            self.x = desiredX
            self.y = desiredY
            self.hasMoved = True
        else:
            raise ValueError("Invalid move")

    def hasMoved(self):
        return self.hasMoved

    def updatePos(self, x, y):
        self.x = x
        self.y = y

class Bishop(Piece):
    def initialize(self, startX, startY, player):
        super().initialize(startX, startY, player)
        self.value = 3
        self.cost = 3
        self.piece_type = "bishop"
        try:
            index = pieceDictionary[self.piece_type]
        except:
            index = 1
            pieceDictionary[self.piece_type] = 1
        self.id = self.loyalty+self.piece_type+str(index)
        pieceDictionary[self.id] = (startX, startY)

    def possible_moves(self, board):
        moves = []
        direction = [(1,1), (1,-1), (-1,-1), (-1,1)]
        for dx, dy in direction:
            x, y = self.x, self.y
            while True:
                x, y = x+dx, y+dy
                if x<0 or x>7 or y<0 or y>7:
                    break
                curr_square = board.get_square(x,y)
                if curr_square == None:
                    moves.append((x,y))
                else:
                    if(curr_square.get_loyalty() != self.get_loyalty()):
                        moves.append((x,y))
                    break
        return moves


class Queen(Piece):
    def initialize(self, startX, startY, player):
        super().initialize(startX, startY, player)
        self.value = 9
        self.cost = 9
        self.piece_type = "queen"
        try:
            index = pieceDictionary[self.piece_type]
        except:
            index = 1
            pieceDictionary[self.piece_type] = 1
        self.id = self.loyalty+self.piece_type+str(index)
        pieceDictionary[self.id] = (startX, startY)

    def possible_moves(self, board):
        moves = []
        direction = [(1,1), (1,-1), (-1,-1), (-1,1), (0,1), (1,0), (0,-1), (-1,0)]
        for dx, dy in direction:
            x, y = self.x, self.y
            while True:
                x, y = x+dx, y+dy
                if x<0 or x>7 or y<0 or y>7:
                    break
                curr_square = board.get_square(x,y)
                if curr_square == None:
                    moves.append((x,y))
                else:
                    if(curr_square.get_loyalty() != self.get_loyalty()):
                        moves.append((x,y))
                    break
        return moves

class Knight(Piece):
    def initialize(self, startX, startY, player):
        super().initialize(startX, startY, player)
        self.value = 3
        self.cost = 3
        self.piece_type = "knight"
        try:
            index = pieceDictionary[self.piece_type]
        except:
            index = 1
            pieceDictionary[self.piece_type] = 1
        self.id = self.loyalty+self.piece_type+str(index)
        pieceDictionary[self.id] = (startX, startY)

    def possible_moves(self, board):
        moves = []
        direction = [(2,1), (2,-1), (1,-2), (1,2), (-1,2), (-1,-2), (-2,-1), (-2,1)]
        x, y = self.x, self.y
        for dx, dy in direction:
            newx, newy = x+dx, y+dy
            print("Checking: " + str(newx) + " " + str(newy) +" from direction: " + str(dx) + " " + str(dy))
            if newx<0 or newx>7 or newy<0 or newy>7:
                print("out of bounds")
                continue
            curr_square = board.get_square(newx,newy)
            if curr_square == None:
                print("empty. adding...")
                moves.append((newx,newy))
            else:
                if(curr_square.get_loyalty() != self.get_loyalty()):
                    print("occupied by opponent. adding...")
                    moves.append((newx,newy))
                continue
        return moves

class King(Piece):
    def initialize(self, startX, startY, player):
        super().initialize(startX, startY, player)
        self.value = 40
        self.cost = 40
        self.piece_type = "king"
        try:
            index = pieceDictionary[self.piece_type]
        except:
            index = 1
            pieceDictionary[self.piece_type] = 1
        self.id = self.loyalty+self.piece_type+str(index)
        pieceDictionary[self.id] = (startX, startY)
        self.hasMoved = False

    def possible_moves(self, board):
        moves = []
        direction = [(1,1), (1,0), (1,-1), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1)]
        x, y = self.x, self.y
        for dx, dy in direction:
            newx, newy = x+dx, y+dy
            if newx<0 or newx>7 or newy<0 or newy>7:
                continue
            curr_square = board.get_square(newx,newy)
            if curr_square == None:
                moves.append((newx,newy))
            else:
                if(curr_square.get_loyalty() != self.get_loyalty()):
                    moves.append((newx,newy))
                continue
        #check if can castle
        if self.hasMoved == False:
            direction = [-1,1]
            for dx in direction:
                newx = self.x
                while True:
                    newx = newx+dx
                    if newx<0 or newx >7:
                        print("out of bounds")
                        break
                    curr_square = board.get_square(newx,self.y)
                    if curr_square == None:
                        print("free square")
                        continue
                    elif curr_square.get_type() == "rook" and curr_square.hasMoved == False:
                        print("castling valid")
                        moves.append((self.x + dx*2,self.y))
                    break
        return moves

    def move(self, desiredX, desiredY, board):
        print("attempted: "+str(desiredX)+ " " + str(desiredY) + "\nfrom:")
        print(self.possible_moves(board))
        if(desiredX, desiredY) in self.possible_moves(board):
            #if castling
            if(desiredX - self.x) in [2,-2]:
                dx = (desiredX-self.x)/2
                if(dx == -1):
                    board.move_piece(self.x, self.y, 2, self.y)
                    board.move_piece(0,self.y, 3, self.y)
                    board.get_square(3, self.y).updatePos(3,self.y)
                else:
                    board.move_piece(self.x, self.y, 6, self.y)
                    board.move_piece(7,self.y, 5, self.y)
                    board.get_square(5, self.y).updatePos(5,self.y)
            else:
                board.move_piece(self.x, self.y, desiredX, desiredY)
            self.x = desiredX
            self.y = desiredY
            self.hasMoved = True
        else:
            raise ValueError("Invalid move")


class Board():
    global pieceDictionary
    def initialize(self):
        self.boardModel = [[None for _ in range(8)] for _ in range(8)]

    def initialize_board(self):
        for x in range(8):
            self.spawn_piece(Pawn(),x, 1, "black")
            self.spawn_piece(Pawn(),x, 6, "white")
        for x in [1, 6]:
            self.spawn_piece(Knight(),x, 0, "black")
            self.spawn_piece(Knight(),x, 7, "white")
        for x in [0, 7]:
            self.spawn_piece(Rook(),x, 0, "black")
            self.spawn_piece(Rook(),x, 7, "white")
        for x in [2, 5]:
            self.spawn_piece(Bishop(),x, 0, "black")
            self.spawn_piece(Bishop(),x, 7, "white")
        self.spawn_piece(Queen(),3, 0, "black")
        self.spawn_piece(King(),4, 0, "black")
        self.spawn_piece(Queen(),3, 7, "white")
        self.spawn_piece(King(),4, 7, "white")

    def get_square(self, x, y):
        return self.boardModel[x][y]

    def move_piece(self, prevX, prevY, nextX, nextY):
        piece = self.get_square(prevX,prevY)
        self.boardModel[prevX][prevY] = None
        otherSquare = self.get_square(nextX,nextY)
        if(otherSquare != None):
            del pieceDictionary[otherSquare.getID()]
        self.boardModel[nextX][nextY] = piece
        pieceDictionary[piece.getID()] = (nextX,nextY)
        self.send_networkMove(piece.getID(), nextX, nextY)
        

    def spawn_piece(self, Piece, x, y, loyalty):
        Piece.initialize(x,y,loyalty)
        self.get_board()[x][y] = Piece

    def is_empty(self, x, y):
        return self.boardModel[x][y] is None
    def get_board(self):
        return self.boardModel
    def make_networkMove(self, pieceID, posx, posy):
        piece = self.get_square(prevX,prevY)
        self.boardModel[prevX][prevY] = None
        otherSquare = self.get_square(nextX,nextY)
        if(otherSquare != None):
            del pieceDictionary[otherSquare.getID()]
        self.boardModel[nextX][nextY] = piece
        pieceDictionary[piece.getID] = (nextX,nextY)
    def send_networkMove(self, pieceID, posx, posy):
        sender.sendData(pieceID, posx, posy)
    def makeNewLink(recvIP, recvPort):
        sender.makeNewLink(recvIP, recvPort)
    def sendRecvAddress(self,recvIP, recvPort):
        sender.sendRecvAddress(recvIP, recvPort)
