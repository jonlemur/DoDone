import pygame

class DynamicLabel(pygame.sprite.Sprite):
    def __init__(self, text, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])

        self.rect = self.image.get_rect()

        self.text = text
        self.image.fill(color)

        font = pygame.font.SysFont('Verdana', 18)
        textColor = pygame.Color(200, 200, 200)
        self.txt_surface = font.render(self.text , 1, textColor)
        textW = self.txt_surface.get_width()
        textH = self.txt_surface.get_height()
        self.image.blit(self.txt_surface,[width/2-textW/2, height/2-textH/2])


if __name__ == "__main__":
    pass