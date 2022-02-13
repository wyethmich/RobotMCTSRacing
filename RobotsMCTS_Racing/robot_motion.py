LENGTH = 10 # from middle of the front wheel to middle of the back wheel
#steering_angle = 0 # angle of front wheels INPUT
#acceleration = 0 # gas/brake INPUT
#speed = 0 
#position = (0,0) # midpoint between the two back wheels
#x = 0
#y = 0
#theta = 0 # global heading of the car


# dx_dt = speed*cos(theta)
# dy_dt = speed*sin(theta)
# dtheta_dt = (speed/LENGTH)*tan(streering_angle)
# dspeed_dt = acceleration

import numpy as np
import math
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import pygame
import matplotlib.patches as patches
from matplotlib import animation
def f(state,t,phi,acceleration): # y = [speed, x, y, theta]
      v = state[0]
      #x = state[1]
      #y = state[2]
      theta = state[3]
      dv_dt = acceleration
      dx_dt = v*math.cos(theta)
      dy_dt = v*math.sin(theta)
      dtheta_dt = (v/LENGTH)*math.tan(phi)
      dstate_dt = [dv_dt,
                  dx_dt,
                  dy_dt,
                  dtheta_dt]
      return dstate_dt
def image_scale(image, factor):
    value = round(image.get_width()*factor),round(image.get_height()*factor)
    return pygame.transform.scale(image,value)
def distance(point1,point2):
   return ((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)**0.5
class motion:
   def __init__(self):
      self.car_image = pygame.image.load('car.png')
      self.car_image = pygame.transform.scale(self.car_image, (25, 50))
      self.car_image = pygame.transform.rotate(self.car_image,-90)
      self.PIVOT = (0,12.5)
      self.timedif = 0
      self.TRACK = image_scale(pygame.image.load("Wyeth-TrackCheckpoint1/Assests/track.png"),0.9)
      self.BORDER = image_scale(pygame.image.load("Wyeth-TrackCheckpoint1/Assests/BORDER.png"),0.9)
      self.BORDER_MASK = pygame.mask.from_surface(self.BORDER)
      self.FINISH = pygame.image.load("Wyeth-TrackCheckpoint1/Assests/finish.png")
      self.FINISH_MASK = pygame.mask.from_surface(self.FINISH)
      self.GRASS = image_scale(pygame.image.load("Wyeth-TrackCheckpoint1/Assests/grass.jpeg"),2.5)
      self.WIDTH, self.HEIGHT = self.TRACK.get_width(), self.TRACK.get_height()
      self.WINDOW = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
      self.FINISH_POSITION = (130,250) 
      self.MAIN_FONT = pygame.font.SysFont("comicsans",44)
      self.images = [(self.GRASS,(0,0)),(self.TRACK,(0,0)),(self.FINISH,self.FINISH_POSITION),(self.BORDER,(0,0))]
      self.START_POS = (180,200)
      self.x1,self.y1 = self.START_POS

      self.path = np.array([(180, 200), (180, 180), (180, 160), (180, 140), (178, 124), 
         (160, 93), (128, 80), (98, 85), (73, 109), (63, 138), (59, 174), (61, 221), (60, 255), 
         (60, 288), (61, 320), (61, 349), (61, 389), (62, 445), (69, 486), (94, 510), (119, 540), (147, 564), 
         (174, 597), (203, 626), (227, 652), (259, 680), (288, 710), (344, 728), (390, 702), (403, 649), (406, 602), 
         (412, 553), (432, 510), (478, 485), (552, 498), (586, 539), (597, 582), (601, 624), (606, 665), (622, 705), 
         (667, 722), (711, 715), (736, 669), (738, 631), (738, 573), (737, 522), (735, 475), (737, 429), (722, 379), 
         (679, 368), (623, 364), (575, 363), (507, 360), (445, 359), (413, 340), (402, 300), (425, 270), (463, 263), 
         (499, 262), (530, 262), (578, 261), (632, 260), (683, 255), (724, 234), (736, 195), (736, 148), (727, 104), 
         (696, 86), (638, 78), (584, 78), (531, 80), (472, 81), (413, 80), (359, 79), (315, 87), (286, 112), (279, 164), 
         (278, 206), (277, 250), (276, 296), (276, 340), (263, 389), (227, 406), (197, 398), (181, 373), (175, 335), 
         (176, 289), (176, 253)])
   
   def closest_point(self,x,y):
      point = min((self.path-[x,y]), key=lambda k: (k[0]**2 + k[1]**2)**0.5)+[x,y]
      for i in range(len(self.path)):
         if self.path[i][0] == point[0] and self.path[i][1] == point[1]:
            return i

   def scoreState(self,x,y):
      point = min((self.path-[x,y]), key=lambda k: (k[0]**2 + k[1]**2)**0.5)+[x,y]
      index = 0
      for i in range(len(self.path)):
         if self.path[i][0] == point[0] and self.path[i][1] == point[1]:
            index = i
            break
      #point2 = min([self.path[index+1],self.path[index-1]], key=lambda k: distance(k,(x,y)))
      index2 = min([index-1,(index+1)%len(self.path)], key=lambda k: distance(self.path[k],(x,y)))
      d1 = distance(point,(x,y))
      d2 = distance(self.path[index2],(x,y))
      if index2 > index:
         return index + (d1)/(d1+d2)
      else:
         return index2 + (d2)/(d1+d2)
   

   def update(self, state, steering, acceleration): # state is [speed, x, y, theta] where x and y and the midpoint between the rear wheels
      t = np.linspace(0, 0.1, 2)
      return odeint(f, state, t, args=(steering, acceleration))[-1]

   def get_frames(self,state,steering,acceleration):
      t = np.linspace(0, 0.1, 11)
      return odeint(f, state, t, args=(steering, acceleration))

   def blitRotate(self, pos, angle):
      originPos = self.PIVOT
      image_rect = self.car_image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
      offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
      rotated_offset = offset_center_to_pivot.rotate(-angle)
      rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
      rotated_image = pygame.transform.rotate(self.car_image, angle)
      rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
      self.WINDOW.blit(rotated_image, rotated_image_rect)
      return rotated_image, rotated_image_rect

   def collide(self,x,y,theta):
      angle = -theta*(180.0/math.pi)
      image_rect = self.car_image.get_rect(topleft = (x-self.PIVOT[0], y-self.PIVOT[1]))
      offset_center_to_pivot = pygame.math.Vector2((x,y)) - image_rect.center
      rotated_offset = offset_center_to_pivot.rotate(-angle)
      rotated_image_center = (x - rotated_offset.x, y - rotated_offset.y)
      rotated_image = pygame.transform.rotate(self.car_image, angle)
      rect = rotated_image.get_rect(center = rotated_image_center)

      offset = (int(rect[0]),int(rect[1]))
      car_mask = pygame.mask.from_surface(rotated_image)
      #offset = (int(rect[0]-x),int(rect[1]-y))
      poi = self.BORDER_MASK.overlap(car_mask,offset)
      return poi
   def collide_finish(self,x,y,theta):
      angle = -theta*(180.0/math.pi)
      image_rect = self.car_image.get_rect(topleft = (x-self.PIVOT[0], y-self.PIVOT[1]))
      offset_center_to_pivot = pygame.math.Vector2((x,y)) - image_rect.center
      rotated_offset = offset_center_to_pivot.rotate(-angle)
      rotated_image_center = (x - rotated_offset.x, y - rotated_offset.y)
      rotated_image = pygame.transform.rotate(self.car_image, angle)
      rect = rotated_image.get_rect(center = rotated_image_center)

      offset = (int(rect[0]-self.FINISH_POSITION[0]),int(rect[1]-self.FINISH_POSITION[1]))
      car_mask = pygame.mask.from_surface(rotated_image)
      #offset = (int(rect[0]-x),int(rect[1]-y))
      poi = self.FINISH_MASK.overlap(car_mask,offset)
      return poi

   def draw_map(self):
      for img, pos in self.images:
         self.WINDOW.blit(img,pos)
      time_text = self.MAIN_FONT.render( "Time: {:.2f}".format(self.timedif),1,(255,255,255))
      self.WINDOW.blit(time_text,(10,self.HEIGHT - time_text.get_height()-40))
   def image_scale(image, factor):
      value = round(image.get_width()*factor),round(image.get_height()*factor)
      return pygame.transform.scale(image,value)
   
   def draw_tree(self,root_node):
      queue = root_node.children
      i = 0
      while(queue):
         node = queue[0]
         queue = queue[1:] + node.children
         pygame.draw.line(self.WINDOW, (0,255,0), (node.state[1],node.state[2]), (node.parent.state[1],node.parent.state[2]), 1)
      return

if __name__ == "__main__":
   y0 = [1,0,0,0]
   
   t = np.linspace(0, 5, 101)
   t2 = np.linspace(5, 10, 101)
   t3 = np.linspace(10, 15, 101)
   t4 = np.linspace(15, 20, 101)
   t_total = np.append(np.append(t,t2),np.append(t3,t4))
   
   sol = odeint(f, y0, t, args=(0, 0))
   sol = np.append(sol,odeint(f, sol[-1], t2, args=(-1.5, .2)), axis=0)
   sol = np.append(sol,odeint(f, sol[-1], t3, args=(1, -.2)), axis=0)
   sol = np.append(sol,odeint(f, sol[-1], t4, args=(.5, 0)), axis=0)
   
   plt.plot(t_total, sol[:, 0], 'b', label='v(t)')
   plt.plot(t_total, sol[:, 1], 'g', label='x(t)')
   plt.plot(t_total, sol[:, 2], 'm', label='y(t)')
   plt.plot(t_total, sol[:,3]%(math.pi*2), 'y', label='theta(t)')
   plt.legend(loc='best')
   plt.xlabel('t')
   plt.grid()
   plt.show()
   
   
   x = sol[:,1]
   y = sol[:,2]
   yaw = sol[:,3]
   fig = plt.figure()
   plt.axis('equal')
   plt.grid()
   ax = fig.add_subplot(111)

   ax.plot(sol[:,1], sol[:,2])
   
   patch = patches.Rectangle((0, 0), 0, 0, fc='y')
   
   def init():
       ax.add_patch(patch)
       return patch,
   
   def animate(i):
       patch.set_xy([x[i], y[i]])
       patch.angle = np.rad2deg(yaw[i])
       patch.set_width(.2)
       patch.set_height(1.0)
       return patch,
   
   anim = animation.FuncAnimation(fig, animate,
                                  init_func=init,
                                  frames=len(x),
                                  interval=20,
                                  blit=True)
   plt.show()

   anim.save('car_motion.gif', writer='imagemagick')