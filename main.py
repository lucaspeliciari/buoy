# started 30/07/2022



import pygame

from classes.buoy import Buoy
from classes.sky import Sky
from classes.water import Water
from constants import TIMESCALE
from engine import Engine
from event_handler import Handler
from util.vectors import Vector2  # turns out pygame has its own vectors

def main():
    pygame.init()
    engine = Engine(Vector2((800, 600)), TIMESCALE)
    event_handler = Handler()
    water = Water(200, 1000)
    sky = Sky(50, engine.screen_size.x, engine.screen_size.y - water.height)
    buoy1 = Buoy(350, 300, 75, 250, 0.3 * 10 ** 9)
    buoy2 = Buoy(50, 0, 200, 100, 0.5 * 10 ** 9)
    buoy3 = Buoy(600, 150, 100, 250, 0.99 * 10 ** 9)
    buoys = [
                buoy1,
                buoy2,
                buoy3
            ]

    while True:
        engine.tick(60)
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        mouse_position = pygame.mouse.get_pos()
        event_handler.handle(engine, events, keys, buoys)

        engine.render_sky(sky)
        engine.render_water(water)
        engine.physics(water, sky, buoys)
        engine.render_buoys(buoys)
        engine.render_ui(mouse_position)

        pygame.display.update()


if __name__ == '__main__':
    main()
