import pygame
from boardModel import *

# Initialize Pygame and the font module
pygame.init()
pygame.font.init()


#BOARD
board = Board()
board.initialize()
board.initialize_board()


# Set up the display
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Define font for button labels
font = pygame.font.SysFont('Arial', 24)

# List to store button objects
buttonboard = [[None for _ in range(8)] for _ in range(8)]

#button class from: https://thepythoncode.com/article/make-a-button-using-pygame-in-python
class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        global objects  # Ensure we're modifying the global list
        self.xPos = x*screen_width/8
        self.yPos = y*screen_height/8
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.persistentImage = None

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        buttonboard[x][y] = self

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(pygame.Color(self.fillColors['normal']))
        if self.buttonRect.collidepoint(mousePos):

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if not self.alreadyPressed or not self.onePress:
                    self.onclickFunction(self)
                    self.alreadyPressed = True
                self.buttonSurface.fill(pygame.Color(self.fillColors['pressed']))
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, (self.width / 2 - self.buttonSurf.get_rect().width / 2, self.height / 2 - self.buttonSurf.get_rect().height / 2))
        if self.persistentImage:
            self.buttonSurface.blit(self.persistentImage, (0, 0))  # Adjust position as needed
        screen.blit(self.buttonSurface, (self.xPos, self.yPos))

    def replaceImage(self, image):
        self.persistentImage = image
        self.buttonSurface.blit(image, (0, 0))
    def resetImage(self):
        self.persistentImage = None
        
    def get_coordinates(self):
        return self.x, self.y


selected_piece = None
currPlayer = "white"
def squareClicked(button):
    global selected_piece
    global currPlayer
    x, y = button.get_coordinates()
    square_object = board.get_square(x,y)
    if(selected_piece == square_object and selected_piece != None):
        #player has reselected the same piece, deselecting it
        selected_piece = None
    elif(selected_piece != None):
        try:
            selected_piece.move(x,y,board)
            update_board_graphics(board)
            selected_piece = None
            if(currPlayer == "white"):
                print("Blacks Turn")
                currPlayer = "black"
            else:
                print("Whites Turn")
                currPlayer = "white"
        except:
            selected_piece = None
        #player has a selected piece and has clicked a square which is possible to move to
    elif(square_object == None):
        pass
    elif(square_object.get_loyalty() == currPlayer):
        #player has clicked a piece of their loyalty
        selected_piece = square_object
    

def initializeBoard():
    #set variables:
    square_width = screen_width/8
    square_height = screen_height/8
    
    letters = ['A','B','C','D','E','F','G','H']
    horizontal_pos = 0
    for letter_pos in letters:
        for vertical_pos in range (0,8):
            square_id = letter_pos + str(vertical_pos+1)
            Button(horizontal_pos, 7 - vertical_pos, square_width, square_height, square_id, squareClicked, onePress = True)
        horizontal_pos += 1

def update_board_graphics(board):
    boardModel = board.get_board()
    for i in range(8):
        for j in range(8):
            if boardModel[i][j] != None:
                #print("Found! AT X,Y: " + str(i) + "   " + str(j))
                buttonboard[i][j].replaceImage(boardModel[i][j].get_image())
            else:
                buttonboard[i][j].resetImage()
            #print("NOT Found! AT X,Y: " + str(i) + str(j))
        




# Call the initializeBoard function to create buttons
initializeBoard()
update_board_graphics(board)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(pygame.Color("purple"))

    # Process and draw buttons
    for row in buttonboard:
        for obj in row:
            obj.process()


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
