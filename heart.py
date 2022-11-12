# Author: Pengkun Jiao
# Date:   2022/11/12

import math
import time
import turtle
import numpy as np

class Heart():
    def __init__(self):

        self.turtle = turtle
        self.turtle.title('My heart')  
        self.turtle.setup(800, 600)  
        self.turtle.tracer(0) 
        self.turtle.bgcolor("black") 
        self.turtle.hideturtle() 
        self.turtle.pensize(1) 
        self.turtle.pencolor('white')

        self.color = 'white' #[255, 255, 255]
        self.heart_size = 6 
        self.dot_size = 2

        self.num_points, self.points = self.get_heart_curve_points(d=0.01)

    def heart_curve_function(self, t):
        """
         Heart curve function is from: https://mathworld.wolfram.com/HeartCurve.html

        """
        x = 16 * math.pow(math.sin(t), 3)
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        return [x, y]

    def get_heart_curve_points(self, d=0.01):
        num_points = int(2*math.pi / d)
        points = []
        t = 0
        for i in range(num_points):
            points.append(self.heart_curve_function(t))
            t += d
        return num_points, points

    def get_mask(self, p):
        return np.random.choice([0, 1], size=self.num_points, p=[p, 1-p])

    def draw_point(self, x, y):
        self.turtle.penup()
        self.turtle.setx(x) 
        self.turtle.sety(y)
        self.turtle.pendown()
        self.turtle.dot(self.dot_size) 
        
    def draw_heart_shape(self, size=10, mask=None):
        for i in range(self.num_points):
            if mask[i]:
                continue
            self.draw_point(self.points[i][0] * size, self.points[i][1] * size)      

    def draw_full_heart(self, beat_size=0, beat_range=1, frame=0):

        diffusion_d = 0.02

        # inner
        self.dot_size = 2
        diffusion_t = 0
        for i in range(int(math.pi /2 / diffusion_d)):
            diffusion_size = math.cos(diffusion_t)
            density = 0.04  * math.pow(diffusion_size, 4)
            size=(self.heart_size+beat_size*beat_range) * diffusion_size
            mask = self.get_mask(p=density)
            self.draw_heart_shape(size=size, mask=mask)
            diffusion_t += diffusion_d

        # outer
        self.dot_size = 1   
        diffusion_t = - math.pi / 8
        density = 0.02
        mask = self.get_mask(p=density)
        while diffusion_t < math.pi / 10:
            diffusion_size = math.sin(diffusion_t)
            size=(self.heart_size+beat_size*1) * (diffusion_size + 1)
            mask = self.get_mask(p=density)
            self.draw_heart_shape(size=size, mask=mask)
            diffusion_t += diffusion_d

    def beat(self):
        intervals = 1/120
        frame = 0 
        beat_d = 0.1
        beat_t = 0
        while True:
            self.turtle.clear()
            beat_size = math.sin(beat_t)
            self.draw_full_heart(beat_size, 1, frame)
            self.turtle.update()
            time.sleep(intervals)
            beat_t += beat_d
            frame += 1
            print('frame:', frame)      
        

my_heart = Heart()
my_heart.beat()