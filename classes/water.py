class Water:
    def __init__(self,
                 height: int,
                 density: float
                 ):
        self.height = height
        self.density = density
        self.color = (0, 0, 255)

    def __str__(self):
        return f'h{self.height}'


