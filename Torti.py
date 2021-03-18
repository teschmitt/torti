import math

import arcade

# direction consts
from KeyListener import KeyListener

LEFT = 1
RIGHT = -1
FORWARD = 1
BACKWARD = -1

LATERAL = 0
TURN = 1

START_TURN_SPEED = 7.0
TURN_DECAY = 0.1
TURN_FAST_THRESH = 1.5
TURN_STOP_THRESH = 0.1

START_SPEED = 10.0
SPEED_DECAY = 0.09
SPEED_FAST_THRESH = 2.0  # lower bound to re-energize when button stays pressed
SPEED_STOP_THRESH = 0.1  # lower bound to stop after button is released

REDIRECTION_SPEED = 0.5
STOP_STRENGTH = 0.5


class Torti(arcade.Sprite, KeyListener):
    """

    Class for a drawing character. Listens for pressed keys that are published by the caller

    Args:
        image (str): path to image file used for this sprite
        scale (float): scale of image
        pos (tuple): (x, y) tuple of initial position

    Attributes:
        no public attributes

    """

    def __init__(self, image: str, scale: float, pos: tuple, top_sprite_list: arcade.SpriteList) -> None:
        """ Set up the player """

        # Call the parent init
        super().__init__(image, scale)

        self._direction = 0
        self._turn_direction = 0

        # moving list shows us if Torti is moving in a certain direction:
        self._moving = [False, False]

        self._start_position = pos
        self.position = pos
        self.brush_trail = top_sprite_list
        self._speed = 0.0

        # set of currently pressed keys
        self.keys_pressed = set()

    def key_press(self, key, modifier):
        self.keys_pressed.add(key)

    def key_release(self, key, modifier):
        try:
            self.keys_pressed.remove(key)
        except KeyError as e:
            print(f'Key {key} with modifier {modifier} not found in keys_pressed set: {e}')

    def impulse(self, direction):
        self._direction = direction
        self._speed = START_SPEED

    def reset_position(self):
        self.center_x, self.center_y = self._start_position
        self._speed = 0
        self.change_angle = 0

    def stop(self):
        self._speed -= self._speed * STOP_STRENGTH

    def turn(self, direction: int):
        self._turn_direction = direction
        self.change_angle = START_TURN_SPEED

    def update(self):
        # Handle key-presses and releases
        if self.keys_pressed:
            self.handle_key_inputs()

        if arcade.key.ESCAPE in self.keys_pressed:
            self.reset_position()

        # Handle movement
        if self.change_angle > 0:
            self._moving[TURN] = True
            self.angle += self._turn_direction * self.change_angle

            # keep angle between 0 and 360
            if self.angle >= 360 or self.angle < 0:
                self.angle -= self._turn_direction * 360

            self.change_angle -= self.change_angle * TURN_DECAY
            if self.change_angle < TURN_STOP_THRESH:
                self.change_angle = 0
                self._moving[TURN] = False

        if self._speed > 0:
            traildot = arcade.SpriteCircle(
                radius=10, color=arcade.color.WHITE,
            )
            traildot.center_x, traildot.center_y = self.center_x, self.center_y
            self.brush_trail.append(traildot)
            # Convert angle in degrees to radians.
            angle_rad = math.radians(self.angle)
            self._moving[LATERAL] = True

            self.center_x += -self._direction * self._speed * math.sin(angle_rad)
            self.center_y += self._direction * self._speed * math.cos(angle_rad)
            self._speed -= self._speed * SPEED_DECAY
            if self._speed < SPEED_STOP_THRESH:
                self._speed = 0
                self._moving[LATERAL] = False

    def handle_key_inputs(self) -> None:
        if arcade.key.UP in self.keys_pressed:
            self.impulse(FORWARD)
        elif arcade.key.DOWN in self.keys_pressed:
            self.impulse(BACKWARD)

        if arcade.key.LEFT in self.keys_pressed:
            self.turn(LEFT)
        elif arcade.key.RIGHT in self.keys_pressed:
            self.turn(RIGHT)
