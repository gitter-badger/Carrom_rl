# Defines Headers, State For Carromimport sys, random
import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
import pymunk.pygame_util
import random
import sys
from math import sqrt,sin,cos

# Global Variables

Static_Velocity_Threshold=2 # Velocity below which an object is considered to be static



Board_Size=800
Board_Damping=0.91# Tune how much the velocity falls


Striker_Angle=(0,1)
Striker_Force=(5000)

Board_Walls_Size=Board_Size*2/90
Board_Size_Walls_Elasticity=0.9

Coin_Mass=1
Coin_Radius=Board_Size*1/70
Coin_Elasticity=0.9

Striker_Mass=1.5
Striker_Radius=Board_Size*1.5/70
Striker_Elasticity=0.9

Hole_Radius=2*Coin_Radius

Striker_Color=[65,125,212]
Hole_Color=[0,0,0]
Black_Coin_Color=[43,43,43]
White_Coin_Color= [169,121,47]
Red_Coin_Color=[169,53,53]
Board_Walls_Color=[56,32,12]
Board_Color=[242,209,158]


def dist(p1,p2):
    return sqrt(pow(p1[0]-p2[0],2)+pow(p1[1]-p2[1],2))


#N randomly generated coin positions around the center of the board
def generate_coin_locations(N):
    # Later do collision handling
    L=[]
    for i in range(N):
        L.append((random.randrange(0.3*Board_Size,0.7*Board_Size),(random.randrange(0.3*Board_Size,0.7*Board_Size))))

    return L

def init_space(space):
    space.damping = Board_Damping
    space.threads=2

def init_walls(space):  # Initializes the four outer walls of the board
    walls = [pymunk.Segment(space.static_body, (0, 0), (0, Board_Size), Board_Walls_Size)
        ,pymunk.Segment(space.static_body, (0,0), (Board_Size, 0), Board_Walls_Size)
        ,pymunk.Segment(space.static_body, (Board_Size, Board_Size), (Board_Size, 0), Board_Walls_Size)
        ,pymunk.Segment(space.static_body, (Board_Size, Board_Size), (0,Board_Size), Board_Walls_Size)
        ]  
    for wall in walls:
        wall.color = Board_Walls_Color
        wall.elasticity = Board_Size_Walls_Elasticity
        
    
    space.add(walls)

def init_holes(space):  # Initializes the four outer walls of the board
    Holes=[]
    for i in [(Board_Size/22, Board_Size/22),(Board_Size - Board_Size/22, Board_Size/22),(Board_Size - Board_Size/22, Board_Size - Board_Size/22),(Board_Size/22, Board_Size - Board_Size/22)]:
        inertia = pymunk.moment_for_circle(0.1, 0, Hole_Radius, (0,0))
        body = pymunk.Body(0.1, inertia)
        body.position = i
        shape = pymunk.Circle(body, Hole_Radius, (0,0))
        shape.color=Hole_Color
        shape.collision_type = 2
        shape.filter = pymunk.ShapeFilter(categories=0b1000)
        space.add(body, shape)
        Holes.append(shape)
        del body
        del shape
    return Holes

def init_striker(space,x, passthrough,action):
    """Add a ball to the given space at a random position"""

    inertia = pymunk.moment_for_circle(Striker_Mass, 0, Striker_Radius, (0,0))
    body = pymunk.Body(Striker_Mass, inertia)
    body.position = action[1]
    body.apply_force_at_world_point((cos(action[0])*action[2],sin(action[0])*action[2]),body.position+(Striker_Radius*0,Striker_Radius*0))
    #print body.position
    shape = pymunk.Circle(body, Striker_Radius, (0,0))
    shape.elasticity=Striker_Elasticity
    shape.color=Striker_Color

    mask = pymunk.ShapeFilter.ALL_MASKS ^ passthrough.filter.categories

    sf = pymunk.ShapeFilter(mask=mask)
    shape.filter = sf 
    shape.collision_type=2
    
    space.add(body, shape)
    return shape

def init_coins(space,coords_black,coords_white,coord_red,passthrough):
    #Adds coins to the board at the given coordinates 
    Coins=[]
    inertia = pymunk.moment_for_circle(Coin_Mass, 0, Coin_Radius, (0,0))
    for coord in coords_black:

        #shape.elasticity=1
        #body.position = i
        body=pymunk.Body(Coin_Mass, inertia)
        body.position=coord
        shape=pymunk.Circle(body, Coin_Radius, (0,0))
        shape.elasticity=Coin_Elasticity
        shape.color=Black_Coin_Color


        mask = pymunk.ShapeFilter.ALL_MASKS ^ passthrough.filter.categories

        sf = pymunk.ShapeFilter(mask=mask)
        shape.filter = sf 
        shape.collision_type=2

        space.add(body, shape)
        Coins.append(shape)
        del body
        del shape

        #body.apply_force_at_world_point((-1000,-1000),body.position)

        #shape.elasticity=1
        #body.position = i
    for coord in coords_white:
        body=pymunk.Body(Coin_Mass, inertia)
        body.position=coord
        shape=pymunk.Circle(body, Coin_Radius, (0,0))
        shape.elasticity=Coin_Elasticity
        shape.color=White_Coin_Color

        mask = pymunk.ShapeFilter.ALL_MASKS ^ passthrough.filter.categories

        sf = pymunk.ShapeFilter(mask=mask)
        shape.filter = sf 
        shape.collision_type=2

        space.add(body, shape)
        Coins.append(shape)
        del body
        del shape
        #body.apply_force_at_world_point((-1000,-1000),body.position)

    for coord in coord_red:
        body=pymunk.Body(Coin_Mass, inertia)
        body.position=coord
        shape=pymunk.Circle(body, Coin_Radius, (0,0))
        shape.elasticity=Coin_Elasticity
        shape.color=Red_Coin_Color
        mask = pymunk.ShapeFilter.ALL_MASKS ^ passthrough.filter.categories

        sf = pymunk.ShapeFilter(mask=mask)
        shape.filter = sf 
        shape.collision_type=2

        space.add(body, shape)
        Coins.append(shape)
        del body
        del shape
    return Coins










