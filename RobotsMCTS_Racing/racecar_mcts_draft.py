#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from abc import ABC, abstractmethod
from collections import defaultdict
import math
from collections import namedtuple
from random import choice
from robot_motion import motion
import numpy as np
from scipy.integrate import odeint

robot_motion = motion()
LENGTH = 10

class MCTS:
    "Monte Carlo tree searcher. First rollout the tree then choose a move."

    def __init__(self, exploration_weight=1):
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.children = dict()  # children of each node
        self.exploration_weight = exploration_weight

    def choose(self, node):
        "Choose the best successor of node. (Choose a move in the game)"
        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            return node.find_random_child()

        def score(n):
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            return self.Q[n] / self.N[n]  # average reward

        
        return max(self.children[node], key=score)

    def do_rollout(self, node):
        "Make the tree one layer better. (Train for one iteration.)"
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._simulate(leaf, path)
        self._backpropagate(path, reward)
        

    def _select(self, node):
        "Find an unexplored descendent of `node`"
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper
    ######## Will need to adjust to reset children (or cache them?) for each step #######
    ######## This function was originally made for games with non-repetitive discrete states ######

    def _expand(self, node):
        "Update the `children` dict with the children of `node`"
        if str(node.state) in self.children:
            return  # already expanded
        self.children[str(node.state)] = node.find_children()

    def _simulate(self, node, path):
        #print("node", node.state[0], node.state[1], node.state[2], node.state[3])
        "Returns the reward for a random simulation (to completion) of `node`"
        invert_reward = True
        for i in range(75):
        #while True:
            if node.is_terminal():
                reward = node.reward()
                return(reward)
            else:
                node = node.find_random_child()
        reward = node.reward()
        return(reward)
            #node = node.find_random_child()

    def _backpropagate(self, path, reward):
        "Send the reward back upa to the ancestors of the leaf"
        for node in reversed(path):
            self.N[node] += 1
            print(self.Q[node], reward)
            self.Q[node] += reward


    def _uct_select(self, node):
        "Select a child of node, balancing exploration & exploitation"

        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            "Upper confidence bound for trees"
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=uct)


class Node(ABC):
    """
    A representation of a single board state.
    MCTS works by constructing a tree of these Nodes.
    Could be e.g. a chess or checkers board state.
    """

    @abstractmethod
    def find_children(self):
        "All possible successors of this board state"
        return set()

    @abstractmethod
    def find_random_child(self):
        "Random successor of this board state (for more efficient simulation)"
        return None
        

    @abstractmethod
    def is_terminal(self):
        "Returns True if the node has no children"
        return True

    @abstractmethod
    def reward(self):
        "Assumes `self` is terminal node. 1=win, 0=loss, .5=tie, etc"
        return 0

    @abstractmethod
    def __hash__(self):
        "Nodes must be hashable"
        return 123456789

    @abstractmethod
    def __eq__(node1, node2):
        "Nodes must be comparable"
        return True



# Inheriting from a namedtuple is convenient because it makes the class
# immutable and predefines __init__, __repr__, __hash__, __eq__, and others
path = [(180, 200), (180, 180), (170, 160), (170, 140), (172, 113), (162, 101), (144, 88), (129, 86), (108, 84), (89, 85), (80, 100), (74, 106), (70, 111), 
(64, 127), (64, 141), (63, 163), (63, 179), (62, 197), (61, 214), (61, 233), (61, 247), (61, 265), (61, 277), (61, 286), 
(61, 298), (60, 309), (59, 334), (59, 350), (59, 379), (59, 399), (58, 418), (58, 435), (58, 456), (62, 474), (75, 485), 
(82, 494), (93, 506), (105, 519), (118, 535), (127, 542), (149, 562), (156, 573), (162, 578), (173, 589), (187, 607), 
(202, 617), (216, 630), (231, 647), (254, 666), (264, 675), (279, 692), (298, 708), (312, 716), (331, 721), (351, 723), 
(367, 722), (380, 709), (397, 694), (404, 668), (404, 641), (405, 605), (405, 585), (407, 548), (413, 536), (426, 515), 
(437, 505), (454, 495), (476, 488), (497, 485), (522, 487), (554, 497), (573, 513), (586, 530), (590, 551), (593, 574), 
(593, 597), (593, 621), (596, 645), (601, 662), (606, 683), (616, 701), (631, 716), (646, 718), (657, 720), (679, 719), 
(704, 715), (714, 707), (725, 692), (725, 663), (733, 650), (735, 620), (734, 592), (734, 567), (733, 540), (733, 518), 
(733, 502), (730, 478), (731, 451), (728, 418), (724, 393), (716, 384), (704, 376), (683, 367), (650, 364), (619, 361), 
(596, 361), (573, 362), (543, 362), (519, 363), (488, 360), (451, 351), (420, 345), (411, 334), (406, 317), (401, 296),
 (408, 284), (423, 270), (442, 261), (466, 261), (486, 260), (507, 260), (530, 259), (542, 259), (568, 258), (600, 256), 
 (625, 257), (649, 257), (673, 256), (695, 253), (703, 249), (717, 242), (725, 232), (729, 218), (732, 208), (734, 182), 
 (734, 169), (734, 150), (732, 128), (732, 123), (727, 101), (712, 87), (694, 82), (653, 79), (637, 79), (606, 77), (587, 77),
  (566, 77), (549, 77), (530, 77), (508, 77), (478, 77), (454, 77), (432, 77), (417, 76), (393, 76), (370, 76), (347, 77), (322, 79), 
  (307, 87), (293, 95), (289, 119), (288, 136), (282, 151), (278, 176), (278, 190), (278, 205), (277, 215), (277, 228), (277, 251),
   (277, 273), (277, 291), (277, 310), (275, 334), (273, 356), (268, 374), (255, 397), (241, 400), (225, 399), (194, 387), (183, 368), 
   (180, 355), (178, 340), (175, 319), (175, 292), (174, 264)]

def distance(point1, point2):
    px = (float(point1[0])-float(point2[0]))**2
    py = (float(point1[1])-float(point2[1]))**2
    return (px+py)**(0.5)

class RacecarNode():
    def __init__(self, state):
      self.state = state      #[speed, x, y, theta]
      self.terminal = False

      
    def find_children(self):
        if self.is_terminal():  # If the game is finished then no moves can be made
            return set()
        # Otherwise, you can make a move in each of the empty spots
        return {
            self.take_action(i) for i in self.possible_actions()
        }
        # must return list/set of all possible actions from current state #

    def f(self, state, t, phi, acceleration): # y = [speed, x, y, theta]
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

    def update(self, state, steering, acceleration): # state is [speed, x, y, theta] where x and y and the midpoint between the rear wheels
      t = np.linspace(0, 0.02, 2)
      return odeint(self.f, self.state, t, args=(steering, acceleration))[-1]

    def possible_actions(self):
      actions = []
      steering = [0, .1, -.1]
      acceleration = [0, .2, -.2]
      for i in steering:
        #for j in acceleration:
         actions.append(self.update(self.state, i, 0))
      #print("actions", actions)
      return actions


    def find_random_child(self):
        if self.is_terminal():
            return None  # If the game is finished then no actions can be taken
        possible_actions = self.possible_actions()
        return self.take_action(choice(possible_actions))
        # must return a random child from all possible actions #

    def reward(self):
        if not self.is_terminal():
            return(self.closest_node())
        else:
            return(self.closest_node()*-1)  # Crash

        # numbers can (should) be adjusted, returns big penalty if crash and
        # returns reward based on distance traveled otherwise #


    def is_terminal(self):
        if robot_motion.collide(self.state[1], self.state[2], self.state[3]) is not None:
            self.terminal = True
            return True
        else:
            self.terminal = False
            return False

    def closest_node(self):
        x = self.state[1]
        y = self.state[2]
        current = (x,y)
        min = distance(path[0],current)
        #print("current", current)
        nodeid = 0
        for i in range(len(path)):
            if distance(current, path[i]) < min:
                min= distance(current, path[i])
                nodeid = i
        #print(path[nodeid])
        return((nodeid+10)*20)
    

    def take_action(self, action):
      return(RacecarNode(action))



def play_game():
      tree = MCTS()
      track = RacecarSim()
      while True:
          # Adjust number of sims below for thinking time #
          for _ in range(10):
              tree.do_rollout(track)
          track = tree.choose(track)
          if track.is_terminal():
              break

if __name__ == "__main__":
    play_game()

