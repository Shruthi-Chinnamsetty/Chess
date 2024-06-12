"""
This the main driver of our game. It will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
from Chess import ChessEngine
import pandas as pd
from csv import writer

winner = ""

player_list = ['player1', 'player2']

def get_player_names():

    return player_list

p.init()
WIDTH = HEIGHT = 600
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
Images = {}

# Initialize the dictionary that contains all the images of the pieces.

def loadImages():

     pieces = ['wp', 'wR', 'bB', 'wN', 'wK', 'wQ', 'bp', 'bR', 'wB', 'bN', 'bK', 'bQ']
     for piece in pieces:
         Images[piece] = p.transform.scale(p.image.load("images/" + piece + '.png'), (SQ_SIZE, SQ_SIZE))

# The main driver for our code which would be responsible to handle ser input and updates graphics.

def main():
    global winner
    screen = p.display.set_mode((WIDTH, HEIGHT))
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()

    running = True

    validMoves = gs.getValidMoves()
    movemade = False

    sqSelected = () #Keep track of the last click of the user. (tuple : (row, col))
    playerClicks = [] #Keep track of the player clicks (two tuples in a list: [(row, col), (row, col)])

    while running:
        for e in p.event.get():

            if e.type == p.QUIT:

                loser = player_list[1] if winner == player_list[0] else player_list[0]

                df = pd.read_csv('Stats.csv')
                names = df['Name']

                name_list = list(names.values)

                if winner in name_list:

                    index = name_list.index(winner)

                    df.loc[index, 'Win'] += 1
                    df.to_csv("Stats.csv", index=False)

                else:

                    record = [winner, 1, 0]

                    df.loc[len(name_list)] = record
                    df.to_csv("Stats.csv", index=False)

                if loser in name_list:

                    index = name_list.index(loser)

                    df.loc[index, 'Lose'] += 1
                    df.to_csv("Stats.csv", index=False)

                else:

                    record = [loser, 0, 1]

                    df.loc[len(name_list)] = record
                    df.to_csv("Stats.csv", index=False)

                running = False


            elif e.type == p.MOUSEBUTTONDOWN: #Checks if the mouse clicked has been recorded in the screen.
                location = p.mouse.get_pos() #Gets the x,y position of the place where mouse was clicked.
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                valid_color = []

                for i in validMoves:
                    if i.startRow == row and i.startCol == col:
                        valid_color.append([i.endRow, i.endCol])


                if sqSelected == (row, col): #Checks if user clicks same square twice.
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2: #Opeartion after 2nd click.

                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            #print(move.getChessNotation())
                            movemade = True
                            # Resetting user clicks.
                            sqSelected = ()
                            playerClicks = []

                    if movemade == False:
                        playerClicks.pop(0)


            elif e.type == p.KEYDOWN:
                if e.key == p.K_z and p.key.get_mods() & p.KMOD_LCTRL:
                    gs.undoMove()
                    movemade = True
                if e.key == p.K_r and p.key.get_mods() & p.KMOD_LCTRL: #reset the game when 'r' is pressed
                    gs = ChessEngine.GameState()
                    valid_moves = gs.getValidMoves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False

            if movemade:
                validMoves = gs.getValidMoves()
                movemade = False

        try:
            drawGameState(screen, gs, valid_color)
        except UnboundLocalError:
            drawGameState(screen, gs, valid_color=[])


        if gs.checkmate:
            if gs.whiteToMove:

                drawText(screen, f"{player_list[1]} wins by checkmate")

                winner = player_list[1]

            else:
                drawText(screen, f"{player_list[0]} wins by checkmate")

                winner = player_list[0]


        elif gs.stalemate:
            drawText(screen, "Stalemate")
    
        p.display.flip()

# This functions will write the text of winning the game

def drawText(screen, text):
    font = p.font.SysFont("Helvitica", 35, True, False)
    text_object = font.render(text, 0, p.Color("white"))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2, HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, p.Color('black'))
    screen.blit(text_object, text_location.move(2,2))

# This function will be responsible for all the graphics present in current game state.

def drawGameState(screen, gs, valid_color):
    # Drawing squares on the board.
    drawBoard(screen)
    # Drawing pieces on the top of those squares.
    drawPieces(screen, gs.board)
    if len(valid_color) > 0:
        drawValid(screen, valid_color)


# Drawing the squares on the board.

def drawBoard(screen):
    colors = [p.Color("#ecf3d2"), p.Color("#63a157")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c) % 2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


# Drawing the pieces on the board using the current GameState.board

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(Images[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Drawing the pieces on the board which are valid.

def drawValid(screen, valid_color):
    for i in valid_color:
        p.draw.circle(screen, 'green', (i[1] * SQ_SIZE + SQ_SIZE/2, i[0] * SQ_SIZE + SQ_SIZE/2), 13)



