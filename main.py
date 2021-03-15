import os

import arcade
import math

SCREEN_TITLE = "torti flying Tortoise v0.1.0"

# Size of screen to show, in pixels
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

# direction consts
LEFT = 0
RIGHT = 1


class Torti(arcade.Sprite):
    def __init__(self, image, scale):
        """ Set up the player """

        # Call the parent init
        super().__init__(image, scale)

        # Create a variable to hold our speed. 'angle' is created by the parent
        # constants
        self._start_velocity = 10.0
        self._deceleration = -2.5
        self._redirection_speed = 0.5
        self._stop_strength = 0.5

        self._direction = (0.0, 0.0)
        self._position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self._velocity = 0.0

    def impulse(self):
        pass

    def stop(self):
        self._velocity -= self._velocity * self._stop_strength

    def update(self):
        # Convert angle in degrees to radians.
        angle_rad = math.radians(self.angle)

        # Rotate the ship
        self.angle += self.change_angle

        # Use math to find our change based on our speed and angle
        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)


class GameWindow(arcade.Window):
    """ Main Window """

    def __init__(self, width, height, title):
        """ Create the variables """

        # Init the parent class
        super().__init__(width, height, title)

        # set file paths for sprite imports
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.b = None
        self.torti_sprite = None
        self.sprite_list = None

        arcade.set_background_color(arcade.color.BLACK_OLIVE)

    def setup(self):
        """ Set up everything with the game """
        self.sprite_list = arcade.SpriteList()
        self.torti_sprite = Torti('images/torti-sprite.png', 1.0)
        self.torti_sprite.center_x = (SCREEN_WIDTH / 2)
        self.torti_sprite.center_y = (SCREEN_HEIGHT / 2)
        self.sprite_list.append(self.torti_sprite)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP:
            self.b.impulse()
        elif key == arcade.key.DOWN:
            self.b.stop()

            # Rotate left/right
        elif key == arcade.key.LEFT:
            self.player_sprite.change_angle = ANGLE_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_angle = -ANGLE_SPEED

        def on_key_release(self, key, modifiers):
            """Called when the user releases a key. """

            if key == arcade.key.UP or key == arcade.key.DOWN:
                self.player_sprite.speed = 0
            elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
                self.player_sprite.change_angle = 0

    def on_update(self, delta_time):
        """ Movement and game logic """
        pass

    def on_draw(self):
        """ Draw everything """
        self.sprite_list.draw()



def main():
    """ Main method """
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
