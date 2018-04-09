# shooting game
import pygame#基本ゲームライブラリ
import math#数学用ライブラリ
import random#乱数

WIDTH = 640
HEIGHT = 480
BLACK = (0,0,0)
WHITE = (255,255,255)
OUTSIDE = 999

class Spclass(pygame.sprite.Sprite):#スプライトクラス
    def __init__(self,x,y,angle,num):
        pygame.sprite.Sprite.__init__(self)
        tempimage = pygame.transform.rotate(\
        charas[num].image, -angle)
        self.image = tempimage#使用する画像
        self.rect = self.image.get_rect()
        self.rect.centerx = x #Sprite中央のx座標
        self.rect.centery = y #Sprite中央のy座標
        self.angle = angle #Spriteの角度
        self.hp = charas[num].hp #キャラに設定されているhpを設置
        self.enemy = charas[num].enemy #敵フラグを設置
        self.time = 0


class Explosion(Spclass):#爆発クラス
    def update(self):
        if self.time > 10:
            #10ms経つと爆発が消える
            self.rect.centerx = OUTSIDE

class Shot(Spclass):#自機の弾丸クラス
    def update(self):
        self.rect.centery -= 8
        hitlist = pygame.sprite.spritecollide(\
        self, allgroup, False)
        for sp in hitlist:
            if sp.enemy == False or sp.hp == 99: continue
            self.rect.centerx = OUTSIDE
            sp.hp -= 1
            #当たったらhpを-1する
            break

class Fireball(Spclass):#敵機の弾丸クラス
    def update(self):
        rad = math.radians(self.angle - 90)
        self.rect.centerx += (math.cos(rad)) * 4
        self.rect.centery += (math.sin(rad)) * 4

class Player(Spclass):#自機クラス
    def update(self):
        press = pygame.key.get_pressed()#キー入力を取得
        if (press[pygame.K_UP]):self.rect.centery -= 4
        if(press[pygame.K_DOWN]):
            self.rect.centery += 4
        if(press[pygame.K_LEFT]):
            self.rect.centerx -= 4
        if(press[pygame.K_RIGHT]):
            self.rect.centerx += 4
        if(self.rect.centerx < 16):
            self.rect.centerx = 16
        if(self.rect.centery < 16):
            self.rect.centery = 16
        if(self.rect.centerx > WIDTH - 16):
            self.rect.centerx = WIDTH - 16
        if(self.rect.centery > HEIGHT - 16):
            self.rect.centery = HEIGHT - 16
        if(press[pygame.K_SPACE] != 0) and \
        (self.time % 10 == 0):#弾丸を撃てる頻度の設定
            newsp = Shot(\
            self.rect.centerx,self.rect.centery,0,1)
            allgroup.add(newsp)
            hitlist = pygame.sprite.spritecollide(\
            self,allgroup,False)
            for sp in hitlist:
                if sp.enemy == True:
                    self.hp -= 1
                    sp.hp -= 1
                    break

class Fighter(Spclass):
    def update(self):
        #self.rect.centerx += 2
        #if self.rect.centerx + 10 >= WIDTH:
        #    self.rect.centerx = 10
        if self.time // 200 % 2 ==0:
            self.rect.centerx += 2
        else:
            self.rect.centerx += -2

        self.rect.centery += \
        int((self.time % 200) / 100) * 2 -1
        # 0 or 2 を1引いてるから、等確率で上下に移動する
        if allgroup.has(player) == 0 or \
        random.randint(0,100) != 0: return
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        angle = math.degrees(math.atan2(dy,dx))+90
        newsp = Fireball(self.rect.centerx,\
        self.rect.centery,angle,2)
        allgroup.add(newsp)

class Boss(Spclass):
    def update(self):
        if(self.time < 100):
            self.rect.centery += 1
            return
        rad = math.radians(self.time - 100)
        self.rect.centerx = \
        (WIDTH/2) + (math.sin(rad) * 200)
        if(self.time % 3 == 0):
            angle = (self.time * 4) % 360
            newsp = Fireball(self.rect.centerx, \
            self.rect.centery,angle,2)
            allgroup.add(newsp)

class Characlass:
    def __init__(self,filename,hp,enemy):
        self.image = \
        pygame.image.load(filename).convert()
        #colorkey = self.image.get_at((0,0))
        #self.image.set_colorkey(colorkey)
        self.image.set_colorkey(BLACK)
        self.hp = hp
        self.enemy = enemy

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(u"shootinggame")#set title on the window
myfont = pygame.font.Font(None,48)
myclock = pygame.time.Clock()
charas = []
charas.append(Characlass("explosion.png",1,False))#(使用する画像,hp,敵フラグ)
charas.append(Characlass("mybullet.png",1,False))
charas.append(Characlass("enemybullet.jpg",99,True))
charas.append(Characlass("player.png",1,False))
charas.append(Characlass("yellow.png",1,True))
charas.append(Characlass("boss.png",10,True))
stars = []
for i in range(10):
    x = random.randint(0,WIDTH - 1)
    y = random.randint(0,HEIGHT - 1)
    stars.append([x,y,2,2])

allgroup = pygame.sprite.Group()
endflag = 0
while endflag == 0:
    allgroup.empty()
    player = Player(WIDTH/2,HEIGHT*3/4,0,3)
    allgroup.add(player)
    bosstimer = 60 * 20
    #20秒でボスが出現する仕様
    gameover = 0
    while endflag == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: endflag = 1
        screen.fill(BLACK)
        for i in range(len(stars)):
            stars[i][1] = (stars[i][1]+i+1) % HEIGHT
            pygame.draw.rect(screen, WHITE,stars[i])
        bosstimer -= 1
        if bosstimer == 0:
            boss = Boss(WIDTH/2, 0, 180, 5)
            allgroup.add(boss)
        elif bosstimer < 0:
            if allgroup.has(boss) == 0: bosstimer = 60*20
        elif random.randint(0,10) == 0: #ノーマル敵の発生率を変える
            x = random.randint(0,WIDTH - 200) + 100
            newsp = Fighter(x, 100, 180, 4)#敵クラス(x座標,y座標,物体の角度,Sprite番号)
            allgroup.add(newsp)
        allgroup.update()
        for sp in allgroup.sprites():
            sp.time += 1
            x = sp.rect.centerx
            y = sp.rect.centery
            if sp.hp <= 0:
                allgroup.remove(sp)
                newsp = Explosion(x,y,0,0)
                allgroup.add(newsp)
            if x < 0 or x > WIDTH or y < 0 or y > HEIGHT:
                allgroup.remove(sp)
        allgroup.draw(screen)
        if allgroup.has(player) == 0:
            imagetext = \
            myfont.render("GAME OVER", True, WHITE)
            screen.blit(imagetext,(230,200))
            gameover += 1
            if gameover >= 120: break
        myclock.tick(60)
        pygame.display.flip()
pygame.quit()