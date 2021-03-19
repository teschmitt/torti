import arcade
from arcade.experimental.shadertoy import ShaderToy

"""
This is all the fantastic work of Romuald Grignon [FR] from the Pyton Arcade Discord server.
See: https://discord.com/channels/458662222697070613/716020595439173663/810473538896134164
"""


class TestArcade(arcade.Window):

    def __init__(self, width, height, title, full_screen):
        # Init application window
        super().__init__(width, height, title, full_screen)
        # Set application window background color
        arcade.set_background_color(arcade.color.BLACK)

        # open file and store source
        fp = open("../resources/shaders/water.glsl", "r")
        source = "".join(fp.readlines())
        fp.close()

        self._shader = ShaderToy(source)
        self._time = 0

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()
        self._shader.draw(self._time)

    def update(self, delta_time):
        self._time += delta_time

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.close()


def main():
    game = TestArcade(800, 600, "Test Shader Toy", False)
    game.set_vsync(True)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
