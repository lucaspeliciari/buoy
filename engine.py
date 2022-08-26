from random import triangular

import pygame.display
import pygame.draw
import pygame.font
import pygame.image

from constants import *
from util.functions import rotate_around
from util.rect import MyRect


class Engine:
    def __init__(self, screen_size, timescale):
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode((screen_size.x, screen_size.y))
        self.clock = pygame.time.Clock()
        self.timer = 0
        self.font = pygame.font.SysFont("monospace", 15)
        self.timescale = timescale

        self.translation = True
        self.rotation = True
        self.wind = False

    def tick(self, framerate):
        self.clock.tick(framerate)
        self.timer += self.clock.get_time() / 1000  # in seconds
        self.screen.fill(BLACK)

        # warning if framerate drops to below 50 fps
        if self.clock.get_fps() < 50 and self.timer > 0.5:
            text = f'LOW FRAMERATE! {self.clock.get_fps()} fps'
            print(text)
            self.screen.blit(self.font.render(text, True, RED), (100, 80))

    def physics(self, water, sky, buoys):
        time_delta = self.clock.get_time() / 1000

        for physics_frame in range(self.timescale):
            self.wind_physics(sky)
            self.buoy_physics(time_delta, water, sky, buoys)

    def wind_physics(self, sky):
        sky.wind_direction += triangular(-1, 1, 0)

    def buoy_physics(self, time_delta, water, sky, buoys):
        for i, buoy in enumerate(buoys):
            water_level = self.screen_size.y - water.height
            buoy.get_submerged_vertices(water_level)
            wind_strength = sky.wind_direction * sky.wind_base_strength if self.wind else 0

            if self.translation:
                buoy.translation(water, wind_strength, time_delta)
            if self.rotation:
                buoy.rotation(water, time_delta)

    def render_water(self, water):  # very realistic graphics
        pygame.draw.rect(self.screen, BLUE,
                         (0, self.screen_size.y - water.height, self.screen_size.x, self.screen_size.y))

    # this draws stars in background
    def render_sky(self, sky):
        text = f'Wind strength: {(sky.wind_direction * sky.wind_base_strength):.2f}'
        self.screen.blit(self.font.render(text, True, WHITE), (self.screen_size.x - self.font.size(text)[0], 0))
        for position, radius in zip(sky.positions, sky.radii):
            pygame.draw.circle(self.screen, WHITE, (position.x, position.y), radius)

    def render_buoys(self, buoys):

        for i, buoy in enumerate(buoys):
            # draw buoy
            MyRect(self.screen, buoy.position, buoy.width, buoy.height, buoy.color, buoy.angle, buoy.cob)

            # draw info about buoy
            if False:  # change to true to draw this info
                text_vertical_offset = 70
                self.screen.blit(self.font.render(f'ID: {buoy.id}  Mass: {buoy.mass:.0f}  position: {buoy.position}', True, WHITE), (10, 140 + i * text_vertical_offset))
                self.screen.blit(
                    self.font.render(f'Speed: {buoy.speed}  accel: {buoy.accel}  angular speed: {buoy.ang_speed:.2f}  angular accel: {buoy.ang_accel:.2f}', True, WHITE),
                    (10, 155 + i * text_vertical_offset))
                self.screen.blit(self.font.render(f'CoM: {buoy.com}  CoB: {buoy.cob}  angle: {buoy.angle}°', True, WHITE), (10, 170 + i * text_vertical_offset))
                if buoy.submerged_area > 0:
                    submerged_percent = 100 * buoy.submerged_area / (buoy.width * buoy.height)  # seems to work perfectly
                    text = f'Submerged area: {buoy.submerged_area:.0f}m²  {submerged_percent:.2f}% submerged'
                    self.screen.blit(self.font.render(text, True, WHITE), (10, 185 + i * text_vertical_offset))

            # draw buoy's vertices and their indices, this is mostly for debug
            for j, vertex in enumerate(buoy.vertices):
                pygame.draw.circle(self.screen, RED, vertex.coord.components(), 5)
                self.screen.blit(pygame.font.SysFont("monospace", 20, bold=True).render(str(j), True, WHITE), (vertex.coord.x - 5, vertex.coord.y - 23))

            if buoy.submerged_area > 0:
                # draw polygon that represents submerged area
                pygame.draw.polygon(self.screen, GREEN, buoy.vertices_in_order)

                # draw points of intersection with water surface
                pygame.draw.circle(self.screen, RED, buoy.vertices_in_order[0], 3)
                pygame.draw.circle(self.screen, RED, buoy.vertices_in_order[-1], 3)

                # draw cob
                cob = buoy.cob + buoy.position
                pygame.draw.circle(self.screen, WHITE, cob.components(), 5)

            # draw com, bugged
            com = rotate_around(buoy.get_centroid() + buoy.position, buoy.com + buoy.position, -buoy.angle)
            pygame.draw.circle(self.screen, YELLOW, com, 3)

    # draw info about simulation
    def render_ui(self, mouse_position):
        texts = [
                    f'Timer: {self.timer:.3f}',
                    f'{self.clock.get_fps():.0f} fps',
                    f'Timescale: {self.timescale}x',
                    f'Mouse position: {mouse_position}',
                    '',
                    f'Translation: {self.translation}',
                    f'Rotation: {self.rotation}',
                    f'Wind: {self.wind}'
                ]

        for i, text in enumerate(texts):
            self.screen.blit(self.font.render(text, True, WHITE), (0, i * 15))


