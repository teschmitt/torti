import arcade
import math

from KeyListener import KeyListener

CCLOCKW = 1
CLOCKW = -1
FORWARD = 1
BACKWARD = -1

LATERAL = 0
TURN = 1

START_TURN_SPEED = 2.0
TURN_DECAY = 0.1
TURN_FAST_THRESH = 1.5
TURN_STOP_THRESH = 0.1

START_SPEED = 5.0
SPEED_DECAY = 0.1
SPEED_FAST_THRESH = 2.0  # lower bound to re-energize when button stays pressed
SPEED_STOP_THRESH = 0.1  # lower bound to stop after button is released

REDIRECTION_SPEED = 0.5
STOP_STRENGTH = 0.5

# Bubble emitter constants
DEFAULT_SCALE = 0.15
DEFAULT_ALPHA = 64
DEFAULT_PARTICLE_LIFETIME = 3.0
PARTICLE_SPEED_FAST = 1.0
PARTICLE_SPEED_SLOW = 0.3
DEFAULT_EMIT_INTERVAL = 0.2
DEFAULT_EMIT_DURATION = 0.5
TEXTURE = ":resources:images/pinball/pool_cue_ball.png"

BUBBLE_OFFSET_X = 10
BUBBLE_OFFSET_Y = 10


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

    def __init__(self, image: str, scale: float, pos: tuple, top_sprite_list) -> None:
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
        self.brush_active = True
        self._speed = 0.0

        # field for the current angle in radians
        self.angle_rad = math.radians(self.angle)

        # self.bubble_emitters = bubble_emitters
        self.bubbles = arcade.Emitter(
            center_xy=(self.center_x, self.center_y),
            emit_controller=arcade.EmitInterval(DEFAULT_EMIT_INTERVAL),
            particle_factory=lambda emitter: arcade.LifetimeParticle(
                filename_or_texture=TEXTURE,
                change_xy=arcade.rand_in_circle((0.0, 0.0), PARTICLE_SPEED_FAST),
                lifetime=1.0,
                scale=DEFAULT_SCALE,
                alpha=DEFAULT_ALPHA
            )
        )

        # set of currently pressed keys
        self.keys_pressed = set()

        print(TEXTURE)

    def key_press(self, key, modifier):
        self.keys_pressed.add(key)

    def key_release(self, key, modifier):
        try:
            self.keys_pressed.remove(key)
        except KeyError as e:
            print(f'Key {key} with modifier {modifier} not found in keys_pressed set: {e}')

    def impulse(self, direction):
        self._moving[LATERAL] = True
        self._direction = direction
        self._speed = START_SPEED

    def reset_torti(self):
        self.center_x, self.center_y = self._start_position
        self.reset_movement()
        remove_list = [s for s in self.brush_trail]
        for s in remove_list:
            self.brush_trail.remove(s)

    def stop(self):
        self._speed -= self._speed * STOP_STRENGTH

    def turn(self, direction: int):
        self._moving[TURN] = True
        self._turn_direction = direction
        self.change_angle = self._turn_direction * START_TURN_SPEED

    # def draw(self):
    #     super().draw()
    #     self.bubbles.draw()

    def update(self):
        # Handle key-presses and releases
        if self.keys_pressed:
            self.handle_key_inputs()

        # Handle Rotation
        if self.change_angle != 0:
            self.change_angle -= self.change_angle * TURN_DECAY

            if (self._turn_direction * TURN_STOP_THRESH) - (self._turn_direction * self.change_angle) > 0:
                self.change_angle = 0
                self._moving[TURN] = False

        # Handle movement
        if self._speed > 0:
            # draw the brush trail behind Torti
            traildot = arcade.SpriteCircle(
                radius=10, color=arcade.color.WHITE, soft=True
            )
            traildot.center_x, traildot.center_y = self.center_x, self.center_y
            if self.brush_active:
                self.brush_trail.append(traildot)

            self.change_x = -self._direction * self._speed * math.sin(self.angle_rad)
            self.change_y = self._direction * self._speed * math.cos(self.angle_rad)
            self._speed -= self._speed * SPEED_DECAY

            if self._speed < SPEED_STOP_THRESH:
                self.reset_movement()
                self._moving[LATERAL] = False

        # Convert angle in degrees to radians.
        self.angle_rad = math.radians(self.angle)
        self.update_bubbles()

    def update_bubbles(self):
        # update bubbles to track head
        self.bubbles.center_x = self.center_x - math.sin(self.angle_rad) * (BUBBLE_OFFSET_X + self.width / 2)
        self.bubbles.center_y = self.center_y + math.cos(self.angle_rad) * (BUBBLE_OFFSET_Y + self.height / 2)

    def handle_key_inputs(self) -> None:
        if arcade.key.UP in self.keys_pressed:
            self.impulse(FORWARD)
        elif arcade.key.DOWN in self.keys_pressed:
            self.impulse(BACKWARD)

        if arcade.key.LEFT in self.keys_pressed:
            self.turn(CCLOCKW)
        elif arcade.key.RIGHT in self.keys_pressed:
            self.turn(CLOCKW)

        if arcade.key.SPACE in self.keys_pressed:
            self.brush_active = True
        else:
            self.brush_active = False

        if arcade.key.ESCAPE in self.keys_pressed:
            self.reset_torti()

    def reset_movement(self):
        self._speed, self.change_x, self.change_y = 0.0, 0.0, 0.0
        self._speed = 0
        self.change_angle = 0
