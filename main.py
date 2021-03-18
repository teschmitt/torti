import os

import arcade

from KeyListener import KeyListener
from Torti import Torti

SCREEN_TITLE = "torti flying Tortoise v0.1.0"

# Size of screen to show, in pixels
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900


class GameWindow(arcade.Window):
    """ Main Window """

    def __init__(self, width, height, title):
        """ Create the variables """

        # Init the parent class
        super().__init__(width, height, title)

        # set file paths for sprite imports
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.torti_sprite = None
        self.sprite_list = None
        self.wall_list = None
        self.key_listeners = None
        self.physics_engine = None

        arcade.set_background_color(arcade.color.OCEAN_BOAT_BLUE)

    def setup(self):
        """ Set up everything with the game """
        self.sprite_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # set up walls around the view to enable collision detection
        x = 5
        w = 20
        for wall_pos in ((SCREEN_WIDTH / 2, -x, SCREEN_WIDTH, w),
                         (SCREEN_WIDTH / 2, SCREEN_HEIGHT + x, SCREEN_WIDTH, w),
                         (-x, SCREEN_HEIGHT / 2, w, SCREEN_HEIGHT),
                         (SCREEN_WIDTH + x, SCREEN_HEIGHT / 2, w, SCREEN_HEIGHT)):
            wall_sprite = arcade.SpriteSolidColor(width=wall_pos[2], height=wall_pos[3],
                                                  color=arcade.color.WHITE)
            wall_sprite.center_x = wall_pos[0]
            wall_sprite.center_y = wall_pos[1]
            self.wall_list.append(wall_sprite)

        self.torti_sprite = Torti(
            'images/torti-sprite.png',
            1.5,
            (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
            self.sprite_list
        )
        self.sprite_list.append(self.torti_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(self.torti_sprite, self.wall_list)

        self.key_listeners = []
        self.key_listeners.append(self.torti_sprite)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        for listener in self.key_listeners:
            listener.key_press(key, modifiers)

    def on_key_release(self, key: int, modifiers: int):
        """Called when the user releases a key. """

        for listener in self.key_listeners:
            listener.key_release(key, modifiers)

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.sprite_list.update()
        self.physics_engine.update()

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.sprite_list.draw()
        # self.sprite_list.draw_hit_boxes()
        self.wall_list.draw()

        # arcade.draw_text(f'{self.hit_list}', 10, 20, arcade.color.WHITE, 14)


def main():
    """ Main method """
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
