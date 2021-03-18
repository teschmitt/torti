import math

import arcade

LATERAL = 0
TURN = 1


class Torti(arcade.Sprite):

    def __init__(self, image, scale, pos):
        """ Set up the player """

        # Call the parent init
        super().__init__(image, scale)

        # Create a variable to hold our speed. 'angle' is created by the parent
        # constants
        self._start_turn_speed = 7.0
        self._turn_decay = 0.1
        self._turn_stop_thresh = 0.1
        self._turn_direction = 1

        self._start_speed = 10.0
        self._speed_decay = 0.1
        self._speed_stop_thresh = 0.1

        self._redirection_speed = 0.5
        self._stop_strength = 0.5

        self._direction = (0.0, 0.0)

        # moving list shows us if Torti is moving in a certain direction:
        self._moving = [False, False]

        self._start_position = pos
        self._speed = 0.0

    def impulse(self):
        self._speed = self._start_speed

    def reset_position(self):
        self.center_x, self.center_y = self._start_position
        self._speed = 0
        self.change_angle = 0

    def stop(self):
        self._speed -= self._speed * self._stop_strength

    def turn(self, direction: int):
        self._turn_direction = direction
        self.change_angle = self._start_turn_speed

    def update(self):
        # Rotate the ship
        if self.change_angle > 0:
            self._moving[TURN] = True
            self.angle += self._turn_direction * self.change_angle

            # keep angle between 0 and 360
            if self.angle >= 360 or self.angle < 0:
                self.angle -= self._turn_direction * 360

            self.change_angle -= self.change_angle * self._turn_decay
            if self.change_angle < self._turn_stop_thresh:
                self.change_angle = 0
                self._moving[TURN] = False



        if self._speed > 0:
            # Convert angle in degrees to radians.
            angle_rad = math.radians(self.angle)
            self._moving[LATERAL] = True

            self.center_x += -self._speed * math.sin(angle_rad)
            self.center_y += self._speed * math.cos(angle_rad)
            self._speed -= self._speed * self._speed_decay
            if self._speed < self._speed_stop_thresh:
                self._speed = 0
                self._moving[LATERAL] = False
