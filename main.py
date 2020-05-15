import arcade
import random
import time
from Virus import *


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Победи коронавирус!'
fields_number = 4
score = 0


class Game(arcade.Window):
    def __init__(self, width, height):
        super(Game, self).__init__(width, height, SCREEN_TITLE)
        self.background = None
        self.music = arcade.Sound(f'data//sound//bg_music.mp3')

    def setup(self):
        self.virus_list = arcade.SpriteList()
        self.background = arcade.load_texture("data//img//bg.png")
        self.music.play(0.1)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        for x in range(SCREEN_WIDTH // fields_number, SCREEN_WIDTH, SCREEN_WIDTH // fields_number):
            arcade.draw_line(x, 0, x, SCREEN_HEIGHT, arcade.color.BLACK, 4)
        self.virus_list.draw()

    def on_update(self, delta_time):
        if random.randrange(200) == 0:
            virus = Virus(random.choice(range(fields_number)))
            virus.center_x = virus.way * SCREEN_WIDTH // fields_number + 50
            virus.center_y = SCREEN_HEIGHT + 50
            virus.change_y = -VIRUS_SPEED + score // 10
            self.virus_list.append(virus)
        for virus in self.virus_list:
            if virus.center_y == 0:
                virus.remove_from_sprite_lists()
        self.virus_list.update()

        position = self.music.get_stream_position()
        if position == 0.0:
            self.music.play(0.1)


def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == '__main__':
    main()
