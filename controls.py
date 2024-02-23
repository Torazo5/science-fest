

# KeyboardTelloModule.py
import pygame


# Initialize pygame library
pygame.init()
pygame.display.set_mode((1, 1), pygame.NOFRAME)  # Create a small window without a frame


def getKey(keyName):
   ans = False
   for event in pygame.event.get():
       pass
   keyInput = pygame.key.get_pressed()
   myKey = getattr(pygame, f'K_{keyName}')
   if keyInput[myKey]:
       ans = True
   return ans


def getKeyboardInput():
   # LEFT RIGHT, FRONT BACK, UP DOWN, YAW VELOCITY
   lr, fb, ud, yv = 0, 0, 0, 0
   speed = 80
   liftSpeed = 80
   moveSpeed = 85
   rotationSpeed = 100


   if getKey("LEFT"):
       lr = -speed  # Controlling The Left And Right Movement
   elif getKey("RIGHT"):
       lr = speed


   if getKey("UP"):
       fb = moveSpeed  # Controlling The Front And Back Movement
   elif getKey("DOWN"):
       fb = -moveSpeed


   if getKey("w"):
       ud = liftSpeed  # Controlling The Up And Down Movement
   elif getKey("s"):
       ud = -liftSpeed


   if getKey("d"):
       yv = rotationSpeed  # Controlling the Rotation
   elif getKey("a"):
       yv = -rotationSpeed


   return [lr, fb, ud, yv]  # Return The Given Value
