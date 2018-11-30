import pygame


class Task(pygame.sprite.Sprite):
    def __init__(self,text, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.w = width
        self.h = height
        self.c = color
        self.active = False

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

        cW = self.image.get_width()
        cH = self.image.get_height()

        font = pygame.font.SysFont('Verdana', 12)
        textColor = pygame.Color(200, 200, 200)
        self.text = text
        self.txt_surface = font.render(text, 1, textColor)
        textW = self.txt_surface.get_width()
        textH = self.txt_surface.get_height()
        self.image.blit(self.txt_surface,[width/2-textW/2, height/2-textH/2])


    def resize(self, w, h):
        self.w = w
        self.h = h
        self.image = pygame.Surface([w, h])
        self.image.fill(self.c)
        self.rect = self.image.get_rect()
        textW = self.txt_surface.get_width()
        textH = self.txt_surface.get_height()
        self.image.blit(self.txt_surface, [self.w/2-textW/2, self.h/2-textH/2])

    def update(self):
        pass

    def setEvent(self, event, dClick=False):
        if self.rect.collidepoint(event.pos) and event.type == pygame.MOUSEBUTTONDOWN:
            self.active = True
            if dClick == True:
                self.kill()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.active = False

        if event.type == pygame.MOUSEMOTION and self.active == True:
            self.rect.center = event.pos


    def reposition(self, x, y):
        self.rect.center = (x,y)

    def setColor(self,done):
        if done == True:
            self.cD = pygame.Color(50, 50, 50, 0)
            self.image.fill(self.cD)
        else:
            self.image.fill(self.c)
            #self.c = pygame.Color(60, 60, 60, 0)

        #self.image.fill(self.c)
        textW = self.txt_surface.get_width()
        textH = self.txt_surface.get_height()
        self.image.blit(self.txt_surface, [self.w / 2 - textW / 2, self.h / 2 - textH / 2])



if __name__ == "__main__":
    pass
