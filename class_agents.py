import math
import pygame
import numpy as np
import random
import time
class agent():
    def __init__(self,screen,init_x,init_y):
        self.pos_x = init_x
        self.pos_y = init_y
        self.coordinate = (self.pos_x,self.pos_y)
        self.speed = 4
        self.cooldown = 0
        self.screen = screen
        self.head_color = (0,200,0)
        self.radius = 30
        self.point = 0
        self.last_eat_time = time.time()
        self.time_since_last_eat = 0
        
    def draw_agent(self):
        pygame.draw.circle(self.screen,self.head_color,(self.pos_x,self.pos_y),self.radius)
    
    def movement(self,closer_food):
        if(self.cooldown > 0):
            self.cooldown -= 1
            return
        target_x,target_y = closer_food.get_coordinate()
        rounded_agent_x = round(self.pos_x,2)
        rounded_agent_y = round(self.pos_y,2)
        rounded_food_x = round(target_x,2)
        rounded_food_y = round(target_y,2)
        #calcular posição atual pela do alvo
        dx = rounded_food_x - rounded_agent_x
        dy = rounded_food_y - rounded_agent_y
        distance = np.sqrt(dx**2 + dy**2)
        
        if distance <= self.speed + 1:
            self.pos_x,self.pos_y =  target_x,target_y
            self.cooldown += 20
            self.points()
            closer_food.randomize()
            self.last_eat_time = time.time()
        else:
            ratio = self.speed/ distance
            step_x = dx * ratio
            step_y = dy * ratio
            #att posicao
            self.pos_x += step_x
            self.pos_y += step_y
        self.coordinate =(self.pos_x,self.pos_y)
        
    def points(self):
        self.point+=1
        if (self.point % 8 == 0):
            self.speed += .5
    
    def get_coordinate(self):
        return self.coordinate
    
    def calculate_time_since_last_eat(self):
        current_time = time.time()
        self.time_since_last_eat = current_time - self.last_eat_time
        return self.time_since_last_eat
    
class food():
    def __init__(self, screen, range_x, range_y,agent):
        self.x_screen_range = range_x
        self.y_screen_range = range_y
        self.radius = 10
        self.pos_x = int(np.random.uniform(self.radius, self.x_screen_range - self.radius,1))
        self.pos_y = int(np.random.uniform(self.radius, self.y_screen_range - self.radius,1))
        self.screen = screen
        self.color = (0, 0, 0)
        self.agent = agent
        self.speed_x = 7
        self.speed_y = 5
        self.delay_timer = None  # Temporizador para controlar o atraso da comida
        self.delay_duration = 2000  # Duração do atraso em milissegundos (1 segundo)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.pos_x, self.pos_y), self.radius)
    
    def get_coordinate(self):
        return (self.pos_x,self.pos_y)
    
    
    def verify_points(self):
        if self.agent.point % 10 == 0:
            self.speed_x += .5
            self.speed_y += .2
    
    def is_being_chased(self):
        agent_pos = self.agent.get_coordinate()
        ball_posicion = self.get_coordinate()
        
        dx = ball_posicion[0]-agent_pos[0]
        dy = ball_posicion[1] - agent_pos[1]
        
        
        distance = np.sqrt(dx**2 + dy **2)
        print(distance)
        if distance <= 120:
            return True
        else:
            return False
    
    def move_away_from_agent(self):
        if self.is_being_chased():
            agent_pos = self.agent.get_coordinate()
            agent_x = agent_pos[0]
            agent_y = agent_pos[1]
            
            dx = self.pos_x - agent_x
            dy = self.pos_y - agent_y
            
            #normalize a direção, para se obter a mesma velocidade
            magnitude = np.sqrt(dx**2 + dy**2)
            dx /= magnitude
            dy /= magnitude
            
            self.pos_x += self.speed_x * dx
            self.pos_y += self.speed_y * dy
            
            self.bounce()
            
            
    def bounce(self):
        if self.pos_x <= 0 or self.pos_x >= self.x_screen_range:
                self.speed_x *= -1
                return True    
        if self.pos_y <= 0 or self.pos_y >= self.y_screen_range:
                self.speed_y *= -1
                return True    
                
    def get_coordinate(self):
        return (self.pos_x, self.pos_y)
    
    def randomize(self):
        self.verify_points()
        self.pos_x = int(np.random.uniform(self.radius, self.x_screen_range - self.radius,1))
        self.pos_y = int(np.random.uniform(self.radius, self.y_screen_range - self.radius,1))
        return True