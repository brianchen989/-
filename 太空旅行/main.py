#spirit
from distutils.command.bdist import show_formats
from multiprocessing.connection import wait
import pygame
import random
import os

GREEN = (0,255,0)
WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)

FPS = 60

WIDTH = 500
HEIGHT = 600

#遊戲初始化&創建視窗
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))#視窗大小
pygame.display.set_caption("太空漫遊")#左上標題
clock = pygame.time.Clock()

#載入圖片
background_img = pygame.image.load(os.path.join("img","background.png")).convert()
player_img = pygame.image.load(os.path.join("img","player.png")).convert()
#rock_img = pygame.image.load(os.path.join("img","rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("img","bullet.png")).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())
    
#載入音樂
shoot_sound = pygame.mixer.Sound(os.path.join("sound","pow1.wav"))

expl_sound = [
    pygame.mixer.Sound(os.path.join("sound","expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound","expl1.wav"))

]
#pygame.mixer.music.load(os.path.join("sound","background.ogg"))

font_name = pygame.font.match_font("arial")
def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name , size)
    text_surface = font.render(text,True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface,text_rect)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,38))#放圖片
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()#定位(框起來)
        self.radius = 20#半徑
        #pygame.draw.circle(self.image , RED , self.rect.center,self.radius)畫圓
        self.rect.centerx = WIDTH/2#擺放x
        self.rect.bottom = HEIGHT-10
        #self.rect.x = 200(設定X座標)
        #self.rect.y = 200(設定y座標)
        self.speedx = 8#設定移動速度
    def update(self):
        key_press = pygame.key.get_pressed()#判斷鍵盤上是否有按鍵被按
        if key_press[pygame.K_RIGHT]:#右鍵是否被按
            self.rect.x += self.speedx#向右移
        if key_press[pygame.K_LEFT]:#左鍵是否被按
            self.rect.x -= self.speedx#向左移
        if self.rect.right > WIDTH:#右邊卡住
            self.rect.right = WIDTH
        if self.rect.left < 0:#左邊卡住
            self.rect.left = 0 

    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()
        
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK) 
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()#定位(框起來)
        self.radius = int(self.rect.width*0.85/2)#半徑
        #pygame.draw.circle(self.image , RED , self.rect.center,self.radius)畫圓
        self.rect.x = random.randrange(0,WIDTH-self.rect.width)
        self.rect.y =  random.randrange(-180,-100)
        
        self.speedy = random.randrange(2,10)#設定移動速度
        #self.speedy = 1
        self.speedx = random.randrange(-5,50)
        #self.speedx = 1
        self.total_degree = 0
        self.rot_degree = random.randrange(-20,20)
    
    
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top  >HEIGHT or self.rect.left >WIDTH or self.rect.right <0:
            self.rect = self.image.get_rect()#定位(框起來)
            self.rect.x = random.randrange(0,WIDTH-self.rect.width)
            self.rect.y =  random.randrange(-100,-40)
        
            self.speedy = random.randrange(2,15)#設定移動速度
            self.speedx = random.randrange(-5,5)
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()#定位(框起來)
        self.rect.centerx = x#擺放x
        self.rect.bottom =y
        #self.rect.x = 200(設定X座標)
        #self.rect.y = 200(設定y座標)
        self.speedy = -10 #設定移動速度
    def update(self):
       self.rect.y += self.speedy
       if self.rect.bottom <0:
            self.kill()

        

all_sprites = pygame.sprite.Group()#創造腳色並加入
rocks = pygame.sprite.Group()#創造石頭並加入
bullets = pygame.sprite.Group()#創造子彈並加入
player = Player()#創造腳色並加入
all_sprites.add(player)
for i in range(8):
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)
score = 0
#pygame.mixer.music.play(-1)
#遊戲迴圈
running = True
while running:
    clock.tick(FPS)#螢幕顯示速率
    # 取得輸入
    for event in pygame.event.get():#接收訊息
        if event.type == pygame.QUIT:
            running = False#關遊戲
        elif event.type == pygame.KEYDOWN: #是否按下按鍵
            if event.key == pygame.K_SPACE: #是否按下空白鍵
                player.shoot()
        

    # 更新遊戲
    all_sprites.update()
    hits = pygame.sprite.groupcollide( rocks,bullets, True, True)#子彈石頭碰撞後刪除
    for hit in hits:
        random.choice(expl_sound).play() 
        score += hit.radius
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)
    hits = pygame.sprite.spritecollide(player,rocks,False,pygame.sprite.collide_circle) 
    if hits:
        running = False


    # 畫面顯示
    screen.fill(BLACK)#視窗顏色
    screen.blit(background_img, (0,0))#畫background_img
    all_sprites.draw(screen) 
    draw_text(screen,str(score),18,WIDTH/2,10)
    pygame.display.update()
pygame.quit()