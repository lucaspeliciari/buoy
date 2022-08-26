import sys

from pygame import constants as constant
import pygame.display

from constants import TIMESCALE
from util.vectors import Vector2



class Handler:
    def __init__(self):
        self.selected = 0

    def handle(self, engine, events,  keys, buoys):
        key_value = 1
        if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT] or (pygame.key.get_mods() & constant.KMOD_LSHIFT) or (
                pygame.key.get_mods() & constant.KMOD_RSHIFT):
            key_value = 100

        # BUOYS
        if keys[constant.K_DOWN]:
            buoys[self.selected].position.y += key_value
        if keys[constant.K_UP]:
            buoys[self.selected].position.y -= key_value
        if keys[constant.K_RIGHT]:
            buoys[self.selected].position.x += key_value
        if keys[constant.K_LEFT]:
            buoys[self.selected].position.x -= key_value

        if keys[constant.K_KP_5]:
            buoys[self.selected].position.y = 0

        if keys[constant.K_KP_6]:
            buoys[self.selected].width += key_value
        if keys[constant.K_KP_4]:
            buoys[self.selected].width -= key_value
            if buoys[self.selected].width < 1:
                buoys[self.selected].width = 1
        if keys[constant.K_KP_8]:
            buoys[self.selected].height += key_value
        if keys[constant.K_KP_2]:
            buoys[self.selected].height -= key_value
            if buoys[self.selected].height < 1:
                buoys[self.selected].height = 1

        if keys[constant.K_KP_9]:
            buoys[self.selected].angle -= key_value
        if keys[constant.K_KP_7]:
            buoys[self.selected].angle += key_value

        if keys[constant.K_KP_3]:
            buoys[self.selected].mass += key_value * 10000
        if keys[constant.K_KP_1]:
            buoys[self.selected].mass -= key_value * 10000

        # change center of mass
        if keys[constant.K_d]:
            buoys[self.selected].com.x += key_value
        if keys[constant.K_a]:
            buoys[self.selected].com.x -= key_value
        if keys[constant.K_x]:
            buoys[self.selected].com.y += key_value
        if keys[constant.K_w]:
            buoys[self.selected].com.y -= key_value
        if keys[constant.K_s]:  # reset center of mass to geometrical center
            buoys[self.selected].com = Vector2(buoys[self.selected].width / 2, buoys[self.selected].height / 2)

        for event in events:

            if event.type == constant.KEYDOWN:
                if event.key == constant.K_e:
                    engine.wind = not engine.wind
                if event.key == constant.K_t:
                    engine.translation = not engine.translation
                if event.key == constant.K_r:
                    engine.rotation = not engine.rotation

                if event.key == constant.K_SPACE:
                    if engine.timescale == 0:
                        engine.timescale = TIMESCALE
                    else:
                        engine.timescale = 0

                if event.key == constant.K_b:
                    engine.timescale += 1
                if event.key == constant.K_v:
                    engine.timescale -= 1

                if event.key == constant.K_PERIOD:
                    self.selected = self.selected + 1 if self.selected + 1 < len(buoys) else 0
                if event.key == constant.K_COMMA:
                    self.selected = self.selected - 1 if self.selected - 1 >= 0 else len(buoys) - 1

                if event.key == constant.K_ESCAPE:
                    sys.exit('Quitting')

            elif event.type == constant.QUIT:
                sys.exit('Quitting')
