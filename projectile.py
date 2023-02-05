import pygame
import math
import time

wScreen = 1200
hScreen = 500
dt = 0.05
g = 9.8

win = pygame.display.set_mode((wScreen, hScreen))
pygame.display.set_caption("Projectile simulation")

class Ball():
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.alfa = 0
        self.power = 0
        self.shoot = False
        self.time = 0
        self.radius = radius
        self.color = color
    
    def onGround(self):
        return (self.y == hScreen - self.radius
                and self.dx == 0
                and self.dy == 0)

    def tick(self):
        #object mechanic
        self.x = self.x + dt * self.dx
        self.y = self.y + dt * self.dy

        #determine angle alfa only if the ball is on the ground and not moving
        if self.onGround():
            self.alfa = find_angle(self)
            self.power = (math.sqrt(((pygame.mouse.get_pos()[0]-self.x)**2)+((pygame.mouse.get_pos()[1]-self.y)**2)))/5

        #check wheter object is in window
        #exit from window on the right
        if self.x > wScreen:
            self.x = 0
        #exit from window on the left
        if self.x < 0:
            self.x = wScreen
        #ball on the ground
        if self.y > hScreen - golfBall.radius:
            self.y = hScreen - golfBall.radius
            self.shoot = False
            self.dx = 0
            self.dy = 0
            self.time = 0
        #exit from window at top
        if self.y < 0:
            self.y = 0

        #shooting
        if self.shoot == True:
            self.time += dt
            self.dx = self.power * math.cos(math.radians(self.alfa))
            self.dy = -self.power * math.sin(math.radians(self.alfa)) + g*self.time
    
    def draw(self, win):
        pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), self.radius)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius-1)

def draw_line(win, ball):
    pygame.draw.line(win, (255, 255, 255), (ball.x, ball.y), pygame.mouse.get_pos())

def find_angle(ball):
    try:
        angle = -math.degrees(math.atan((pygame.mouse.get_pos()[1]-ball.y)/(pygame.mouse.get_pos()[0]-ball.x)))
    except ZeroDivisionError:
        angle = 90

    if ball.x > pygame.mouse.get_pos()[0]:
        angle = 180-abs(angle)
    
    return angle

def redrawWindow():
    win.fill((94,94,94))
    golfBall.draw(win)
    draw_line(win, golfBall)
    pygame.display.update()

radius = 10
golfBall = Ball(300, hScreen-radius, radius, (255,94,14))

run = True

while run: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            golfBall.shoot = True
    golfBall.tick()
    redrawWindow()
    print(golfBall.power, golfBall.alfa)
    time.sleep(dt/10)

pygame.quit()
