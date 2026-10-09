#This code was created by Aidan Powell
#Code is inspired by game dev Chris Bradfield who was inspired by notch

''''''
#Why are we making game a class? --> So we can store and organize all the objects in that class
#Why is it capitalized
#What is init?
#What is pass?

#Data types: boolean, JSON, strings, 
#Input (events): Keyboard, mouse, right click, voice, 
# power button, eye tracking, camera, gyroscoping, electrostatic, location, volume, 
# microphone

#Process: cursor position, position of the player, score, enemy position, velocity, 
#aim in a FPS, 

#Output: Graphics, sound, haptics (vibration of the controller)

#CSGO
#GOALS: kill eveyone not on your team, last one standing, Plant or Defuse Bombs

#RULES: 

#FEEDBACK

#FREEDOM

''''''

import pygame as pg 
from os import path       #import the pygame into the code
from settings import *    #have the other blocks of code be imported here so we can use them
from sprite import* 
from utils import * 

class Game: #defining the class game
    def __init__(self): #runs first and are the processors of the class game
          pg.init()
          pg.mixer.init()
          self.screen = pg.display.set_mode((WIDTH , HEIGHT))
          print("game initialize...")
          pg.display.set_caption(TITLE)
          self.running = True
          self.playing = True
          self.clock = pg.time.Clock()

    def load_data(self,map): #makes images, sounds, and text available
        self.game_dir = path.dirname(__file__)
        self.img_dir = path.join(self.game_dir, 'images')
        self.snd_dir = path.join(self.game_dir, 'audio')
        self.map = Map(path.join(self.game_dir, map))

    def new(self): # instantiating sprite groups (adding and positioning the sprites)
        self.load_data('level1.txt') #also sets up tilemap 
        print(self.map.data)
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        #self.player = player(self,WIDTH/2, HEIGHT/2)
        self.wall = Wall(self,2,0)
        self.mob = Mob(self,5,0)
        print(type(self.all_sprites))
        # self.all_sprites.add(self.player)
        # self.all_sprites.add(self.walls)

        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'M':
                    pass
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == 'P':
                    player(self, col, row)

    def run(self): #CORE of the game loop 
        self.playing= True
        while self.playing:
            self.dt = self.clock.tick(FPS)/ 1000
            self.events()
            self.update()
            self.draw()

    def events(self): #handles all the user input
         for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing =False
                self.running = False
    def draw_text(self, text, size, color, x,y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def update(self):
       self.all_sprites.update()
       
    def draw(self):
        #The order matters: The bottom layers of the game are the ones that need to be drawn first
        #Last(text) should be on top of everything
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text("Frames per second: " +str(floor(1/self.dt) ), 24, WHITE, WIDTH/2, HEIGHT/4)
        pg.display.flip()


if __name__=="__main__":
    g= Game() #instantiated the Game Class (Called for the game class

while g.running:
    g.new() 
    g.run()   