import pygame as pg

WIDTH = 1024
HEIGHT = 768
TITLE = "BEst Game Ever!!!!"
TILESIZE = 32
FPS = 30

#colors
WHITE= (255,255,255) #r,g,b value
GREEN = (0,255,0)
RED = (255,0,0)
BGCOLOR = (255,100,100)

# player settings 
PLAYER_SPEED = 300
PLAYER_HIT_RECT = pg.Rect(0,0, TILESIZE-5, TILESIZE-5)