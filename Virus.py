import arcade


VIRUS_SPEED = 1


def load_texture(filename):
    return arcade.load_texture(filename)


class Virus(arcade.Sprite):
    def __init__(self, way):
        super().__init__()
        self.way = way
        self.texture = load_texture(f"data//img//virus.png")
