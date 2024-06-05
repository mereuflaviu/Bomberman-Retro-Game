from itertools import count
import pygame
import random
import math
import sys
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800,600))

#Title and Icon
pygame.display.set_caption("Bomberman")
icon = pygame.image.load('bomberman.png')

pygame.display.set_icon(icon)

#Music
mixer.music.load('backgroundmusic.mp3')
pygame.mixer.music.set_volume(0.2)
mixer.music.play(-1)


#Meniu selector
meniu_background = pygame.image.load('backInitial.png')
mod_de_joc=0
running_meniu = True
screen.blit(meniu_background, (0,0))
primulbuton = pygame.image.load('primulbuton.png')
screen.blit(primulbuton, (260, 250))
doileabuton = pygame.image.load('doileabuton.png')
screen.blit(doileabuton, (360, 250))
exitbuton = pygame.image.load('exit.png')
screen.blit(exitbuton, (310, 330))
pygame.display.update()

while running_meniu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Set the x, y postions of the mouse click
            pos = pygame.mouse.get_pos()
            if pos[0]>260 and pos[0]<320 and pos[1]>250 and pos[1]<330:
                running_meniu=False
                mod_de_joc=1
            if pos[0]>360 and pos[0]<420 and pos[1]>250 and pos[1]<330:
                running_meniu=False
                mod_de_joc=2
            if pos[0]>310 and pos[0]<370 and pos[1]>330 and pos[1]<410:
                sys.exit()
             

#Sounds

powerup_sound = pygame.mixer.Sound('powerup.wav')
explosion_sound = pygame.mixer.Sound('explozie.wav')
bomb_sound = pygame.mixer.Sound('bombalert.wav')
gameover_sound = pygame.mixer.Sound('gameover.wav')
one_explosion=[0,0]
#Background
background = pygame.image.load('fundal.png')

#blocks
barrel = pygame.image.load('barrel.png')
barrel = pygame.transform.scale(barrel, (50,50))
stone = pygame.image.load('fence.png')
stone = pygame.transform.scale(stone , (45,45))

#Back matrix
matrix = [[2, 2, 2, 2, 2, 2, 2 ,2 , 2, 2, 2, 2, 2],
        [2, 0, 0, 0, 0, 0, 0 ,0 , 0 ,0, 0, 0, 2],
        [2, 0, 2, 0, 2, 0, 2 ,0 , 2, 0, 2, 0, 2],
        [2, 0, 0, 0, 0, 0, 0 ,0 , 0, 0, 0, 0, 2],
        [2, 0, 2, 0, 2, 0, 2 ,0 , 2, 0, 2, 0, 2],
        [2, 0, 0, 0, 0, 0, 0 ,0 , 0, 0, 0, 0, 2],
        [2, 0, 2, 0, 2, 0, 2 ,0 , 2, 0, 2, 0, 2],
        [2, 0, 0, 0, 0, 0, 0 ,0 , 0, 0, 0, 0, 2],
        [2, 0, 2, 0, 2, 0, 2 ,0 , 2, 0, 2, 0, 2],
        [2, 0, 0, 0, 0, 0, 0 ,0 , 0, 0, 0, 0, 2],
        [2, 0, 2, 0, 2, 0, 2 ,0 , 2, 0, 2, 0, 2],
        [2, 0, 0, 0, 0, 0, 0 ,0 , 0, 0, 0, 0, 2],
        [2, 2, 2, 2, 2, 2, 2 ,2 , 2, 2, 2, 2, 2]]

#Players
number_of_players=2
Players = [pygame.image.load('white.png'), pygame.image.load('black.png')]
SpecialPlayers = [pygame.image.load('special1.png'), pygame.image.load('special2.png')]
for i in range(2):
    Players[i]=pygame.transform.scale(Players[i], (40,40))
    SpecialPlayers[i]=pygame.transform.scale(SpecialPlayers[i], (40,40))

line_players=[0,0]
collumn_players=[0,0]
playerX_change=[0,0]
playerY_change=[0,0]
playersHealth=[2,2]
healthChange=[0,0]

#Putting players
counter=number_of_players
while counter > 0:
    line=random.randint(1,12)
    collumn=random.randint(1,12)
    if matrix[line][collumn]!=2 and matrix[line][collumn]<2:
        matrix[line][collumn]=counter-1+3
        line_players[counter-1]=line
        collumn_players[counter-1]=collumn
        counter-=1


def verify_barrel(x,y):
    if matrix[x][y]==2 or matrix[x][y]==1 or matrix[x][y]>2:
        return False
    if matrix[x+1][y]>2 or matrix[x][y+1]>2 or matrix[x-1][y]>21 or matrix[x][y-1]>2:
        return False
    return True
# TREBUIE VERIFICAT SA NU FIE IN JURUL FIX AL JUCATORULUI!!
random_barrels=40
while random_barrels > 0:
    line=random.randint(1,12)
    collumn=random.randint(1,12)
    if verify_barrel(line, collumn) == True:
        matrix[line][collumn]=1
        random_barrels=random_barrels-1

#Explosion

def explode(x,y, parametru):
    ExplosionImg = pygame.image.load(parametru)
    ExplosionImg = pygame.transform.scale(ExplosionImg, (40,40))
    screen.blit(ExplosionImg, (x*40, y*40+80))

#Bomb 1 
BombImg = pygame.image.load('bomb1.png')
BombImg = pygame.transform.scale(BombImg, (40,40))
bombLine=0
bombCollum=0


#Bomb 2 
BombImg2 = pygame.image.load('bomb2.png')
BombImg2 = pygame.transform.scale(BombImg2, (40,40))
bombLine2=0
bombCollum2=0

#area
bombArea=[1,1]

#Bonusuri
Viata = pygame.image.load('heart.png')
Viata = pygame.transform.scale(Viata, (40,40))
Arie = pygame.image.load('Fire.png')
Arie = pygame.transform.scale(Arie, (40,40))
Vest = pygame.image.load('vest.png')
Vest = pygame.transform.scale(Vest, (40,40))
bonusSpecial=[0,0]
bonusSpecialTime=[0,0]

#After Explosion
def dexplosion(r,c,nr):
        for i in range(bombArea[nr]):
            if r+i+1<13:
                if matrix[r+i+1][c]==-1:
                    matrix[r+i+1][c]=0
            if r-1-i>0:
                if matrix[r-i-1][c]==-1 :
                    matrix[r-i-1][c]=0
            if c+i+1<13:
                if matrix[r][c+i+1]==-1:
                    matrix[r][c+i+1]=0
            if c-i-1>0:
                if matrix[r][c-i-1]==-1:
                    matrix[r][c-i-1]=0

#Explosion
def explosion(r, c, nr):
    global playersHealth
    global healthChange
    global parametru
    global matrix
    if one_explosion[nr]==1:
        explosion_sound.play()
        one_explosion[nr]=0
    #BONUSURI VIATA -3, ARIE -4, SPECIAL -5
    chance=0
    if nr == 0:
        parametru = 'explode1.png'
    else:
        parametru = 'explode2.png'
    explode(r,c, parametru)
    if matrix[r][c]>2 and bonusSpecial[matrix[r][c]-3]!=2:
        playersHealth[matrix[r][c]-3]+=-1+healthChange[matrix[r][c]-3]
        healthChange[matrix[r][c]-3]=1
    for i in range(bombArea[nr]):
        if matrix[r+1][c]!=2 and r+i+1<13:
            explode(r+i+1,c, parametru)
            if matrix[r+i+1][c]>2 and bonusSpecial[matrix[r+i+1][c]-3]!=2:
                playersHealth[matrix[r+i+1][c]-3]=playersHealth[matrix[r+i+1][c]-3]-1+healthChange[matrix[r+i+1][c]-3]
                healthChange[matrix[r+i+1][c]-3]=1
            if matrix[r+i+1][c]==1:
                score_value[nr]+=2
                chance=random.randint(0,24)
                if chance>10:
                    if chance<16:
                        matrix[r+i+1][c]=-3
                    elif chance<21:
                        matrix[r+i+1][c]=-4
                    elif chance<24:
                        matrix[r+i+1][c]=-5
                else:
                    matrix[r+i+1][c]=-1
        if matrix[r-1][c]!=2 and r-i-1>0:
            explode(r-i-1,c, parametru)
            if matrix[r-i-1][c]>2 and bonusSpecial[matrix[r-i-1][c]-3]!=2:
                playersHealth[matrix[r-i-1][c]-3]=playersHealth[matrix[r-i-1][c]-3]-1+healthChange[matrix[r-i-1][c]-3]
                healthChange[matrix[r-i-1][c]-3]=1
            if matrix[r-i-1][c]==1:
                score_value[nr]+=2
                chance=random.randint(0,24)
                if chance>10:
                    if chance<16:
                        matrix[r-i-1][c]=-3
                    elif chance<21:
                        matrix[r-i-1][c]=-4
                    elif chance<24:
                        matrix[r-i-1][c]=-5
                else:
                    matrix[r-i-1][c]=-1
        if matrix[r][c+1]!=2 and c+i+1<13:
            explode(r,c+i+1, parametru)
            if matrix[r][c+i+1]>2 and bonusSpecial[matrix[r][c+i+1]-3]!=2:
                playersHealth[matrix[r][c+1+i]-3]=playersHealth[matrix[r][c+1+i]-3]-1+healthChange[matrix[r][c+1+i]-3]
                healthChange[matrix[r][c+1+i]-3]=1
            if matrix[r][c+i+1]==1:
                score_value[nr]+=2
                chance=random.randint(0,24)
                if chance>10:
                    if chance<16:
                        matrix[r][c+i+1]=-3
                    elif chance<21:
                        matrix[r][c+i+1]=-4
                    elif chance<24:
                        matrix[r][c+i+1]=-5
                else:
                    matrix[r][c+i+1]=-1
        if matrix[r][c-1]!=2 and c-i-1>0:
            explode(r,c-i-1, parametru)
            if matrix[r][c-1-i]>2 and bonusSpecial[matrix[r][c-1-i]-3]!=2:
                playersHealth[matrix[r][c-i-1]-3]=playersHealth[matrix[r][c-i-1]-3]-1+healthChange[matrix[r][c-i-1]-3]
                healthChange[matrix[r][c-i-1]-3]=1
            if matrix[r][c-i-1]==1:
                score_value[nr]+=2
                chance=random.randint(0,24)
                if chance>10:
                    if chance<16:
                        matrix[r][c-i-1]=-3
                    elif chance<21:
                        matrix[r][c-i-1]=-4
                    elif chance<24:
                        matrix[r][c-i-1]=-5
                else:
                    matrix[r][c-i-1]=-1


# pause Se apasa p pentru pauza
game_status=1
textPauzaX=330
textPauzaY=245
def pauza():
    timeout=font.render("P a u z a", True, 	(255,0,0))
    screen.blit(timeout, (textPauzaX, textPauzaY))

#Score
score_value=[0,0]
font = pygame.font.Font('dogica.ttf',15)
textX=15
textY=20

#ShowScore
def showScore(x,y):
    score1=font.render("Score Player1: %2d" % score_value[0] + "   Health: " + str(playersHealth[0]),True, (255, 255, 255) )
    score2=font.render("Score Player2: %2d" % score_value[1] + "   Health: " + str(playersHealth[1]),True, (255, 255, 255) )
    screen.blit(score1, (textX, textY))
    screen.blit(score2, (textX, textY+20))


#Nu se poate trece de bomba
def passBomb(x,y):
    if x==bombLine and y==bombCollum:
        return False
    if x==bombLine2 and y==bombCollum2:
        return False
    return True

pygame.display.update()
running = True


#Conditii
start_bomb=0
start_bomb2=0
startGame=0
circular=0
clock = pygame.time.Clock()
iteratii=0
coltMic=1
coltMare=11
completat=0
linie_de_completat=11
coloana_de_completat=1


render =pygame.image.load('render.png')
render=pygame.transform.scale(render, (420,420))
speech =pygame.image.load('speech.png')
speech = pygame.transform.scale(speech, (280,300))
if mod_de_joc==1:
    while running:
        
        if game_status>0:
            iteratii+=1
        
        screen.fill((128,128,0))
        screen.blit(render,(450, 189) )
        screen.blit(speech, (520, 10))
        while game_status<0:
            pauza()
            pygame.display.update()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game_status = game_status*(-1)
                        continue

        if playersHealth[0]==0:
            gameover_sound.play()
            print('Player2 a castigat')
            running = False
            continue
        if playersHealth[1]==0:
            gameover_sound.play()
            running = False
            print('Player1 a castigat')
            continue

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_status = game_status*(-1)
                    if game_status < 0:
                        print('Pauza')
                        continue
                if event.key == pygame.K_a:
                    if  matrix[line_players[0]-1][collumn_players[0]]==0 and passBomb(line_players[0]-1, collumn_players[0])==True:
                        matrix[line_players[0]][collumn_players[0]]=0
                        line_players[0]+=-1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]-1][collumn_players[0]]==-4:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        line_players[0]+=-1
                        bombArea[0]+=1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]-1][collumn_players[0]]==-3:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        line_players[0]+=-1
                        playersHealth[0]+=1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif matrix[line_players[0]-1][collumn_players[0]]==-5:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        line_players[0]+=-1
                        bonusSpecial[0]=1
                        matrix[line_players[0]][collumn_players[0]]=3
                if event.key == pygame.K_d:
                    if  matrix[line_players[0]+1][collumn_players[0]]==0 and passBomb(line_players[0]+1,collumn_players[0])==True:
                        matrix[line_players[0]][collumn_players[0]]=0
                        line_players[0]+=1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]+1][collumn_players[0]]==-4:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        line_players[0]+=1
                        bombArea[0]+=1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]+1][collumn_players[0]]==-3:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        line_players[0]+=1
                        playersHealth[0]+=1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]+1][collumn_players[0]]==-5:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        line_players[0]+=1
                        bonusSpecial[0]=1
                        matrix[line_players[0]][collumn_players[0]]=3
                if event.key == pygame.K_w:
                    if  matrix[line_players[0]][collumn_players[0]-1]==0 and passBomb(line_players[0],collumn_players[0]-1)==True:
                        matrix[line_players[0]][collumn_players[0]]=0
                        collumn_players[0]+=-1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]][collumn_players[0]-1]==-4:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        collumn_players[0]+=-1
                        bombArea[0]+=1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]][collumn_players[0]-1]==-3:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        collumn_players[0]+=-1
                        playersHealth[0]+=1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]][collumn_players[0]-1]==-5:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        collumn_players[0]+=-1
                        bonusSpecial[0]=1
                        matrix[line_players[0]][collumn_players[0]]=3
                if event.key == pygame.K_s:
                    if  matrix[line_players[0]][collumn_players[0]+1]==0 and passBomb(line_players[0],collumn_players[0]+1)==True:
                        matrix[line_players[0]][collumn_players[0]]=0
                        collumn_players[0]+=1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]][collumn_players[0]+1]==-4:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        collumn_players[0]+=1
                        bombArea[0]+=1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]][collumn_players[0]+1]==-3:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        collumn_players[0]+=1
                        playersHealth[0]+=1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]][collumn_players[0]+1]==-5:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        collumn_players[0]+=1
                        bonusSpecial[0]=1
                        matrix[line_players[0]][collumn_players[0]]=3
                if event.key == pygame.K_LEFT:
                    if  matrix[line_players[1]-1][collumn_players[1]]==0 and passBomb(line_players[1]-1,collumn_players[1])==True:
                        matrix[line_players[1]][collumn_players[1]]=0
                        line_players[1]+=-1
                        matrix[line_players[1]][collumn_players[1]]=4
                    elif  matrix[line_players[1]-1][collumn_players[1]]==-4:
                        powerup_sound.play()
                        matrix[line_players[1]][collumn_players[1]]=0
                        line_players[1]+=-1
                        playersHealth[1]+=1
                        matrix[line_players[1]][collumn_players[1]]=4
                    elif  matrix[line_players[1]-1][collumn_players[1]]==-3:
                        powerup_sound.play()
                        matrix[line_players[1]][collumn_players[1]]=0
                        line_players[1]+=-1
                        playersHealth[1]+=1
                        matrix[line_players[1]][collumn_players[1]]=4
                    elif  matrix[line_players[1]-1][collumn_players[1]]==-5:
                        powerup_sound.play()
                        matrix[line_players[1]][collumn_players[1]]=0
                        line_players[1]+=-1
                        bonusSpecial[1]=1
                        matrix[line_players[1]][collumn_players[1]]=4
                if event.key == pygame.K_RIGHT:
                    if  matrix[line_players[1]+1][collumn_players[1]]==0 and passBomb(line_players[1]+1,collumn_players[1])==True:
                        matrix[line_players[1]][collumn_players[1]]=0
                        line_players[1]+=1
                        matrix[line_players[1]][collumn_players[1]]=4
                    elif  matrix[line_players[1]+1][collumn_players[1]]==-3:
                        powerup_sound.play()
                        matrix[line_players[1]][collumn_players[1]]=0
                        line_players[1]+=1
                        playersHealth[1]+=1
                        matrix[line_players[1]][collumn_players[1]]=4
                    elif  matrix[line_players[1]+1][collumn_players[1]]==-4:
                        powerup_sound.play()
                        matrix[line_players[1]][collumn_players[1]]=0
                        line_players[1]+=1
                        bombArea[1]+=1
                        matrix[line_players[1]][collumn_players[1]]=4
                    elif  matrix[line_players[1]+1][collumn_players[1]]==-5:
                        powerup_sound.play()
                        matrix[line_players[1]][collumn_players[1]]=0
                        line_players[1]+=1
                        bonusSpecial[1]=1
                        matrix[line_players[1]][collumn_players[1]]=4
                if event.key == pygame.K_UP:
                    if  matrix[line_players[1]][collumn_players[1]-1]==0 and passBomb(line_players[1],collumn_players[1]-1)==True:
                        matrix[line_players[1]][collumn_players[1]]=0
                        collumn_players[1]+=-1
                        matrix[line_players[1]][collumn_players[1]]=4
                    elif  matrix[line_players[1]][collumn_players[1]-1]==-4:
                        powerup_sound.play()
                        matrix[line_players[1]][collumn_players[1]]=0
                        collumn_players[1]+=-1
                        bombArea[1]+=1
                        matrix[line_players[1]][collumn_players[1]]=4
                    elif  matrix[line_players[1]][collumn_players[1]-1]==-3:
                        powerup_sound.play()
                        matrix[line_players[1]][collumn_players[1]]=0
                        collumn_players[1]+=-1
                        playersHealth[1]+=1
                        matrix[line_players[1]][collumn_players[1]]=4
                    elif  matrix[line_players[1]][collumn_players[1]-1]==-5:
                        powerup_sound.play()
                        matrix[line_players[1]][collumn_players[1]]=0
                        collumn_players[1]+=-1
                        bonusSpecial[1]=1
                        matrix[line_players[1]][collumn_players[1]]=4
                if event.key == pygame.K_DOWN:
                    if  matrix[line_players[1]][collumn_players[1]+1]==0 and passBomb(line_players[1],collumn_players[1]+1)==True:
                        matrix[line_players[1]][collumn_players[1]]=0
                        collumn_players[1]+=1
                        matrix[line_players[1]][collumn_players[1]]=4
                    elif  matrix[line_players[1]][collumn_players[1]+1]==-4:
                        powerup_sound.play()
                        matrix[line_players[1]][collumn_players[1]]=0
                        collumn_players[1]+=1
                        bombArea[1]+=1
                        matrix[line_players[1]][collumn_players[1]]=4
                    elif  matrix[line_players[1]][collumn_players[1]+1]==-3:
                        powerup_sound.play()
                        matrix[line_players[1]][collumn_players[1]]=0
                        collumn_players[1]+=1
                        playersHealth[1]+=1
                        matrix[line_players[1]][collumn_players[1]]=4
                    elif  matrix[line_players[1]][collumn_players[1]+1]==-5:
                        powerup_sound.play()
                        matrix[line_players[1]][collumn_players[1]]=0
                        collumn_players[1]+=1
                        bonusSpecial[1]=1
                        matrix[line_players[1]][collumn_players[1]]=4
                if event.key == pygame.K_SPACE and bombCollum==0:
                    bomb_sound.play()
                    bombLine=line_players[0]
                    bombCollum=collumn_players[0]
                    start_bomb = pygame.time.get_ticks()
                    one_explosion[0]=1
                if event.key == pygame.K_m and bombCollum2==0:
                    bomb_sound.play()
                    bombLine2=line_players[1]
                    bombCollum2=collumn_players[1]
                    start_bomb2 = pygame.time.get_ticks()
                    one_explosion[1]=1
                if event.key == pygame.K_x and bonusSpecial[0]==1:
                    bomb_sound.play()
                    print('Start bonus')
                    bonusSpecialTime[0]=pygame.time.get_ticks()
                    bonusSpecial[0]=2
                if event.key == pygame.K_n and bonusSpecial[1]==1:
                    bomb_sound.play()
                    print('Start bonus')
                    bonusSpecialTime[1]=pygame.time.get_ticks()
                    bonusSpecial[1]=2



        if pygame.time.get_ticks()-bonusSpecialTime[0]>5000 and bonusSpecial[0]==2:
            print('Over Bonus')
            bonusSpecialTime[0]=0
            bonusSpecial[0]=0

        if pygame.time.get_ticks()-bonusSpecialTime[1]>5000 and bonusSpecial[1]==2:
            print('Over Bonus')
            bonusSpecialTime[1]=0
            bonusSpecial[1]=0

        screen.blit(background, (0,100))

        if bombLine!=0 and bombCollum!=0 and pygame.time.get_ticks() - start_bomb < 2500:
            screen.blit(BombImg, (bombLine*40+7, bombCollum*40+80))
        elif bombLine!=0 and bombCollum!=0 and pygame.time.get_ticks() - start_bomb < 3500:
            explosion(bombLine, bombCollum, 0)
        elif pygame.time.get_ticks() - start_bomb > 3500 and bombLine!=0:
            dexplosion(bombLine, bombCollum, 0)
            bombLine=0
            bombCollum=0
            healthChange[0]=0
            healthChange[1]=0


        if  bombLine2!=0 and bombCollum2!=0 and pygame.time.get_ticks() - start_bomb2 < 2500:
            screen.blit(BombImg2, (bombLine2*40+7, bombCollum2*40+80))
        elif bombLine2!=0 and bombCollum2!=0 and pygame.time.get_ticks() - start_bomb2 < 3500:
            explosion(bombLine2, bombCollum2, 1)
        elif pygame.time.get_ticks() - start_bomb2 > 3500 and bombLine2!=0:
            dexplosion(bombLine2, bombCollum2, 1)
            bombLine2=0
            bombCollum2=0
            healthChange[0]=0
            healthChange[1]=0

        for i in range (13):
            for j in range (13):
                if matrix[i][j]==2:
                    screen.blit(stone, (i*40, j*40+80))
                if matrix[i][j]==1:
                    screen.blit(barrel, (i*40, j*40+80))
                if matrix[i][j]==-3:
                    screen.blit(Viata, (i*40, j*40+80))
                if matrix[i][j]==-4:
                    screen.blit(Arie, (i*40, j*40+80))
                if matrix[i][j]==-5:
                    screen.blit(Vest, (i*40, j*40+80))
                if matrix[i][j]>2:
                    if bonusSpecial[matrix[i][j]-3]==2:
                        screen.blit(SpecialPlayers[matrix[i][j]-3], (line_players[matrix[i][j]-3]*40, collumn_players[matrix[i][j]-3]*40+80))
                    else:
                        screen.blit(Players[matrix[i][j]-3], (line_players[matrix[i][j]-3]*40, collumn_players[matrix[i][j]-3]*40+80))

        showScore(textX,textY)

        pygame.display.update()
        #Ar trebui adaugat efectul ca block-ul indestructibil sa treaca peste player
        if iteratii>2500 and iteratii%5==0 and completat<2:
            if coloana_de_completat==coltMic and linie_de_completat>coltMic:
                if matrix[coloana_de_completat][linie_de_completat]==3:
                    #screen.blit(stone, (coloana_de_completat*40, linie_de_completat*40+80))
                    gameover_sound.play()
                    print('Player2 a castigat')
                    running=False
                if matrix[coloana_de_completat][linie_de_completat]==4:
                    #screen.blit(stone, (coloana_de_completat*40, linie_de_completat*40+80))
                    gameover_sound.play()
                    print('Player1 a castigat')
                    running=False
                matrix[coloana_de_completat][linie_de_completat]=2
                linie_de_completat+=-1
            if linie_de_completat==coltMic and coloana_de_completat<coltMare:
                if matrix[coloana_de_completat][linie_de_completat]==3:
                    #screen.blit(stone, (coloana_de_completat*40, linie_de_completat*40+80))
                    gameover_sound.play()
                    print('Player2 a castigat')
                    running=False
                if matrix[coloana_de_completat][linie_de_completat]==4:
                    #screen.blit(stone, (coloana_de_completat*40, linie_de_completat*40+80))
                    gameover_sound.play()
                    print('Player1 a castigat')
                    running=False
                matrix[coloana_de_completat][linie_de_completat]=2
                coloana_de_completat+=1
            if coloana_de_completat==coltMare and linie_de_completat<coltMare:
                if matrix[coloana_de_completat][linie_de_completat]==3:
                    #screen.blit(stone, (coloana_de_completat*40, linie_de_completat*40+80))
                    gameover_sound.play()
                    print('Player2 a castigat')
                    running=False
                if matrix[coloana_de_completat][linie_de_completat]==4:
                    #screen.blit(stone, (coloana_de_completat*40, linie_de_completat*40+80))
                    gameover_sound.play()
                    print('Player1 a castigat')
                    running=False
                matrix[coloana_de_completat][linie_de_completat]=2
                linie_de_completat+=1
            if linie_de_completat==coltMare and coloana_de_completat>coltMic:
                if matrix[coloana_de_completat][linie_de_completat]==3:
                    #screen.blit(stone, (coloana_de_completat*40, linie_de_completat*40+80))
                    gameover_sound.play()
                    print('Player2 a castigat')
                    running=False
                if matrix[coloana_de_completat][linie_de_completat]==4:
                    #screen.blit(stone, (coloana_de_completat*40, linie_de_completat*40+80))
                    gameover_sound.play()
                    print('Player1 a castigat')
                    running=False
                matrix[coloana_de_completat][linie_de_completat]=2
                coloana_de_completat+=-1
            if linie_de_completat==coltMare and coloana_de_completat==coltMic and completat==1:
                completat=2
            if linie_de_completat==coltMare and coloana_de_completat==coltMic and completat==0:
                coltMare+=-1
                linie_de_completat+=-1
                coloana_de_completat+=1
                coltMic+=1
                completat=1
        
        if iteratii==8000:
            if score_value[0]>score_value[1]:
                gameover_sound.play()
                print('Player1 a castigat')
                running=False
            if score_value[1]>score_value[0]:
                gameover_sound.play()
                print('Player2 a castigat')
                running = False
            if score_value[0]==score_value[1]:
                gameover_sound.play()
                print('Egalitate')
                running=False

if mod_de_joc==2:
    while running:
        

        iteratii+=1
        
        screen.fill((128,128,0))
        screen.blit(render,(450, 189) )
        screen.blit(speech, (520, 10))
        while game_status<0:
            pauza()
            pygame.display.update()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game_status = game_status*(-1)
                        continue

        if playersHealth[0]==0:
            gameover_sound.play()
            print('Player2 a castigat')
            running = False
            continue
        if playersHealth[1]==0:
            gameover_sound.play()
            running = False
            print('Player1 a castigat')
            continue

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_status = game_status*(-1)
                    if game_status < 0:
                        print('Pauza')
                        continue
                if event.key == pygame.K_a:
                    if  matrix[line_players[0]-1][collumn_players[0]]==0 and passBomb(line_players[0]-1, collumn_players[0])==True:
                        matrix[line_players[0]][collumn_players[0]]=0
                        line_players[0]+=-1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]-1][collumn_players[0]]==-4:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        line_players[0]+=-1
                        bombArea[0]+=1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]-1][collumn_players[0]]==-3:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        line_players[0]+=-1
                        playersHealth[0]+=1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif matrix[line_players[0]-1][collumn_players[0]]==-5:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        line_players[0]+=-1
                        bonusSpecial[0]=1
                        matrix[line_players[0]][collumn_players[0]]=3
                if event.key == pygame.K_d:
                    if  matrix[line_players[0]+1][collumn_players[0]]==0 and passBomb(line_players[0]+1,collumn_players[0])==True:
                        matrix[line_players[0]][collumn_players[0]]=0
                        line_players[0]+=1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]+1][collumn_players[0]]==-4:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        line_players[0]+=1
                        bombArea[0]+=1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]+1][collumn_players[0]]==-3:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        line_players[0]+=1
                        playersHealth[0]+=1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]+1][collumn_players[0]]==-5:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        line_players[0]+=1
                        bonusSpecial[0]=1
                        matrix[line_players[0]][collumn_players[0]]=3
                if event.key == pygame.K_w:
                    if  matrix[line_players[0]][collumn_players[0]-1]==0 and passBomb(line_players[0],collumn_players[0]-1)==True:
                        matrix[line_players[0]][collumn_players[0]]=0
                        collumn_players[0]+=-1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]][collumn_players[0]-1]==-4:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        collumn_players[0]+=-1
                        bombArea[0]+=1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]][collumn_players[0]-1]==-3:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        collumn_players[0]+=-1
                        playersHealth[0]+=1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]][collumn_players[0]-1]==-5:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        collumn_players[0]+=-1
                        bonusSpecial[0]=1
                        matrix[line_players[0]][collumn_players[0]]=3
                if event.key == pygame.K_s:
                    if  matrix[line_players[0]][collumn_players[0]+1]==0 and passBomb(line_players[0],collumn_players[0]+1)==True:
                        matrix[line_players[0]][collumn_players[0]]=0
                        collumn_players[0]+=1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]][collumn_players[0]+1]==-4:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        collumn_players[0]+=1
                        bombArea[0]+=1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]][collumn_players[0]+1]==-3:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        collumn_players[0]+=1
                        playersHealth[0]+=1
                        matrix[line_players[0]][collumn_players[0]]=3
                    elif  matrix[line_players[0]][collumn_players[0]+1]==-5:
                        powerup_sound.play()
                        matrix[line_players[0]][collumn_players[0]]=0
                        collumn_players[0]+=1
                        bonusSpecial[0]=1
                        matrix[line_players[0]][collumn_players[0]]=3
                if event.key == pygame.K_SPACE and bombCollum==0:
                    bomb_sound.play()
                    bombLine=line_players[0]
                    bombCollum=collumn_players[0]
                    start_bomb = pygame.time.get_ticks()
                    one_explosion[0]=1
                if event.key == pygame.K_x and bonusSpecial[0]==1:
                    bomb_sound.play()
                    print('Start bonus')
                    bonusSpecialTime[0]=pygame.time.get_ticks()
                    bonusSpecial[0]=2

        #MISCARE BOT
        directie=7
        if iteratii%7==0:
            directie=random.randint(1,4)
            directie=directie*2
        pune_bomba=0


        if directie==4:
            if  matrix[line_players[1]-1][collumn_players[1]]==0 and passBomb(line_players[1]-1,collumn_players[1])==True:
                matrix[line_players[1]][collumn_players[1]]=0
                line_players[1]+=-1
                matrix[line_players[1]][collumn_players[1]]=4
            elif  matrix[line_players[1]-1][collumn_players[1]]==-4:
                powerup_sound.play()
                matrix[line_players[1]][collumn_players[1]]=0
                line_players[1]+=-1
                playersHealth[1]+=1
                matrix[line_players[1]][collumn_players[1]]=4
            elif  matrix[line_players[1]-1][collumn_players[1]]==-3:
                powerup_sound.play()
                matrix[line_players[1]][collumn_players[1]]=0
                line_players[1]+=-1
                playersHealth[1]+=1
                matrix[line_players[1]][collumn_players[1]]=4
            elif  matrix[line_players[1]-1][collumn_players[1]]==-5:
                powerup_sound.play()
                matrix[line_players[1]][collumn_players[1]]=0
                line_players[1]+=-1
                bonusSpecial[1]=1
                matrix[line_players[1]][collumn_players[1]]=4
            elif  matrix[line_players[1]-1][collumn_players[1]]==1 or matrix[line_players[1]-1][collumn_players[1]]==3:
                pune_bomba=1
        if directie==6:
            if  matrix[line_players[1]+1][collumn_players[1]]==0 and passBomb(line_players[1]+1,collumn_players[1])==True:
                matrix[line_players[1]][collumn_players[1]]=0
                line_players[1]+=1
                matrix[line_players[1]][collumn_players[1]]=4
            elif  matrix[line_players[1]+1][collumn_players[1]]==-3:
                powerup_sound.play()
                matrix[line_players[1]][collumn_players[1]]=0
                line_players[1]+=1
                playersHealth[1]+=1
                matrix[line_players[1]][collumn_players[1]]=4
            elif  matrix[line_players[1]+1][collumn_players[1]]==-4:
                powerup_sound.play()
                matrix[line_players[1]][collumn_players[1]]=0
                line_players[1]+=1
                bombArea[1]+=1
                matrix[line_players[1]][collumn_players[1]]=4
            elif  matrix[line_players[1]+1][collumn_players[1]]==-5:
                powerup_sound.play()
                matrix[line_players[1]][collumn_players[1]]=0
                line_players[1]+=1
                bonusSpecial[1]=1
                matrix[line_players[1]][collumn_players[1]]=4
            elif  matrix[line_players[1]+1][collumn_players[1]]==1 or matrix[line_players[1]+1][collumn_players[1]]==3:
                pune_bomba=1
        if directie==2:
            if  matrix[line_players[1]][collumn_players[1]-1]==0 and passBomb(line_players[1],collumn_players[1]-1)==True:
                matrix[line_players[1]][collumn_players[1]]=0
                collumn_players[1]+=-1
                matrix[line_players[1]][collumn_players[1]]=4
            elif  matrix[line_players[1]][collumn_players[1]-1]==-4:
                powerup_sound.play()
                matrix[line_players[1]][collumn_players[1]]=0
                collumn_players[1]+=-1
                bombArea[1]+=1
                matrix[line_players[1]][collumn_players[1]]=4
            elif  matrix[line_players[1]][collumn_players[1]-1]==-3:
                powerup_sound.play()
                matrix[line_players[1]][collumn_players[1]]=0
                collumn_players[1]+=-1
                playersHealth[1]+=1
                matrix[line_players[1]][collumn_players[1]]=4
            elif  matrix[line_players[1]][collumn_players[1]-1]==-5:
                powerup_sound.play()
                matrix[line_players[1]][collumn_players[1]]=0
                collumn_players[1]+=-1
                bonusSpecial[1]=1
                matrix[line_players[1]][collumn_players[1]]=4
            elif  matrix[line_players[1]][collumn_players[1]-1]==1 or matrix[line_players[1]][collumn_players[1]-1]==3:
                pune_bomba=1
        if directie==8:
            if  matrix[line_players[1]][collumn_players[1]+1]==0 and passBomb(line_players[1],collumn_players[1]+1)==True:
                matrix[line_players[1]][collumn_players[1]]=0
                collumn_players[1]+=1
                matrix[line_players[1]][collumn_players[1]]=4
            elif  matrix[line_players[1]][collumn_players[1]+1]==-4:
                powerup_sound.play()
                matrix[line_players[1]][collumn_players[1]]=0
                collumn_players[1]+=1
                bombArea[1]+=1
                matrix[line_players[1]][collumn_players[1]]=4
            elif  matrix[line_players[1]][collumn_players[1]+1]==-3:
                powerup_sound.play()
                matrix[line_players[1]][collumn_players[1]]=0
                collumn_players[1]+=1
                playersHealth[1]+=1
                matrix[line_players[1]][collumn_players[1]]=4
            elif  matrix[line_players[1]][collumn_players[1]+1]==-5:
                powerup_sound.play()
                matrix[line_players[1]][collumn_players[1]]=0
                collumn_players[1]+=1
                bonusSpecial[1]=1
                matrix[line_players[1]][collumn_players[1]]=4
            elif  matrix[line_players[1]][collumn_players[1]+1]==1 or matrix[line_players[1]][collumn_players[1]+1]==3:
                pune_bomba=1
        if pune_bomba and bombCollum2==0:
            bomb_sound.play()
            bombLine2=line_players[1]
            bombCollum2=collumn_players[1]
            start_bomb2 = pygame.time.get_ticks()
            one_explosion[1]=1
            pune_bomba=0
        if directie==9 and bonusSpecial[1]==1:
            bomb_sound.play()
            print('Start bonus')
            bonusSpecialTime[1]=pygame.time.get_ticks()
            bonusSpecial[1]=2



        if pygame.time.get_ticks()-bonusSpecialTime[0]>5000 and bonusSpecial[0]==2:
            print('Over Bonus')
            bonusSpecialTime[0]=0
            bonusSpecial[0]=0

        if pygame.time.get_ticks()-bonusSpecialTime[1]>5000 and bonusSpecial[1]==2:
            print('Over Bonus')
            bonusSpecialTime[1]=0
            bonusSpecial[1]=0

        screen.blit(background, (0,100))

        if bombLine!=0 and bombCollum!=0 and pygame.time.get_ticks() - start_bomb < 2500:
            screen.blit(BombImg, (bombLine*40+7, bombCollum*40+80))
        elif bombLine!=0 and bombCollum!=0 and pygame.time.get_ticks() - start_bomb < 3500:
            explosion(bombLine, bombCollum, 0)
        elif pygame.time.get_ticks() - start_bomb > 3500 and bombLine!=0:
            dexplosion(bombLine, bombCollum, 0)
            bombLine=0
            bombCollum=0
            healthChange[0]=0
            healthChange[1]=0


        if  bombLine2!=0 and bombCollum2!=0 and pygame.time.get_ticks() - start_bomb2 < 2500:
            screen.blit(BombImg2, (bombLine2*40+7, bombCollum2*40+80))
        elif bombLine2!=0 and bombCollum2!=0 and pygame.time.get_ticks() - start_bomb2 < 3500:
            explosion(bombLine2, bombCollum2, 1)
        elif pygame.time.get_ticks() - start_bomb2 > 3500 and bombLine2!=0:
            dexplosion(bombLine2, bombCollum2, 1)
            bombLine2=0
            bombCollum2=0
            healthChange[0]=0
            healthChange[1]=0

        for i in range (13):
            for j in range (13):
                if matrix[i][j]==2:
                    screen.blit(stone, (i*40, j*40+80))
                if matrix[i][j]==1:
                    screen.blit(barrel, (i*40, j*40+80))
                if matrix[i][j]==-3:
                    screen.blit(Viata, (i*40, j*40+80))
                if matrix[i][j]==-4:
                    screen.blit(Arie, (i*40, j*40+80))
                if matrix[i][j]==-5:
                    screen.blit(Vest, (i*40, j*40+80))
                if matrix[i][j]>2:
                    if bonusSpecial[matrix[i][j]-3]==2:
                        screen.blit(SpecialPlayers[matrix[i][j]-3], (line_players[matrix[i][j]-3]*40, collumn_players[matrix[i][j]-3]*40+80))
                    else:
                        screen.blit(Players[matrix[i][j]-3], (line_players[matrix[i][j]-3]*40, collumn_players[matrix[i][j]-3]*40+80))

        showScore(textX,textY)

        pygame.display.update()
        
        if iteratii>8000 and iteratii%5==0 and completat<2:
            if coloana_de_completat==coltMic and linie_de_completat>coltMic:
                if matrix[coloana_de_completat][linie_de_completat]==3:
                    #screen.blit(stone, (coloana_de_completat*40, linie_de_completat*40+80))
                    gameover_sound.play()
                    print('Player2 a castigat')
                    running=False
                if matrix[coloana_de_completat][linie_de_completat]==4:
                    #screen.blit(stone, (coloana_de_completat*40, linie_de_completat*40+80))
                    gameover_sound.play()
                    print('Player1 a castigat')
                    running=False
                matrix[coloana_de_completat][linie_de_completat]=2
                linie_de_completat+=-1
            if linie_de_completat==coltMic and coloana_de_completat<coltMare:
                if matrix[coloana_de_completat][linie_de_completat]==3:
                    #screen.blit(stone, (coloana_de_completat*40, linie_de_completat*40+80))
                    gameover_sound.play()
                    print('Player2 a castigat')
                    running=False
                if matrix[coloana_de_completat][linie_de_completat]==4:
                    #screen.blit(stone, (coloana_de_completat*40, linie_de_completat*40+80))
                    gameover_sound.play()
                    print('Player1 a castigat')
                    running=False
                matrix[coloana_de_completat][linie_de_completat]=2
                coloana_de_completat+=1
            if coloana_de_completat==coltMare and linie_de_completat<coltMare:
                if matrix[coloana_de_completat][linie_de_completat]==3:
                    #screen.blit(stone, (coloana_de_completat*40, linie_de_completat*40+80))
                    gameover_sound.play()
                    print('Player2 a castigat')
                    running=False
                if matrix[coloana_de_completat][linie_de_completat]==4:
                    #screen.blit(stone, (coloana_de_completat*40, linie_de_completat*40+80))
                    gameover_sound.play()
                    print('Player1 a castigat')
                    running=False
                matrix[coloana_de_completat][linie_de_completat]=2
                linie_de_completat+=1
            if linie_de_completat==coltMare and coloana_de_completat>coltMic:
                if matrix[coloana_de_completat][linie_de_completat]==3:
                    #screen.blit(stone, (coloana_de_completat*40, linie_de_completat*40+80))
                    gameover_sound.play()
                    print('Player2 a castigat')
                    running=False
                if matrix[coloana_de_completat][linie_de_completat]==4:
                    #screen.blit(stone, (coloana_de_completat*40, linie_de_completat*40+80))
                    gameover_sound.play()
                    print('Player1 a castigat')
                    running=False
                matrix[coloana_de_completat][linie_de_completat]=2
                coloana_de_completat+=-1
            if linie_de_completat==coltMare and coloana_de_completat==coltMic and completat==1:
                completat=2
            if linie_de_completat==coltMare and coloana_de_completat==coltMic and completat==0:
                coltMare+=-1
                linie_de_completat+=-1
                coloana_de_completat+=1
                coltMic+=1
                completat=1











        
