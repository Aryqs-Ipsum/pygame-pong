import pygame
import time
from pygame.locals import*
from random import*
from settings import*

### DEF ###
pygame.init()
fenetre=pygame.display.set_mode(size)
clock=pygame.time.Clock()

#chargement des images
ball=pygame.image.load("ressources/ballon.gif").convert_alpha()
fond=pygame.image.load("ressources/terrain.png").convert_alpha()
pers1=pygame.image.load("ressources/Pers1.png").convert_alpha()
pers2=pygame.image.load("ressources/Pers2.png").convert_alpha()
obstacle=pygame.image.load("ressources/obstacle.png").convert_alpha()

#redimensionnement
bigpers1=pygame.transform.scale(pers1,(scalepers))
bigpers2=pygame.transform.scale(pers2,(scalepers))
bigobstacle=pygame.transform.scale(obstacle,(50,50))
ball2=pygame.transform.scale(ball,(scaleball))

#creation rectangle
joueur1rect=bigpers1.get_rect()
joueur2rect=bigpers2.get_rect()
ballrect1=ball2.get_rect()
cage1=pygame.Rect(0,0,5,height)
cage2=pygame.Rect(width-30,0,5,height)
obsrect=bigobstacle.get_rect()

#placement des elements
joueur1rect.centerx=width/15
joueur1rect.centery=height/2
joueur2rect.centerx=width-width/15
joueur2rect.centery=height/2
ballrect1.centerx=width/2
ballrect1.centery=height/2
obsrect.centerx=randint(0,width)
obsrect.centery=randint(0,height)

#fond du jeu
fond2=pygame.transform.scale(fond,(width,height))

#nom de la fenetre
pygame.display.set_caption('Pong')

### UNE FONCTION ###
def affichertexte(txt,couleur,time,txtcolor):
    background=pygame.Surface(fenetre.get_size())
    background=background.convert()
    background.fill(couleur)

    font=pygame.font.Font('ressources\kongtext.ttf',50)
    text=font.render(txt,1,(txtcolor))
    textpos=text.get_rect()
    textpos.centerx=width/2
    textpos.centery=height/2
    background.blit(text,textpos)
    fenetre.blit(text,textpos)

    fenetre.blit(background,(0,0))
    pygame.display.flip()
    pygame.time.wait(time)

### LANCEMENT ###
def lancement():
    affichertexte("3",NOIR,500,BLANC)
    affichertexte("2",NOIR,500,BLANC)
    affichertexte("1",NOIR,500,BLANC)
    affichertexte("START",NOIR,1000,BLANC)
    ballrect1.centerx=width/2
    ballrect1.centery=height/2
    obsrect.centerx=randint(0,width)
    obsrect.centery=randint(0,height)

def quitgame():
    pygame.quit()
    quit()

### MENU ###
def text_objects(text, font):
    textSurface = font.render(text, True, BLANC)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None): #definition d'un bouton
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:#detection avec la souris
        pygame.draw.rect(fenetre, ac,(x,y,w,h))

        if click[0] == 1 and action != None:#detection du clic
            action()
    else:
        pygame.draw.rect(fenetre, ic,(x,y,w,h))

    smallText = pygame.font.Font("ressources\kongtext.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    fenetre.blit(textSurf, textRect)

def game_intro(): #creation menu de selection

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        fenetre.fill(NOIR)
        largeText = pygame.font.Font('ressources\kongtext.ttf',50)
        TextSurf, TextRect = text_objects("Choose number of players", largeText)
        TextRect.center = ((width/2),(height/2))
        fenetre.blit(TextSurf, TextRect)

        button('1',150,350,100,50,blue,bright_blue,game_loop1p)#creation de boutons
        button('2',550,350,100,50,blue,bright_blue,game_loop2p)
        button('Quit',950,350,100,50,ROUGE,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)

### LE PROGRAMME ###
def game_loop1p(): #jeu pour 1 joueur

    #debut boucle
    continuer=True
    debut,actu=time.time(),time.time()

    #scores
    score1=0
    score2=0

    #compte a rebours
    lancement()

    while continuer :

        #mouvement du ballon
        ballrect1.move_ip(speed)

        #collisions du ballon avec la fenetre
        if ballrect1.left<0 or ballrect1.right>width:
            speed[0]=-speed[0]
        if ballrect1.top<0 or ballrect1.bottom>height:
            speed[1]=-speed[1]

        #collisions du ballon avec les joueurs
        if joueur1rect.colliderect(ballrect1) or joueur2rect.colliderect(ballrect1):
            speed[0]=-speed[0]

        #collision avec l'obstacle
        if obsrect.colliderect(ballrect1):
            speed[0]=-speed[0]
            obsrect.centerx=randint(0,width)
            obsrect.centery=randint(0,height)

        #but
        if ballrect1.colliderect(cage1):
            score2=score2+1
            if score2<3:
                lancement()
        elif ballrect1.colliderect(cage2):
            score1=score1+1
            if score1<3:
                lancement()

        fenetre.blit(fond2,(0,0))
        fenetre.blit(ball2,ballrect1)
        fenetre.blit(bigpers1,joueur1rect)
        fenetre.blit(bigpers2,joueur2rect)
        fenetre.blit(bigobstacle,obsrect)

        #gestion du framerate
        clock.tick(FPS)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                continuer=False

        #gestion des evenements du clavier
        tkey=pygame.key.get_pressed()

        #AI, player 2
        if ballrect1.top > joueur2rect.top :
            joueur2rect.move_ip(0,persspeed)
        elif ballrect1.top < joueur2rect.top :
            joueur2rect.move_ip(0,-persspeed)

        #player 1
        if tkey[K_s]:
            joueur1rect.move_ip(0,-persspeed)
        elif tkey[K_x]:
            joueur1rect.move_ip(0,persspeed)
        elif tkey[K_ESCAPE]:
            continuer=False

        #fin jeu
        if score1>=3 or score2>=3 :
            continuer=False

        #affichage des scores
        if score1>=3 :
            affichertexte('END, player 1 win : '+str(score1)+str('-')+str(score2),BLEU,3000,BLANC)
        elif score2>=3 :
            affichertexte('END, player 2 win : '+str(score2)+str('-')+str(score1),ROUGE,3000,BLANC)

def game_loop2p(): #jeu pour 2 joueurs

    #debut boucle
    continuer=True
    debut,actu=time.time(),time.time()

    #scores
    score1=0
    score2=0

    #compte a rebours
    lancement()

    while continuer :

        #mouvement du ballon
        ballrect1.move_ip(speed)

        #collisions du ballon avec la fenetre
        if ballrect1.left<0 or ballrect1.right>width:
            speed[0]=-speed[0]
        if ballrect1.top<0 or ballrect1.bottom>height:
            speed[1]=-speed[1]

        #collisions du ballon avec les joueurs
        if joueur1rect.colliderect(ballrect1) or joueur2rect.colliderect(ballrect1):
            speed[0]=-speed[0]

        #collision avec l'obstacle
        if obsrect.colliderect(ballrect1):
            speed[0]=-speed[0]
            obsrect.centerx=randint(0,width)
            obsrect.centery=randint(0,height)

        #but
        if ballrect1.colliderect(cage1):
            score2=score2+1
            if score2<3:
                lancement()
        elif ballrect1.colliderect(cage2):
            score1=score1+1
            if score1<3:
                lancement()

        fenetre.blit(fond2,(0,0))
        fenetre.blit(ball2,ballrect1)
        fenetre.blit(bigpers1,joueur1rect)
        fenetre.blit(bigpers2,joueur2rect)
        fenetre.blit(bigobstacle,obsrect)

        #gestion du framerate
        clock.tick(FPS)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                continuer=False

        #gestion des evenements du clavier
        tkey=pygame.key.get_pressed()

        #AI, player 2
        if tkey[K_UP]:
            joueur2rect.move_ip(0,-persspeed)
        elif tkey[K_DOWN]:
            joueur2rect.move_ip(0,persspeed)

        #player 1
        if tkey[K_s]:
            joueur1rect.move_ip(0,-persspeed)
        elif tkey[K_x]:
            joueur1rect.move_ip(0,persspeed)
        elif tkey[K_ESCAPE]:
            continuer=False

        #fin jeu
        if score1>=3 or score2>=3 :
            continuer=False

        #affichage des scores
        if score1>=3 :
            affichertexte('END, player 1 win : '+str(score1)+str('-')+str(score2),BLEU,3000,BLANC)
        elif score2>=3 :
            affichertexte('END, player 2 win : '+str(score2)+str('-')+str(score1),ROUGE,3000,BLANC)

game_intro() #menu
pygame.quit() #quitter la fenetre
quit()
