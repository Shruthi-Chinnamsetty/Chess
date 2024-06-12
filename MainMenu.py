import pygame_menu
import pygame as p
from Chess import Stats
from Chess import ChessMain

#MainMenu


player1 = ''
player2 = ''

def player_1(name):

    l = ChessMain.get_player_names()
    l[0] = name

def player_2(name):

    l = ChessMain.get_player_names()
    l[1] = name



surface2 = p.display.set_mode((600, 400))

menu2 = pygame_menu.Menu('Welcome', 600, 400, theme=pygame_menu.themes.THEME_DARK)

menu2.add.label('Player1')
menu2.add.text_input('', onchange=player_1)
menu2.add.label('Player2')
menu2.add.text_input('', onchange=player_2)
menu2.add.label('')
menu2.add.button('Play', ChessMain.main)
menu2.add.button('Stats', Stats.stats)
menu2.add.button('Quit', pygame_menu.events.EXIT)

# Login Page

username = ['admin']
password = ['admin']

def sign_up():

    new_username = ''
    new_password = ''

    surface = p.display.set_mode((600, 400))
    menu = pygame_menu.Menu('Welcome', 600, 400, theme=pygame_menu.themes.THEME_BLUE)

    def MakeUsername(name):
        global new_username
        new_username = name

    def MakePassword(name):
        global new_password
        new_password = name

    def Store():
        global new_username
        global new_password
        username.append(new_username)
        password.append(new_password)
        account()

    menu.add.label('Username')
    menu.add.text_input('', onchange=MakeUsername)
    menu.add.label('Password')
    menu.add.text_input('', onchange=MakePassword)
    menu.add.button('SignUp', action=Store)
    menu.mainloop(surface)

def sign_in():

    username_check = False
    username_index = 0
    password_check = False
    password_index = 1

    surface = p.display.set_mode((600, 400))

    def MyUsername(name):
        global username_check
        global username_index
        if name in username:
            username_check = True
            username_index = username.index(name)
        else:
            username_check = False

    def MyPassword(name):
        global password_check
        global password_index
        if name in password:
            password_check = True
            password_index = password.index(name)
        else:
            password_check = False

    def MyLogin():
        global username_check
        global username_index
        global password_check
        global password_index
        if username_check and password_check:
            if username_index == password_index:
                menu2.mainloop(surface2)

    menu = pygame_menu.Menu('Welcome', 600, 400, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.label('Username')
    menu.add.text_input('', onchange=MyUsername)
    menu.add.label('Password')
    menu.add.text_input('', onchange=MyPassword)
    menu.add.button('Login', action=MyLogin)
    menu.mainloop(surface)

def account():

    surface = p.display.set_mode((600, 400))
    menu = pygame_menu.Menu('Welcome', 600, 400, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Sign in', sign_in)
    menu.add.button('Sign up', sign_up)
    menu.mainloop(surface)

account()

