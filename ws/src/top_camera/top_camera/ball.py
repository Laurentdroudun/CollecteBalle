import cv2 as cv
import numpy as np
from zenith_camera_subscriber import *

class Ball:
    def __init__(self,timeStamp,X,id):
        self.time=timeStamp
        self.score=0
        self.position=X
        self.id=id

class TerrainBalls:
    def __init__(self,timeStamp):
        self.time=timeStamp
        self.score=0
        self.terrain=None
        self.balls=[]
        rclpy.init()
        self.Camera=ZenithCameraSubscriber(self.update)
        # rclpy.spin_once(self.Camera)
        rclpy.spin(self.Camera)

    
    def detect_balls(self):
        frame_HSV = cv.cvtColor(self.terrain, cv.COLOR_BGR2HSV)
        frame_threshold = cv.inRange(frame_HSV, (24, 1, 1), (51, 255, 255))
        ret,thresh = cv.threshold(frame_threshold,127,255,cv.THRESH_BINARY)
        contours,h = cv.findContours(thresh,cv.RETR_CCOMP,cv.CHAIN_APPROX_NONE)
        ball_centers=[]
        for cnt in contours:
            (cx, cy), radius = cv.minEnclosingCircle(cnt)
            ball_centers.append([int(cx),int(cy)])
            cv.drawContours(self.terrain, [cnt], 0, (0, 0, 255), -1)
        for i in range(len(ball_centers)):
            b=Ball(self.time,ball_centers[i],i)
            self.balls.append(b)
            cv2.putText(self.terrain, str(b.time), tuple(b.position), cv2.FONT_HERSHEY_SIMPLEX,
            1, (255,255,0), 1, cv2.LINE_AA)
            # self.isolatedBalls=img
    
    def show_balls(self):
        cv.imshow('Terrain',self.terrain)
        cv.waitKey(1)
    
    def __del__(self):
        self.Camera.destroy_node()
        cv.destroyAllWindows()
        rclpy.shutdown()

    def update(self,img,timeStamp):
        self.terrain=img
        self.time=timeStamp
        self.detect_balls()
        self.show_balls()


t=TerrainBalls(0)

t.Camera.destroy_node()
