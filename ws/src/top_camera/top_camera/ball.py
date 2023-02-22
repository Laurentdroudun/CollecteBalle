import cv2 as cv
import numpy as np


class Ball:
    def __init__(self, id, timestamp, X):
        self.time0 = timestamp
        self.elapsed_time = 0
        self.score = 0
        self.position = X
        self.id = id

    def get_score(self, robot_position=(0, 0)):
        """
            Closer the ball is to the robot, higher the score

            :param robot_position: (x, y) tuple [in pixels, relative to the top left corner of the image]

            :return: score: float
        """
        distance_coeff = 1
        time_coeff = 10

        distance = np.linalg.norm(
            np.array(self.position) - np.array(robot_position)
        )

        self._score = 1 / (distance_coeff * distance +
                           time_coeff * self.elapsed_time)

        # print("distance: ", distance, "time_diff: ",
        #       time_diff, "score: ", self._score)

        return self._score

    def set_position(self, X):
        self.position = X

    def set_time(self, timestamp):
        self.elapsed_time = timestamp - self.time0
