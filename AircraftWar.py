# 飞机大战
#import pygame
import time
import random
import math
# 下面代码是为了取消因引用pygame模块而打印出的字符串。
import os, sys
with open(os.devnull, 'w') as f:
    # disable stdout
    oldstdout = sys.stdout
    sys.stdout = f
    import pygame
    # enable stdout
    sys.stdout = oldstdout

# 初始化页面
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("飞机大战")
# 加载背景图片
bg = pygame.image.load('./resource/bg.png')

# 添加背景音乐
pygame.mixer.music.load('./resource/bg.wav')
pygame.mixer.music.play(-1) # 单曲循环播放
# 添加击中音效
BaoSound = pygame.mixer.Sound('./resource/exp.wav')
loser = pygame.mixer.Sound('./resource/laser.wav')

# 创建用户飞机
player = pygame.image.load('./resource/player.png')
playerx = 400-32   # 玩家的x坐标
playery = 500   # 玩家的Y坐标
playerxstep = 0
playerystep = 0
player_HP = 10
# 显示飞机
def ShowAircraft():
    global playerx,playery
    playerx += playerxstep
    playery += playerystep
    if playery>500:
        playery = 500
    elif playery<0:
        playery = 0
    if playerx>736:
        playerx = 735
    elif playerx<0:
        playerx = 0
    screen.blit(player,(playerx,playery))# 显示飞机

# 分数与生命值,wave
score = 0
#font = pygame.font.Font('freesansbold.ttf', 32)
font = pygame.font.SysFont('simsunnsimsun',32)
def drawScore():# 分数、生命值以及波数
    text = f'score: {score}'
    text2 = f'HP: {player_HP}'
    text3 = '{:2d}\'d wave'.format(session)
    score_render = font.render(text, True, (255, 0, 0))
    PH_render = font.render(text2, True, (0, 255, 0))
    session_render = font.render(text3, True, (255, 0, 0))
    screen.blit(score_render, (10, 10))
    screen.blit(session_render, (10, 50))
    screen.blit(PH_render, (700, 10))
over_font = pygame.font.SysFont('simsunnsimsun',64)
def CheckIsOver():# 结束游戏显示
    text = 'Game Over'
    text2 = 'Score: {:>4}'.format(score)
    render = over_font.render(text, True, (255, 0, 0))
    render2 = over_font.render(text2, True, (255, 0, 0))
    screen.blit(render, (280, 250))
    screen.blit(render2, (290, 320))

# 创建敌人类
ufoImg = pygame.image.load('./resource/ufo.png')
enemy2Img = pygame.image.load('./resource/enemy2.png')
enemyImg = pygame.image.load('./resource/enemy.png')
class EnemyClass:
    def __init__(self,enemyImg,left_M=0,right_M=735,enemystep = 5):
        self.left_M = left_M
        self.right_M = right_M
        self.x = random.randrange(left_M,right_M,20)
        self.y = random.randrange(0,200,20)
        self.step = random.choice([enemystep, -enemystep])
        self.Img = enemyImg
    def move(self):
        self.x += self.step
        if self.x%20 == 0:
            self.y += 4
        if self.x > self.right_M:
            self.step = -self.step
            #self.y += 40
        elif self.x < self.left_M:
            self.step = -self.step

# 创建子弹类
bulletImg = pygame.image.load('./resource/bullet.png')
class BullerClass(object):
    def __init__(self, bulletImg, x , y,bulletStep=20):
        self.bulletImg = bulletImg
        self.x = x+16
        self.y = y-10
        self.step = bulletStep

    def move(self):
        self.y -= self.step

# 定义一个敌人列表
enemies = []
enemystep = 5 #敌人速度
#创建15个随机敌人（默认15）
def EnemyCreate(N=15):
    global enemies, enemystep
    for i in range(N):
        a = random.random()
        if a<0.35:
            Img = enemyImg
        elif a<0.7:
            Img = enemy2Img
        else:
            Img = ufoImg
        enemies.append(EnemyClass(Img, enemystep = enemystep))
# 显示所有敌人
def ShowEnemies(enemies, Down_M = 500):# 默认下边界为400
    global player_HP
    enemy_clear = []
    for i in range(len(enemies)):# 显示所有敌人
        enemies[i].move()
        if enemies[i].y > Down_M:
            enemy_clear.append(i)
        else:
            screen.blit(enemies[i].Img,(enemies[i].x, enemies[i].y))
    enemy_clear.sort(reverse=True)# 排序从大到小
    for i in enemy_clear:
        del enemies[i]
        player_HP -= 1

# 定义一个子弹列表
bullets = []
# 显示所有子弹
def ShowBullets(bullets):
    bullet_clear = []
    for i in range(len(bullets)):
        bullets[i].move()
        if bullets[i].y<0:
            bullet_clear.append(i)
        else:
            screen.blit(bullets[i].bulletImg,(bullets[i].x, bullets[i].y))
    for i in bullet_clear:
        del bullets[i]

# 两个对象之间的距离（子弹与敌人）
def destance(bullet, enemy):
    x = bullet.x-enemy.x
    y = bullet.y-enemy.y
    return math.sqrt(x**2+y**2)
# 击中检查
def hit(bullets, enemies):
    global score
    bulletCler = []
    enemyCler = []
    for i in range(len(bullets)):
        for j in range(len(enemies)):
            if destance(bullets[i], enemies[j])<30:
                #射中了
                bulletCler.append(i)
                enemyCler.append(j)
    bulletCler = list(set(bulletCler))
    bulletCler.sort(reverse=True)
    for i in bulletCler:
        del bullets[i]
    enemyCler = list(set(enemyCler))
    enemyCler.sort(reverse=True)
    for i in enemyCler:
        BaoSound.play()
        del enemies[i] 
        score += 1

IsOver = False
running = True
session = 0 # 当前敌人第session波
#游戏主循环
while running:
    screen.blit(bg,(0,0))
    for event in pygame.event.get():# 人机交互，事件获取
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                playerxstep = 20
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                playerxstep = -20
            elif event.key in (pygame.K_UP, pygame.K_w):
                playerystep = -20
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                playerystep = 20
            elif event.key == pygame.K_SPACE:
                if not IsOver:
                    bullets.append(BullerClass(bulletImg, playerx, playery))
            elif event.key == pygame.K_TAB:
                print('游戏开始......')
                pygame.mixer.music.play(-1) # 单曲循环播放
                IsOver = False;session = 0;player_HP = 10;score = 0;enemystep = 5
        elif event.type == pygame.KEYUP:
             playerxstep = 0 
             playerystep = 0
    if not IsOver:# 游戏未结束时，操作
        ShowBullets(bullets)    # 显示子弹
        ShowEnemies(enemies)    # 显示所有敌人
        ShowAircraft()          # 显示飞机
        hit(bullets, enemies)   # 击中检测

        if len(enemies) == 0:# 敌人为0时，产生敌人
            EnemyCreate()
            session += 1

        # 敌人等级设置（速度）
        if session == 2:
            enemystep = 10
        elif session ==4:
            enemystep = 15
        elif session == 6:
            enemystep = 20

        drawScore() # 显示分数

        if player_HP <= 0:# 生命值低于0时，游戏结束
            loser.play()
            print('游戏结束......')
            enemies.clear() # 清空敌人
            bullets.clear() # 清空子弹
            IsOver = True
    else:   # 游戏结束时，操作
        screen.blit(player, (400-32, 500))
        CheckIsOver()   # 结束游戏显示

    pygame.display.update()
    time.sleep(0.05)