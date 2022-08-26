from random import randint

from util.vectors import Vector2


class Sky:
    def __init__(self, number_of_stars: int, screen_width: int, water_start: int):
        self.positions = []
        self.radii = []
        for i in range(number_of_stars):
            x = randint(0, screen_width)
            y = randint(0, water_start)
            self.positions.append(Vector2((x, y)))
            r = randint(1, 3)
            self.radii.append(r)
        self.wind_direction = 0
        self.wind_base_strength = 100.0  # N / m²
