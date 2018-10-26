import pygame
from pygame.locals import *
import random, sys

def events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

W, H = 800, 537
HW, HH = W / 2, H / 2
AREA = W * H

# initialise display
pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("ball")
FPS = 30

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)

OW, OH = 40, 200

bground = pygame.image.load("sea.jpg")

class Obstacle:
    def __init__(self, x, y, width, height, velocityObstacle):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocityObstacle = velocityObstacle

    def test(self, player):
        if player.y + player.radius >= self.y and player.y - player.radius <= self.y + self.height:
            if player.x - player.radius == self.x:
                return True
        elif self.x <= 0:
            return False
        else:
            return None
        

class Obstacles:
    generateTime = 0
    randomTime = random.randint(10, 15)
    def __init__(self):
        self.container = list([])

    def add(self, p):
        self.container.append(p)

    def draw(self):
        global WHITE
        display = pygame.display.get_surface()
        for p in self.container:
            pygame.draw.rect(display, WHITE, (int(p.x), int(p.y), p.width, p.height))
            p.x += p.velocityObstacle
        self.generateTime += 1
        if self.generateTime == self.randomTime:
            OBSTACLES.add(Obstacle(W, random.randint(0, 400), 2, random.randint(150, 300), -10))
            self.generateTime = 0
            self.randomTime = random.randint(10, 20)

    def testCollision(self, player):
        for p in self.container:
            result = p.test(player)
            if result:
                print('salami')
            if result == False:
                self.container.remove(p)
        

class Player:
    def __init__(self, x, y, radius, velocity):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = velocity
        starts = [self.velocity, -self.velocity]
        random.shuffle(starts)
        self.yVelocity = starts[0]

    def keys(self):
        k = pygame.key.get_pressed()
        if k[K_UP] and self.y - self.radius > 0: self.yVelocity = -self.velocity 
        elif k[K_DOWN] and self.y + self.radius < H : self.yVelocity = self.velocity
        
    def move(self):
        self.y += self.yVelocity
        if self.y - self.radius <= 0:
            self.yVelocity = 0
        elif self.y + self.radius >= H:
            self.yVelocity = 0
            
    def draw(self):
        display = pygame.display.get_surface()
        pygame.draw.circle(display, WHITE, (int(self.x), int(self.y)), self.radius)        
                         
OBSTACLES = Obstacles()
PLAYER = Player(50, H//2, 20, 10)
    
while True:
    events()
    
    OBSTACLES.draw()
    OBSTACLES.testCollision(PLAYER)
    
    PLAYER.keys()
    PLAYER.move()
    PLAYER.draw()
    
    pygame.display.update()
    CLOCK.tick(FPS)
    DS.fill(BLACK)

