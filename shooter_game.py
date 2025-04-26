from pygame import *
import random
from time import time as timer
 
#создай окно 
window = display.set_mode((700,500))
display.set_caption('shooter')

#шрифты
font.init()
font = font.Font(None, 70)
l_text = font.render('LOOSE', True, (255, 0, 0))
win_text = font.render('WIN', True, (0, 255, 0))
reload_text = font.render('Reloading...', True, (255, 0, 0))


#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
   #конструктор класса
   def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
       super().__init__()
       # каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()


num_bul = 0
relod = False
reload_start = 0

class Player(GameSprite):
    def update(self):
        global num_bul
        global relod
        global reload_start
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x < 700 - 65:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_SPACE]:
            if num_bul < 10 and relod == False:
                num_bul += 1
                self.fire()

            if num_bul >= 10 and relod == False:
                relod = True
                reload_start = timer()
        

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)





lost = 0 
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 440:
            lost += 1
            self.rect.x = random.randint(90, 610)
            self.rect.y = 30

class Boss(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y, hp):
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
    def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 440:
            self.rect.x = random.randint(90, 610)
            self.rect.y = 30


            





        






mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)


background = transform.scale(image.load("galaxy.jpg"), (700,500))
player = Player("rocket.png",10,410,10, 60, 90)
monsters = sprite.Group()
for i in range(1,7):
    monster = Enemy("ufo.png",random.randint(90,610),30, random.randint(1,3), 90, 60)
    monsters.add(monster)
bullets = sprite.Group()
asteroid = Boss('asteroid.png',random.randint(90,610),30,1,90,60,10)






clock = time.Clock()
FPS = 30


finish = True
max_lost = 10
score = 0
game = True
while game:
    if finish:

        window.blit(background,(0,0))
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroid.reset()

        player.update()
        monsters.update()
        bullets.update()
        asteroid.update()
        collides = sprite.groupcollide(monsters, bullets, True, True)
        if relod == True:
            reload_how = timer()
            if reload_how - reload_start < 3:
                window.blit(reload_text,(10,160))
            else:
                num_bul = 0
                relod = False

            
        for c in collides:
            score += 1
            monster = Enemy("ufo.png",random.randint(90,610),30, random.randint(1,9), 90, 60)
            monsters.add(monster)
        
        if sprite.spritecollide(player, monsters, False) or lost >= max_lost:
            finish = False
            window.blit(l_text,(350,250))
        if score >= 10:
            finish = False
            window.blit(win_text,(350,250))
        
        




    text = font.render('счёт:'+ str(score), 1, (255,255,255))
    window.blit(text,(10,20))
    text_lose = font.render('Пропущено:'+ str(lost), 1, (255,255,255))
    window.blit(text_lose,(10,90))


  



    


 


    for e in event.get():
        if e.type == QUIT:
            game = False

        
    clock.tick(FPS)
    display.update()

