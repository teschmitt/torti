import os

import arcade

from torti import Torti

SCREEN_TITLE = "torti flying Tortoise v0.1.0"

# Size of screen to show, in pixels
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

# direction consts
LEFT = 1
RIGHT = -1


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
        self.torti_sprite = Torti(
            'images/torti-sprite.png',
            1.0,
            (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.sprite_list.append(self.torti_sprite)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP:
            self.torti_sprite.impulse()
        elif key == arcade.key.DOWN:
            self.torti_sprite.stop()

            # Rotate left/right
        elif key == arcade.key.LEFT:
            self.torti_sprite.turn(LEFT)
        elif key == arcade.key.RIGHT:
            self.torti_sprite.turn(RIGHT)

        elif key == arcade.key.ESCAPE:
            self.torti_sprite.reset_position()

    def on_key_release(self, key: int, modifiers: int):
        """Called when the user releases a key. """

        # if key == arcade.key.UP or key == arcade.key.DOWN:
        #     self.torti_sprite.speed = 0
        # elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
        #     self.torti_sprite.change_angle = 0

        pass

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.sprite_list.update()

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.sprite_list.draw()
        arcade.draw_text(f'{self.torti_sprite.angle}', 10, 20, arcade.color.WHITE, 14)


def main():
    """ Main method """
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
