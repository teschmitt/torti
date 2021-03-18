class KeyListener:
    """

    Interface class for objects subscribed to keypresses somewhere
    This might be a bit overkill, but it's fun so whatever

    """

    def handle_key_inputs(self):
        pass

    def key_press(self, key, modifier):
        pass

    def key_release(self, key, modifier):
        pass
