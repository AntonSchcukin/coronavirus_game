import arcade
import random
import time
import typing
from Virus import *


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Победи коронавирус!'
fields_number = 4
VIRUS_SPEED = -1
score = 0


class Game(arcade.Window):
    def __init__(self, width, height):
        super(Game, self).__init__(width, height, SCREEN_TITLE)
        self.background = None
        self.music = arcade.Sound(f'data//sound//bg_music.mp3')
        self.sound_kill_virus = arcade.Sound('data//sound//kill_virus.wav')
        self.sound_game_over_scream = arcade.Sound('data//sound//game_over_scream.mp3')
        self.game_over = False

    def setup(self):
        self.virus_list = arcade.SpriteList()
        self.background = arcade.load_texture("data//img//bg.png")
        self.music.play(0.1)

        self.view_left = 0
        self.view_bottom = 0

    def on_mouse_press(self, x, y, virus, key_modifiers):
        if not self.game_over:
            global score
            hit_sprites = arcade.get_sprites_at_point((x, y), self.virus_list)
            for sprite in hit_sprites:
                virus_sprite = typing.cast(Virus, sprite)
                if virus == arcade.MOUSE_BUTTON_LEFT:
                    virus_sprite.remove_from_sprite_lists()
                    self.sound_kill_virus.play(0.3)
                    score += 1

    def on_draw(self):
        arcade.start_render()
        if not self.game_over:
            arcade.draw_lrwh_rectangle_textured(0, 0,
                                                SCREEN_WIDTH, SCREEN_HEIGHT,
                                                self.background)

            for x in range(SCREEN_WIDTH // fields_number, SCREEN_WIDTH, SCREEN_WIDTH // fields_number):
                arcade.draw_line(x, 0, x, SCREEN_HEIGHT, arcade.color.BLACK, 4)
            self.virus_list.draw()
            arcade.draw_text(str(score), self.view_left + 10, self.view_bottom + SCREEN_HEIGHT - 30,
                             arcade.csscolor.BLACK, 20)
        else:
            arcade.draw_lrtb_rectangle_filled(left=0,
                                              right=SCREEN_WIDTH,
                                              top=SCREEN_HEIGHT,
                                              bottom=0,
                                              color=arcade.color.ORANGE + (200,))
            arcade.draw_text('Вы заболели!', self.view_left + 60, self.view_bottom + SCREEN_HEIGHT - 100,
                             arcade.csscolor.BLACK, 40)
            arcade.draw_text(f'Вирусов убито: {score}', self.view_left + 60, self.view_bottom + SCREEN_HEIGHT - 140,
                             arcade.csscolor.BLACK, 20)
            arcade.draw_text('Нажмите ПРОБЕЛ чтобы продолжить', self.view_left + 5, self.view_bottom + 140,
                             arcade.csscolor.WHITE, 20)

    def on_key_press(self, key, modifiers):
        if self.game_over and key == arcade.key.SPACE:
            global score
            score = 0
            self.virus_list = arcade.SpriteList()
            self.music.play(0.1)
            self.game_over = False

    def on_update(self, delta_time):
        if not self.game_over:
            global score, VIRUS_SPEED, kill_virus
            if random.randrange(50) == 0:
                virus = Virus(random.choice(range(fields_number)))
                virus.center_x = virus.way * SCREEN_WIDTH // fields_number + 50
                virus.center_y = SCREEN_HEIGHT + 50
                virus.change_y = VIRUS_SPEED - (score / 10)
                self.virus_list.append(virus)

            position = self.music.get_stream_position()
            if position == 0.0:
                self.music.play(0.1)

            for virus in self.virus_list:
                if virus.center_y <= 0:
                    self.game_over = True
                    self.music.stop()
                    virus.remove_from_sprite_lists()
                    self.sound_game_over_scream.play(0.2)
                    break

            self.virus_list.update()


def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == '__main__':
    main()
