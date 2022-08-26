import pygame.surface


# still only works for rectangles
class MyRect(pygame.Surface):
    def __init__(self, parent, position, width, height, color, angle, cob):
        super(MyRect, self).__init__((width, height))
        self.position = position
        self.color = color
        self.angle = angle
        self.cob = cob

        self.parent = parent  # try to remove this

        self.surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.surface.convert_alpha()
        self.surface.fill(self.color)
        self.big_surface = pygame.Surface((width * 2, height * 2), pygame.SRCALPHA, 32)
        self.big_surface.convert_alpha()
        self.rect = self.surface.get_rect(center=(position.x + width // 2, position.y + height // 2))

        self.update()

    def update(self):
        center = self.rect.center
        image = pygame.transform.rotate(self.surface, self.angle)
        self.rect = image.get_rect()
        self.rect.center = center
        self.parent.blit(image, self.rect)


