from random import *
from pygame import *
import time as t

st = t.time()
shop_st = t.time()

#class
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


p_shoot = 0.5
p_speed = 5
class Player(GameSprite):
    def __init__(self, shoot, player_image, player_x, player_y, player_width, player_height, player_speed):
        self.shoot = p_shoot
        super().__init__(player_image, player_x, player_y, player_width, player_height, player_speed)
    def move(self):
        keys = key.get_pressed()
        if tekcor.purshed == 0:
            if keys[K_LEFT] and self.rect.x >= 0:
                self.rect.x -= self.speed
            if keys[K_RIGHT] and self.rect.x <= win_width - player_width:
                self.rect.x += self.speed
            if keys[K_UP] and self.rect.y >=0:
                self.rect.y -= self.speed
            if keys[K_DOWN] and self.rect.bottom <= win_height:
                self.rect.y += self.speed
        else:
            if keys[K_RIGHT] and self.rect.x >= 0:
                self.rect.x -= self.speed
            if keys[K_LEFT] and self.rect.x <= win_width - player_width:
                self.rect.x += self.speed
            if keys[K_DOWN] and self.rect.y >=0:
                self.rect.y -= self.speed
            if keys[K_UP] and self.rect.bottom <= win_height:
                self.rect.y += self.speed
        self.reset()
        #debug
        if keys[K_p]:
            print(mouse.get_pos())

#        if mouse.get_pressed()[2]:
#            if self.rect.x < mouse.get_pos()[0] - self.rect.width/2:
#                self.rect.x += self.speed
#            else:
#                self.rect.x -= self.speed

    def fire(self):
        global score
        keys = key.get_pressed()
        global en, st
        if not rrocket.purshed > 0:
            if keys[K_SPACE] and en - st >= self.shoot:
                fire.play(1)
                bullet = Bullet("bullet.png", self.rect.x+15, self.rect.y, 40, 70, 15)
                bullet_group.add(bullet)
                st = t.time()
        if keys[K_SPACE] and en - st >= self.shoot:
            fire.play(2)
            bullet = Bullet("bullet.png", self.rect.left, self.rect.y, 40, 70, 15)
            bullet_group.add(bullet)
            bullet = Bullet("bullet.png", self.rect.right - bullet.rect.width, self.rect.y, 40, 70, 15,)
            bullet_group.add(bullet)
            st = t.time()
    
        if keys[K_q] and en - st >= 1 and bomb.purshed >= 1:
            for enemy in enemy_group:
                enemy_group.remove(enemy)
                score += 1
            for asteroid in asteroid_group:
                asteroid_group.remove(asteroid)
                self.speed += 1
            bomb.purshed -= 1
            st = t.time()

class Enemy(GameSprite):
    def move(self):
        self.rect.y += self.speed
        self.reset()

class Bullet(GameSprite):
    def shooting(self):
        self.rect.y -= self.speed
        self.reset()

class Asteroid(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed, touched):
        super().__init__(player_image, player_x, player_y, player_width, player_height, player_speed)
        self.touched = touched
    def move(self):
        self.rect.y += self.speed
        self.reset()

class Item(GameSprite):
    def __init__(self,purshed, cost, player_image, player_x, player_y, player_width, player_height, player_speed):
        self.purshed = 0
        self.cost = cost
        super().__init__(player_image, player_x, player_y, player_width, player_height, player_speed)
        items_group.add(self)

    def mechanics(self, speed, shoot):
        if speed != 0:
            player.speed += speed
        if shoot != 0:
            player.shoot -= shoot
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        cost_au = font1.render(str(self.cost), True, (255, 255, 255), (0, 0, 0))
        window.blit(cost_au, (self.rect.x + 50 /2, self.rect.y + 50))



font.init()
font1 = font.SysFont("Arial", 20)
font_end = font.SysFont("Arial", 64)
mixer.init()
mixer.music.load("space.ogg")
mixer.music.load("fire.ogg")
fire = mixer.Sound("fire.ogg")
back_sound = mixer.Sound("space.ogg")
back_sound.play()

#win_width = 700
#win_height = 500
win_width = 900
win_height = 700

window = display.set_mode((win_width, win_height))
display.set_caption("Шутер")

#sprite
player_width = 70
player_height = 110
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
background_shop = transform.scale(image.load("shop.png"), (win_width, win_height))
exit_button = transform.scale(image.load("exit.png"), (75, 75))
return_button = transform.scale(image.load("return.png"), (75, 75))

bullet_group = sprite.Group()
enemy_group = sprite.Group()
asteroid_group = sprite.Group()
items_group = sprite.Group()

player = Player(0.5, "rocket.png", win_width / 2 - 35, win_height - 130, player_width, player_height, 5)
automat = Item(0, 10, "automat.png", 70, 99, 110, 42, 0)
bomb = Item(0,15, "bomb.png", 180, 99, 75, 75, 0,)

#skin
tekcor = Item(0, 50, "tekcor.png", 810, 550, player_width, player_height, 0)
player_skin = GameSprite("rocket.png", 645, 114, player_width//2, player_height//2, 0)
rrocket = Item(0, 75, "rrocket.png", 810, 426, player_width + 50, player_height, 0)

door =  Rect(0, win_height-80, 55, 80)

for enemy in range(5):
    enemy = Enemy("ufo.png", randint(0, win_width - 65), -65, 65, 65, randint(1, 3))
    enemy_group.add(enemy)

r_win = False
r_lose = False

shop = True
score = 99
shkip = 0
skiped = font1.render("пропущено:", True, (255, 255, 255), (0, 0, 0))
ybutue = font1.render("получено:", True, (255, 255, 255), (0, 0, 0))
win = font_end.render("победа", True, (255, 255, 255), (255, 255 , 0))
lose = font_end.render("проигрыш", True, (255, 255, 255),(255, 0, 0))

shop_en = t.time()
shop_st = t.time()


complexity = 0
while True:

    display.set_icon(player.image)

    #skiped_score = font1.render(str(shkip), True, (255, 255, 255), (0, 0, 0))
    score_score = font1.render(str(score), True, (255, 255, 255), (0, 0, 0))

    en = t.time()
    

    for e in event.get():
        if e.type == QUIT:
            quit()

    if shop:
        window.blit(background_shop, (0, 0))
        player_skin.reset()
        for item in items_group:
            item.reset()
        #window.blit(skiped, (0, 10))
        #window.blit(skiped_score, (110, 10))
        window.blit(ybutue, (0, 30))
        window.blit(score_score, (94, 30))
        if door.colliderect(player):
            shop = False
            print("!start!")
            complexity += 1
            print("complexity =", complexity)

        bomb.cost = 14 + complexity//2
        player.move()
        player.reset()

        if player.rect.colliderect(automat.rect):
            if automat.purshed < 5 and score >= automat.cost and en - st >= 1:
                score -= automat.cost
                automat.purshed += 1
                automat.mechanics(0, 0.0643)
                st = t.time()
        
        if player.rect.colliderect(bomb.rect):
            if score >= bomb.cost and en - st >= 1:
                score -= bomb.cost
                bomb.purshed += 1
                st = t.time()
        
        if player.rect.colliderect(tekcor.rect):
            if score >= tekcor.cost and en - st >= 1:
                score -= tekcor.cost
                tekcor.purshed += 1

                player.__init__(player.shoot - 0.0643, "tekcor.png", player.rect.x, player.rect.y, player_width, player_height, player.speed)
                st = t.time()

        if player.rect.colliderect(rrocket.rect):
            if score >= rrocket.cost and en - st >= 1:
                score -= rrocket.cost
                rrocket.purshed += 1

                player.__init__(player.shoot - 0.0643, "rrocket.png", player.rect.x, player.rect.y, player_width + 25, player_height, player.speed - 0.5)
                st = t.time()

        if tekcor.purshed > 0 or rrocket.purshed > 0:
            if player.rect.colliderect(player_skin.rect):
                    player.__init__(player.shoot + 0.0643, "rocket.png", player.rect.x, player.rect.y, player_width, player_height, player.speed)
                    tekcor.purshed = 0
                    rrocket.purshed = 0
                    st = t.time()

    elif not shop:
        shop_en = t.time()
        window.blit(background, (0, 0))
        #window.blit(skiped, (0, 10))
        #window.blit(skiped_score, (110, 10))
        window.blit(ybutue, (0, 30))
        window.blit(score_score, (94, 30))
        if randint(1, 300-complexity) == 1:
            asteroid = Asteroid("asteroid.png", randint(0,win_width - player_width), -65, 75, 75, 2, 0)
            asteroid_group.add(asteroid)
            
        #if shkip >=3:
        #    r_lose = True
        #    game = False
        #if score >= 10:
        #    game = False
        #    r_win = Truegame
        if r_lose:
            window.blit(lose, (win_width //2, win_height //2))
            t.sleep(0.5)
            window.blit(exit_button, (815, 15))
            window.blit(return_button, (815 - 75 - 25, 15))
            for e in event.get():
                if e.type == MOUSEBUTTONDOWN:
                    if mouse.get_pos() >= (815, 15) and mouse.get_pos() <= (890, 90):
                        quit()
                    elif mouse.get_pos() >= (815- 75- 25, 15) and mouse.get_pos() <= (890 - 75 - 15, 90):
                        r_lose = False
                        player.__init__(p_shoot, "rocket.png", win_width / 2 - 35, win_height - 130, player_width, player_height, p_speed)
                        rrocket.purshed = 0
                        tekcor.purshed = 0
                        score = 0
                        bomb.purshed = 0
                        complexity = 0
                        shop = True
                        for enemy in enemy_group:
                            enemy_group.remove(enemy)
                        for asteroid in asteroid_group:
                            asteroid_group.remove(asteroid)
        else:
            if shop_en - shop_st >= 75:
                shop = True
                print("--- S H O P ---")
                player.rect.x = win_width / 2
                shop_st = t.time()
                for enemy in enemy_group:
                    enemy_group.remove(enemy)
                
            

            for aster in asteroid_group:
                aster.move()
                if aster.rect.colliderect(player):
                    r_lose = True
                for bullet in bullet_group:
                    if bullet.rect.y <=0:
                        bullet.remove(bullet_group)
                    if bullet.rect.colliderect(aster):
                        aster.touched += 1
                        if aster.touched >= 2:
                            aster.remove(asteroid_group)
                            
                            player.speed +=1
                            score += 1
                        else:
                            bullet.remove(bullet_group)
            if len(enemy_group) <= 5 + complexity:
                enemy = Enemy("ufo.png", randint(0, win_width - 65), -65, 65, 65, randint(1, 3))
                enemy_group.add(enemy)
            for i in enemy_group:
                i.move()
                if i.rect.y >= win_height:
                    enemy_group.remove(i)
                    shkip += 1
                if i.rect.colliderect(player):
                    r_lose = True
            for i in bullet_group:
                i.shooting()
            collide_group = sprite.groupcollide(enemy_group, bullet_group, True, True)
            if len(collide_group)>= 1:
                score += 1
            player.move()
            player.fire()
            #window.blit(player.image, (player.rect.x, player.rect.y))
            window.blit(bomb.image, (815, 15)), window.blit(font1.render(str(bomb.purshed), True, (255, 255, 255), (0, 0, 0)), (845, 40))


        en = t.time()
        shop_st = t.time()

        


    display.update()
    time.Clock().tick(45)
#https://docs.google.com/presentation/d/1Fhr7LklR9gCcMt87PC61cU07UWE8qy9v_PuK5ufGx6s/edit?usp=sharing