import pygame
import time
#from drive import MAIN_FONT
import robot_motion
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)


def image_scale(image, factor):
    value = round(image.get_width()*factor),round(image.get_height()*factor)
    return pygame.transform.scale(image,value)

#load in images and create window
if __name__ == "__main__":
    TRACK = image_scale(pygame.image.load("Wyeth-TrackCheckpoint1/Assests/track.png"),0.9)
    BORDER = image_scale(pygame.image.load("Wyeth-TrackCheckpoint1/Assests/BORDER.png"),0.9)
    BORDER_MASK = pygame.mask.from_surface(BORDER)
    FINISH = pygame.image.load("Wyeth-TrackCheckpoint1/Assests/finish.png")
    GRASS = image_scale(pygame.image.load("Wyeth-TrackCheckpoint1/Assests/grass.jpeg"),2.5)
    WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

    images = [(GRASS,(0,0)),(TRACK,(0,0))]
    START_POS = (180,200)
    x1,y1 = START_POS
    pygame.display.set_caption("Autonomous Project")


    FPS = 60
    #Game loop
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
  #      draw(WINDOW,images)
    
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        #Will print collision
 #       if collide(BORDER_MASK) !=None:
 #           print("collide")


    pygame.quit()