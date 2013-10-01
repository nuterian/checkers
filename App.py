from Checkers import *
import pygame
import pygame.gfxdraw


pygame.init()
pygame.display.set_caption("Checkers")
screen = pygame.display.set_mode((800, 600))

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((240, 240, 240))


def drawCheckerBoard(screen, x, y, s):
    for a in xrange(8):
        for b in xrange(8):
            if (a+b)%2 == 0:
                pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(x+a*s, y+b*s, s, s))
            else:
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x+a*s, y+b*s, s, s))
                
                if b < 3:
                    #pygame.draw.circle(screen, (204, 0, 51), ((x+a*s)+s/2, (y+b*s)+s/2), s/2-10)
                    pygame.gfxdraw.aacircle(screen, (x+a*s)+s/2, (y+b*s)+s/2, s/2-10, (204, 0, 51))
                    pygame.gfxdraw.filled_circle(screen, (x+a*s)+s/2, (y+b*s)+s/2, s/2-10, (204, 0, 51))
                elif b > 4:
                    #pygame.draw.circle(screen, (0, 0, 0), ((x+a*s)+s/2, (y+b*s)+s/2), s/2-10)
                    pygame.gfxdraw.aacircle(screen, (x+a*s)+s/2, (y+b*s)+s/2, s/2-10, (30, 30, 30))
                    pygame.gfxdraw.filled_circle(screen, (x+a*s)+s/2, (y+b*s)+s/2, s/2-10, (30, 30, 30))                    
                    

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
            pygame.quit()
            

    #pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(30, 30, 60, 60))
    drawCheckerBoard(background, 50, 50, 60)
    
    screen.blit(background, (0, 0))
    pygame.display.flip()

