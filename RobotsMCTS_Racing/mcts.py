import pygame
from robot_motion import motion
import math
import time
import random
  
class Node:
    def __init__(self, state, parent, action, steering, acceleration):
        self.state = state
        self.steering = steering
        self.acceleration = acceleration
        self.parent = parent
        self.children = []
        #self.actions_not_tried = [(0,0),(3,0),(3,-0.4),(3,0.4),(-3,0),(-3,-0.4),(-3,0.4),(0,0.4),(0,-0.4)]
        self.actions_not_tried = [(0,0),(0,0.2),(0,-0.2)]

        self.action = action
        self.reward = 0
        self.n = 1 # number of times expanded
        return
    def update(): # update and back propogate
        return
    

class game():
    def __init__(self):
        #self.actions = [(0,0),(3,0),(3,-0.3),(3,0.3),(-3,0),(-3,-0.3),(-3,0.3),(0,0.3),(0,-0.3)] # (acceleration,steering)
        self.actions = [(0,0),(0,0.2),(0,-0.2)]
        self.rob_motion = motion()
        self.Cp = 5 # exploration coef
        return
    def isterminal(self,state):
        return self.rob_motion.collide(state[1],state[2],state[3])
    def expand_node(self, node):
        action = random.choice(node.actions_not_tried)
        node.actions_not_tried.remove(action)
        new_steering = node.steering+action[1]
        new_acceleration = node.acceleration+action[0]
        new_state = self.rob_motion.update(node.state,new_steering,new_acceleration)
        new_node = Node(new_state,node,action,new_steering,new_acceleration)
        node.children += [new_node]
        return new_node
    def TreePolicy(self,node):
        while not self.isterminal(node.state):
            if len(node.children) < len(self.actions):
                return self.expand_node(node)
            node = self.bestChild(node)
        return node
    def bestChild(self,node):
        explore_term = 2*math.log(node.n)
        return max(node.children, key = lambda v: (v.reward/v.n)+self.Cp*math.sqrt(explore_term/v.n))
    def DefaultPolicy(self, node):
        state = node.state
        steering = node.steering
        acceleration = node.acceleration
        i = 0
        while not self.isterminal(state):
            random_action = random.choice(self.actions)
            steering += random_action[1]
            acceleration += random_action[0]
            state = self.rob_motion.update(state,steering,acceleration)
            i += 1
        score = self.rob_motion.scoreState(state[1],state[2])
        if i == 1:
            score /= 2
        return score
    def backup(self,node,reward):
        while node.parent != None:
            node.n+=1
            node.reward+=reward
            node = node.parent
        return
    def mcts(self,root_node,computaional_budget,frames):
        # given node with initial state (could be root of existing tree if tree is being fed forward)
        start_time = time.time()
        last_node = None
        frame = 0
        while(time.time()-start_time < computaional_budget): # While withing computational budget
            if(time.time()-start_time > (computaional_budget/10.0)*(frame)):
                frame += 1
                angle = -frames[frame][3]*(180.0/math.pi)
                self.animate((frames[frame][1],frames[frame][2]),angle)
            node = self.TreePolicy(root_node)
            if node == last_node:
                reward = -1
            else:
                reward = self.DefaultPolicy(node)
            self.backup(node,reward)
            last_node = node
        return self.bestChild(root_node)
    def animate(self,pos,angle):
        self.rob_motion.draw_map()
        text_surface = myfont.render('Acceleration = '+str(acceleration)+", Steering = "+str(steering), False, (0, 0, 0))
        self.rob_motion.WINDOW.blit(text_surface, (0,0))
        rotated_image,rect = Game.rob_motion.blitRotate( pos, angle)
        Game.rob_motion.draw_tree(head)
        pygame.display.update()
        return


if __name__ == "__main__":
    initial_state = (160,180,200,-math.pi/2.0)
    steering = 0
    acceleration = 0
    head = Node(initial_state,None,None,steering,acceleration)
    last_head = head

    pygame.font.init()
    FPS = 60
    clock = pygame.time.Clock()
    begin = 0
    timedif = 0
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    Game = game()
    iteration_time = 0.5
    frames = [head.state for i in range(11)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        #Game.rob_motion.draw_map()
        #text_surface = myfont.render('Acceleration = '+str(acceleration)+", Steering = "+str(steering), False, (0, 0, 0))
        #Game.rob_motion.WINDOW.blit(text_surface, (0,0))
        #old_head = head
        Game.Cp += 0.03
        #print(Game)
        if iteration_time > 0.25:
            iteration_time *= 0.99
        head = Game.mcts(head,iteration_time,frames) # make the next head of the tree equal to the decision
        #frames = Game.rob_motion.get_frames(head.state,steering,acceleration)
        head.parent = None
        steering = head.steering
        acceleration = head.acceleration
        pos = (head.state[1],head.state[2])
        angle = -head.state[3]*(180.0/math.pi)
        frames = Game.rob_motion.get_frames(last_head.state,steering,acceleration)
        last_head = head
        #rotated_image,rect = Game.rob_motion.blitRotate( pos, angle)
        #Game.rob_motion.draw_tree(head)
        #pygame.display.update()
        #Game.animate(pos,angle)
        print(frames)

        if Game.rob_motion.collide(head.state[1], head.state[2],head.state[3]): #restart if there is a collision
            initial_state = (15,180,200,-math.pi/2.0)
            steering = 0
            acceleration = 0
            head = Node((15,180,200,-math.pi/2.0),None, None,steering,acceleration)
