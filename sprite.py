import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import *

from random import randint

from os import path 

vec = pg.math.Vector2

def collide_hit_rect(one, two): #def what will happen if the player comes into contact with an object
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite, group, dir): #defines what happens when player comes into contact with the walls
    #check for x collision
    if dir =='x':
        #checks if we collided with hit rects
        hits = pg.sprite.spritecollide(sprite,group, False, collide_hit_rect)
        if hits: 
            #this line checks to see if we're to the the left of the wall
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                #reposition the sprite/player to the left side of the wall
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width/2
            if hits [0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir =='y':
        hits = pg.sprite.spritecollide(sprite,group, False, collide_hit_rect)
        if hits: 
            #this line checks to see if we're to the top of the wall
            if hits[0].rect.centery > sprite.hit_rect.centery:
            #reposition the sprite/player to the top side of the wall
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height/2
            if hits [0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y
           
class player (Sprite): #creating the class player
    def __init__(self, game, x,y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        self.load_images()
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE) 
        self.image.set_colorkey(BLACK)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.vel = vec(0,0)
        self.pos = vec(x*TILESIZE,y*TILESIZE)
        self.last_update = 0 
        self.current_frame = 0
        self.coins = 0
        self.dir = "none"

        print("player initialized")

    def get_keys(self):
        #reset d to zero
        # listen for events specific to keys
        #change velocity based on which key is pressed
       
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        #check to see if player is moving diagonal 
        if self.vel.x != 0 and self.vel.y !=0:
            #self.vel.normalize()
            self.vel *= 0.7071

    def animate(self): #animates the sprite player
        # use the time element to get now
        now = pg.time.get_ticks()
        if self.dir == "none":
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        elif self.dir == "right":
            pass

    def load_images(self): #moves from one image of player to another image of the player continuously
        self.idle_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE),
                            self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)
                            ]
        

    def update(self): #updates all attributes of player
        self.get_keys()
        self.animate()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        hits = pg.sprite.spritecollide(self, self.game.all_coins, True)
        if hits:
            for i in range(10):
                Particle(self.game, hits[0].pos.x, hits[0].pos.y)
            self.coins += 1
            self.game.score += 1
            self.game.pickup_snd.play()
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self,self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center


class Wall (Sprite): #defines class wall
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx,self.vy = 0,0
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.rect.x = self.x 
        self.rect.y = self.y
        print("wall initialized")

class Particle (Sprite): #defines the class particles
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.all_particles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/8, TILESIZE/8))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vel=vec(randint(-180,180), randint(-180,180))
        self.pos = vec(x,y)
        self.speed = randint(1,3)
        self.countdown = Cooldown()
        self.countdown.event_time = floor(pg.time.get_ticks()/1000)
        print(self.pos.x)
        print(self.pos.y)
        print(str(len(self.game.all_particles)))

    def update(self):
        self.countdown.ticking()

        self.pos += self.vel * self.speed * self.game.dt
        if self.countdown.delta > 1:
            self.kill()
            print("im dead")

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

class Coin(Sprite): #defines coin collectable
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        pg.draw.circle(self.image, GOLD, (TILESIZE/2, TILESIZE/2), TILESIZE/2)
        # pg.draw.ellipse(self.image, GOLD, (TILESIZE/2, TILESIZE/2), TILESIZE/2)
        self.image.set_colorkey(BLACK)
        # self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0) 
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
        
class Mob (Sprite): #defines mob sprite
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        self.load_images()
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE) 
        self.image.set_colorkey(BLACK)
        self.image = self.spritesheet.get_image(0,0,TILESIZE, TILESIZE)
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.speed = 100
        self.vel = vec(0,0)
        self.pos = vec(x*TILESIZE, y*TILESIZE)
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        self.last_update = 0 
        self.current_frame = 0
        self.hit_rect = MOB_HIT_RECT
        self.dir = "none"
        

    def animate(self): #animating mob
         # use the time element to get now
        now = pg.time.get_ticks()
        if self.dir == "none":
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        elif self.dir == "right":
            pass

    def load_images(self): #move mob sprite from one image of spritesheet to the next
        self.idle_frames = [self.spritesheet.get_image(64,0,TILESIZE, TILESIZE),
                                self.spritesheet.get_image(96,0,TILESIZE, TILESIZE)
                                ]
        self.run_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE),
                                self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)
                                ]   
    #uses autpcomplete by creating a chase method using pos vectors and obj as a parameter
    def chase(self, obj):
        if self.pos.x < obj.pos.x:
            self.vel.x = self.speed
            self.dir = "right"
        elif self.pos.x > obj.pos.x:
            self.vel.x = -self.speed
            self.dir = "left"
        else:
            self.vel.x = 0

        if self.pos.y < obj.pos.y:
            self.vel.y = self.speed
        elif self.pos.y > obj.pos.y:
            self.vel.y = -self.speed
        else:
            self.vel.y = 0

    def update(self): #updates the attributes of mob
        self.animate()
        if self.game.player:
            self.chase(self.game.player)
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center