#import map
import pygame
from robot_motion import motion
from mcts_draft import MCTS, RacecarNode
import math
import time
from collections import defaultdict
pygame.font.init()

robot_motion = motion()
tree = MCTS()

myfont = pygame.font.SysFont('Comic Sans MS', 30)



def blit_text_center(win,font,text):
    render = font.render(text,1,(200,200,200))
    win.blit(render,(win.get_width()/2 - render.get_width()/2, win.get_height()/2 - render.get_height()/2))


def collide(mask,car_image,rect,x=0,y=0):
    offset = (int(rect[0]),int(rect[1]))
    car_mask = pygame.mask.from_surface(car_image)
    offset = (int(rect[0]-x),int(rect[1]-y))
    poi = mask.overlap(car_mask,offset)
    return poi

def distance(point1, point2):
    px = (float(point1[0])-float(point2[0]))**2
    py = (float(point1[1])-float(point2[1]))**2
    return (px+py)**(0.5)
FPS = 60
#Game loop
run = True
clock = pygame.time.Clock()
x = 60 #180 
y = 170 #200
speed = 30
theta = math.pi/2.0 # flip sign
steering = 0
acceleration = 0
state = [speed,x,y,theta]
car_init = RacecarNode(state)
begin = 0
timedif = 0

while run:
    
   
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
               steering -= 0.1
            if event.key == pygame.K_RIGHT:
               steering += 0.1
            if event.key == pygame.K_DOWN:
               acceleration -= 0.1
            if event.key == pygame.K_UP:
               acceleration += 0.1
   # draw_points(WINDOW,path)
    robot_motion.draw_map()
    
    while not begin:
        blit_text_center(robot_motion.WINDOW, robot_motion.MAIN_FONT,"Press any key to start.")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                start_time = time.time()
                print(start_time)
                begin = 1

    
    for _ in range(10):
        tree.do_rollout(car_init)
    car_init = tree.choose(car_init)
    tree.Q = defaultdict(int)
    tree.N = defaultdict(int)
    tree.children = dict()
    
    print("state", car_init.state[0], car_init.state[1], car_init.state[2], car_init.state[3])
    if robot_motion.collide(car_init.state[1], car_init.state[2], car_init.state[3]) is not None:
        break

    text_surface = myfont.render('Acceleration = '+str(acceleration)+", Steering = "+str(steering), False, (0, 0, 0))
    robot_motion.WINDOW.blit(text_surface, (0,0))
    state = car_init.state

    pos = (state[1], state[2])
    #print(pos)
    angle = -state[3]*(180.0/math.pi)
    rotated_image,rect = robot_motion.blitRotate(pos, angle)
    pygame.draw.line(robot_motion.WINDOW, (0, 255, 0), (pos[0]-20, pos[1]), (pos[0]+20, pos[1]), 3)
    pygame.draw.line(robot_motion.WINDOW, (0, 255, 0), (pos[0], pos[1]-20), (pos[0], pos[1]+20), 3)

    pygame.display.update()
    #Will print collision
    #if collide(BORDER_MASK,rotated_image,rect) !=None:
    if robot_motion.collide(state[1], state[2],state[3]):
        print("collide")
    if collide(robot_motion.FINISH_MASK,rotated_image,rect,*robot_motion.FINISH_POSITION) != None:
        print("Lap Complete!")
        temp = current_time - start_time
        time_text = robot_motion.MAIN_FONT.render( "Time: {:.2f}".format(temp),1,(255,255,255))
        robot_motion.WINDOW.blit(time_text,(10,robot_motion.HEIGHT - time_text.get_height()-10))
        pygame.display.update()
    else:
        current_time = time.time()
        robot_motion.timedif = current_time - start_time
  
    #print(distance(START_POS,pos))
    clock.tick(FPS)

#print(path)
pygame.quit()
