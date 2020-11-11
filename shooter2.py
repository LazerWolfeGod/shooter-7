import pygame,math,random,time
screen = pygame.display.set_mode((700, 700),pygame.RESIZABLE)
pygame.init()
done = False
clock = pygame.time.Clock()
walls_images = [pygame.image.load('wall_1.png').convert(),pygame.image.load('wall_2.png').convert(),pygame.image.load('wall_3.png').convert(),pygame.image.load('wall_4.png').convert(),pygame.image.load('wall_5.png').convert()]
for x in range(len(walls_images)):
    walls_images[x].set_colorkey((255,255,255))
guns_images = pygame.image.load('weapons_images.png').convert()
guns_images.set_colorkey((255,255,255))
rounds = [pygame.image.load('ammo_sign.png').convert()]
for x in range(len(rounds)):
    rounds[x].set_colorkey((255,255,255))
back_ground_image = pygame.image.load('back ground image.png').convert()
coin_image = pygame.image.load('coin.png').convert()
coin_image.set_colorkey((255,255,255))

def text_objects(text, font, col):
    textSurface = font.render(text, True, col)
    return textSurface, textSurface.get_rect()

def write(x,y,text,col,size):
    largeText = pygame.font.SysFont("chiller", size)
    TextSurf, TextRect = text_objects(text, largeText, col)
    TextRect.center = (x,y)
    screen.blit(TextSurf, TextRect)
    
class shot:
    def __init__(self,x,y,damage,aoe,screenx,screeny):
        self.x = x
        self.y = y
        self.aoe = aoe
        self.damage = damage
        s = 10
        self.die = 232
        self.landed = False
        self.lines = []
        for a in range(8):
            self.lines.append([[random.randint(int((self.x-10)/800*screenx),int((self.x+10)/800*screenx)),random.randint(int((self.y-10)/800*screeny),int((self.y+10)/800*screeny))],[random.randint(int((self.x-10)/800*screenx),int((self.x+10)/800*screenx)),random.randint(int((self.y-10)/800*screeny),int((self.y+10)/800*screeny))]])
    def draw(self,screenx,screeny):
        self.die-=1
        if self.die<50:
            if len(self.lines)>0:
                del self.lines[0]
                self.die = 100
            elif self.die<0:
                return True
        for a in self.lines: pygame.draw.line(screen,(100,100,100),a[0],a[1],2)
        pygame.draw.circle(screen,(150,100,20),(self.x/800*screenx,self.y/800*screenx),4)
        return False

class blood:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.xs = random.randint(-5,5)
        self.ys = random.randint(-3,12)
        self.max_height = random.randint(self.y-15,self.y+15)
        self.s = random.randint(1,3)
    def moaw(self,screenx,screeny):
        pygame.draw.circle(screen,(200,0,0),(self.x/800*screenx,self.y/800*screenx),self.s)
        if self.y>self.max_height and self.ys<0:
            if random.randint(0,100) == 69:
                return True
        else:
            self.x-=self.xs
            self.y-=self.ys
            self.xs*=0.8
            self.ys-=1
        return False
        
class enemy:
    def __init__(self,typ,speed,health,distance):
        self.typ = typ
        self.health = health
        self.distance = distance
        self.speed = speed
        self.max_health = health
        self.animation = 0
        self.animation_timer = 0
        self.y = random.randint(320,700)
        self.x = 800
        self.hit = False
        self.wall = False
        self.damage = 0
        if self.typ == 'swords_man': self.images = [pygame.image.load('swords_man_walking_1.png').convert(),pygame.image.load('swords_man_walking_2.png').convert(),pygame.image.load('swords_man_walking_3.png').convert(),pygame.image.load('swords_man_walking_4.png').convert(),pygame.image.load('swords_man_attacking_1.png').convert(),pygame.image.load('swords_man_attacking_2.png').convert(),pygame.image.load('swords_man_attacking_3.png').convert(),pygame.image.load('swords_man_attacking_4.png').convert(),pygame.image.load('swords_man_damage.png').convert()]
        elif self.typ == 'swords_man_armour': self.images = [pygame.image.load('swords_man_armour_walking_1.png').convert(),pygame.image.load('swords_man_armour_walking_2.png').convert(),pygame.image.load('swords_man_armour_walking_3.png').convert(),pygame.image.load('swords_man_armour_walking_4.png').convert(),pygame.image.load('swords_man_armour_attacking_1.png').convert(),pygame.image.load('swords_man_armour_attacking_2.png').convert(),pygame.image.load('swords_man_armour_attacking_3.png').convert(),pygame.image.load('swords_man_armour_attacking_4.png').convert(),pygame.image.load('swords_man_armour_damage.png').convert()]
        elif self.typ == 'pistol_man': self.images = [pygame.image.load('pistol_man_walking_1.png').convert(),pygame.image.load('pistol_man_walking_2.png').convert(),pygame.image.load('pistol_man_walking_3.png').convert(),pygame.image.load('pistol_man_walking_4.png').convert(),pygame.image.load('pistol_man_attacking_1.png').convert(),pygame.image.load('pistol_man_attacking_2.png').convert(),pygame.image.load('pistol_man_attacking_3.png').convert(),pygame.image.load('pistol_man_attacking_4.png').convert(),pygame.image.load('pistol_man_damage.png').convert()]
        elif self.typ == 'tank': self.images = [pygame.image.load('tank_moving_1.png').convert(),pygame.image.load('tank_moving_2.png').convert(),pygame.image.load('tank_moving_3.png').convert(),pygame.image.load('tank_moving_4.png').convert(),pygame.image.load('tank_attacking_1.png').convert(),pygame.image.load('tank_attacking_2.png').convert(),pygame.image.load('tank_attacking_3.png').convert(),pygame.image.load('tank_attacking_4.png').convert(),pygame.image.load('tank_damage.png').convert()]
        for a in self.images:
            a.set_colorkey((255,255,255))
    def move(self,wall,screenx,screeny):
        if self.damage<1:
            if not self.wall:
                self.animation_timer += 1
                if self.animation_timer > self.speed:
                    self.animation+=1
                    self.animation_timer = 0
                    if self.animation > 3:
                        self.animation = 0
                        self.x-=12
                    if self.x-self.animation*3+round(self.animation_timer/self.speed*3)<self.distance and wall != -1 and not self.wall:
                        self.x = self.distance
                        self.wall = True
                        self.animation = 4
                    if self.x<-50:
                        return True
            else:
                self.animation_timer += 1
                if self.animation_timer > 10:
                    self.animation+=1
                    self.animation_timer = 0
                    if self.animation > 6:
                        self.animation = 4
                        self.animation_timer = -10
                        self.hit = True
                        if wall>2:
                            self.health-=5
                            self.damage = 10
                            if self.health<1:
                                self.health = 1
                if wall == -1:
                    self.wall = False
        else:
            self.animation = 3
        return False
    def draw(self,screenx,screeny):
        if self.damage>0:
            screen.blit(self.images[8],(self.x/800*screenx,self.y/800*screeny))
            self.damage-=1
        else:
            if not self.wall:
                screen.blit(self.images[self.animation],(self.x/800*screenx,self.y/800*screeny))
            else:
                screen.blit(self.images[self.animation],(self.x/800*screenx,self.y/800*screeny))
        if self.health != self.max_health:
            health_bar_move = self.animation*3+round(self.animation_timer/self.speed*3)
            if self.wall:
                pygame.draw.rect(screen,(0,0,0),pygame.Rect((self.x+10)/800*screenx,(self.y-15)/800*screeny,25/800*screenx,10/800*screeny))
                pygame.draw.rect(screen,(0,150,0),pygame.Rect((self.x+11)/800*screenx,(self.y-15)/800*screeny+1,self.health/self.max_health*23/800*screenx,8/800*screeny))
            else:
                pygame.draw.rect(screen,(0,0,0),pygame.Rect((self.x-health_bar_move+10)/800*screenx,(self.y-15)/800*screeny,25/800*screenx,10/800*screeny))
                pygame.draw.rect(screen,(0,150,0),pygame.Rect((self.x+1-health_bar_move+10)/800*screenx,(self.y-15)/800*screeny+1,self.health/self.max_health*23/800*screenx,8/800*screeny))
    def shot(self,bullets):
        for a in bullets:
            if a.die>230:
                if pygame.Rect(self.x-a.aoe,self.y-a.aoe,self.images[0].get_width()+a.aoe*2,self.images[0].get_height()+a.aoe*2).collidepoint((a.x,a.y)):
                    self.damage = 10
                    beg_h = self.health
                    self.health-=a.damage
                    end_h = self.health
                    if self.health<1:
                        self.health = 0
                        end_h = self.health
                        return True,beg_h-end_h,bullets.index(a)
                    return False,beg_h-end_h,bullets.index(a)
        return False,0,0
                
class Gun:
    def __init__(self,gun_typ,mag_size,rel_sped,aim_zoom,aim_normal,aim_back,sites_size,damage,aoe,automatic,kick_back,round_price,bullets,num,gun_info,gun_upgrades):
        self.gun_info = gun_info
        self.num = num
        self.rel_sped = rel_sped
        self.rel_timer = -10
        self.mag = mag_size+gun_upgrades[num][2][1]*gun_upgrades[num][2][0]
        self.set_gun(gun_typ,mag_size,rel_sped,aim_zoom,aim_normal,aim_back,sites_size,damage,aoe,automatic,kick_back,round_price,bullets,num,gun_upgrades)
        self.rel_timer = -10
        self.automatic_delay = 5
        self.curser_pos = [400,400]
        self.curser_slide = [0,0]
        self.curser_kickback_slide = [0,0]
    def set_gun(self,gun_typ,mag_size,rel_sped,aim_zoom,aim_normal,aim_back,sites_size,damage,aoe,automatic,kick_back,round_price,bullets,num,gun_upgrades):
        temp_rel = self.rel_timer*1.2
        if temp_rel>self.rel_sped: temp_rel = self.rel_sped
        self.gun_typ = gun_typ
        self.round_price = round_price
        self.mag_size = mag_size+gun_upgrades[num][2][1]*gun_upgrades[num][2][0]
        self.bullets = bullets
        self.rel_sped = rel_sped-gun_upgrades[num][1][1]*gun_upgrades[num][1][0]
        self.aim_zoom = aim_zoom-gun_upgrades[num][3][1]*gun_upgrades[num][3][0]
        self.aim_normal = aim_normal
        self.aim_back = aim_back
        self.sites_size = sites_size
        self.damage = damage+gun_upgrades[num][0][1]*gun_upgrades[num][0][0]
        self.aoe = aoe
        self.automatic = automatic
        self.kick_back = kick_back
        self.gun_info[self.num][0] = self.mag
        self.gun_info[self.num][1] = temp_rel
        if self.gun_info[num][0]>0:
            self.rel_timer = -10
        else:
            self.rel_timer = self.gun_info[num][1]
        self.num = num
        self.mag = self.gun_info[self.num][0]
        self.zoom = False
        self.shoot_zone = 100
        self.cs = 1200
        self.shoot_press = True
        
        
    def curser_move(self):
        if pygame.mouse.get_pressed()[2]:
            self.zoom = True
            if self.cs>self.sites_size:
                self.cs*=0.8
                if self.cs<self.sites_size:
                    self.cs = self.sites_size
        else:
            self.zoom = False
            if self.cs<1200:
                self.cs*=1.2
                if self.cs>1200:
                    self.cs = 1200
    def curser_draw(self,screenx,screeny):
        pygame.mouse.set_visible(False)
        backing = (20,20,20)
        self.curser_move()
        if self.cs<1000:
            detail = 100
            dots = [[-10,-10],[-10,screeny+10],[screenx+10,screeny+10],[screenx+10,-10],[-10,-10]]
            for a in range(detail+1):
                dots.append([(self.curser_pos[0]-round(math.sin((360/detail*a*math.pi)/180)*self.cs))/800*screenx,(self.curser_pos[1]-round(math.cos((360/detail*a*math.pi)/180)*self.cs))/800*screeny])
            pygame.draw.polygon(screen,backing,dots)
            pygame.draw.line(screen,backing,((self.curser_pos[0]-self.cs)/800*screenx,self.curser_pos[1]/800*screeny),((self.curser_pos[0]-self.cs*0.8)/800*screenx,self.curser_pos[1]/800*screeny),5)
            pygame.draw.line(screen,backing,((self.curser_pos[0])/800*screenx,(self.curser_pos[1]-self.cs)/800*screeny),((self.curser_pos[0])/800*screenx,(self.curser_pos[1]-self.cs*0.8)/800*screeny),5)
            pygame.draw.line(screen,backing,((self.curser_pos[0]+self.cs)/800*screenx,self.curser_pos[1]/800*screeny),((self.curser_pos[0]+self.cs*0.8)/800*screenx,self.curser_pos[1]/800*screeny),5)
            pygame.draw.line(screen,backing,((self.curser_pos[0])/800*screenx,(self.curser_pos[1]+self.cs)/800*screeny),((self.curser_pos[0])/800*screenx,(self.curser_pos[1]+self.cs*0.8)/800*screeny),5)
        pygame.draw.line(screen,backing,(self.curser_pos[0]/800*screenx,(self.curser_pos[1]-10)/800*screeny),(self.curser_pos[0]/800*screenx,(self.curser_pos[1]+10)/800*screeny),3)
        pygame.draw.line(screen,backing,((self.curser_pos[0]-10)/800*screenx,self.curser_pos[1]/800*screeny),((self.curser_pos[0]+10)/800*screenx,self.curser_pos[1]/800*screeny),3)
        dots = []
        if self.rel_timer>0:
            semi_circle = 100-int(self.rel_timer/self.rel_sped*100)
        else:
            semi_circle = 101
        circle_width = 3
        for a in range(semi_circle):
            dots.append([(self.curser_pos[0]-round(math.sin((360/100*a*math.pi)/180)*self.shoot_zone))/800*screenx,(self.curser_pos[1]-round(math.cos((360/100*a*math.pi)/180)*self.shoot_zone))/800*screeny])
        for b in range(semi_circle,0,-1):
            dots.append([(self.curser_pos[0]-round(math.sin((360/100*(b)*math.pi)/180)*(self.shoot_zone+circle_width)))/800*screenx,(self.curser_pos[1]-round(math.cos((360/100*(b)*math.pi)/180)*(self.shoot_zone+circle_width)))/800*screeny])
        if len(dots)>2:
            pygame.draw.polygon(screen,backing,dots)
        distance = int(300/self.mag_size)
        if distance>25: distance = 25
        for a in range(self.mag_size):
            if a<self.mag:
                screen.blit(rounds[0],((a*distance+5)/800*screenx,5))
        screen.blit(guns_images,(350/800*screenx,5),(0,self.num*60,204,60))
    def curser_stuf(self,shoot_holes,game_info,screenx,screeny):
        if self.automatic:
            self.automatic_delay -=1
            if self.automatic_delay < 1:
                self.shoot_press = False
        self.rel_timer-=1
        if self.rel_timer == 0:
            self.mag = self.mag_size
        if pygame.mouse.get_pressed()[0] and not self.shoot_press and self.rel_timer<0:
            shoot_holes,game_info = self.shoot(shoot_holes,game_info,screenx,screeny)
            self.shoot_press = True
            self.automatic_delay = 5
            game_info[1]+=self.bullets
        elif not pygame.mouse.get_pressed()[0] and not self.automatic:
            self.shoot_press = False
        if self.shoot_zone>self.aim_zoom and self.zoom:self.shoot_zone-=self.aim_back
        elif self.shoot_zone>self.aim_normal and not self.zoom:self.shoot_zone-=self.aim_back
        elif not self.zoom: self.shoot_zone = self.aim_normal
        old_pos = pygame.mouse.get_pos()
        pygame.mouse.set_pos(400,400)
        for a in range(2): self.curser_slide[a]*=0.8
        for a in range(2): self.curser_kickback_slide[a]*=0.8
        self.curser_slide[0]+=old_pos[0]-400+(random.randint(-10,10)/100)
        self.curser_slide[1]+=old_pos[1]-400+(random.randint(-10,10)/100)
        if self.zoom: sped = 4
        else: sped = 2
        self.curser_pos[0]+=self.curser_slide[0]/sped
        self.curser_pos[1]+=self.curser_slide[1]/sped
        self.curser_pos[0]+=self.curser_kickback_slide[0]
        self.curser_pos[1]+=self.curser_kickback_slide[1]
        
        if self.curser_pos[0]>790: self.curser_pos[0] = 790
        elif self.curser_pos[0]<10: self.curser_pos[0] = 10
        if self.curser_pos[1]>700: self.curser_pos[1] = 700
        elif self.curser_pos[1]<300: self.curser_pos[1] = 300
        
        if self.curser_slide[0]<-10: self.curser_slide[0] = -10
        elif self.curser_slide[0]>10: self.curser_slide[0] = 10
        if self.curser_slide[1]<-10: self.curser_slide[1] = -10
        elif self.curser_slide[1]>10: self.curser_slide[1] = 10
        
        self.curser_draw(screenx,screeny)
        return shoot_holes,game_info

    def shoot(self,shoot_holes,game_info,screenx,screeny):
        for a in range(self.bullets):
            game_info[3]+=self.round_price
            shoot_holes.append(shot(round(self.curser_pos[0])+random.randint(int(-self.shoot_zone),int(self.shoot_zone)),round(self.curser_pos[1])+random.randint(int(-self.shoot_zone),int(self.shoot_zone)),self.damage,self.aoe,screenx,screeny))
        self.shoot_zone+=self.kick_back
        self.curser_kickback_slide[0]+=random.randint(int(-self.kick_back/10),int(self.kick_back/10))
        self.curser_kickback_slide[1]+=random.randint(-self.kick_back,int(-self.kick_back*0.7))
        self.mag-=1
        if self.mag<1:
            self.rel_timer = self.rel_sped
        return shoot_holes,game_info

def rock_gen(h,t,screenx,screeny):
    detail = 80
    blocks = [[screenx+10,h-t],[screenx+10,h],[-10,h],[-10,h-t]]
    for a in range(screenx//10):
        blocks.append([int(800/detail*a),random.randint(int(h-t),int(h-20))])
    return blocks

def main(gun,shoot_holes,g_rock_map,b_rock_map,t_rock_map,enemies,bloods,wall,wall_health,level,game_info,screenx,screeny):
    win = False
    done = False
    if level[5] == 0 and level[6] == 0 and level[7] == 0 and level[8] == 0 and len(enemies) == 0: win = True
    if random.randint(0,level[0]) == 0:
        create = False
        enemy_info = [['swords_man',random.randint(9,11),random.randint(17,20),32],['swords_man_armour',random.randint(12,15),random.randint(50,60),32],['pistol_man',random.randint(7,9),random.randint(25,35),random.randint(180,220)],['tank',random.randint(20,24),random.randint(900,1000),random.randint(300,400)]]
        if not win:
            while not create and not (level[5] == 0 and level[6] == 0 and level[7] == 0 and level[8] == 0 and len(enemies)):
                weight = random.randint(0,100)
                for a in range(4):
                    if weight<level[a+1]:
                        if level[a+5]>0:
                            enemies.append(enemy(enemy_info[a][0],enemy_info[a][1],enemy_info[a][2],enemy_info[a][3]))
                            create = True
                            level[a+5]-=1
                        break
    pygame.draw.polygon(screen,(100,100,100),t_rock_map)
    pygame.draw.polygon(screen,(50,150,10),g_rock_map)
    pygame.draw.rect(screen,(50,150,10),pygame.Rect(0,300/800*screeny,800/800*screenx,500/800*screeny))
    bul_kill = []
    for a in shoot_holes:
        if a.draw(screenx,screeny):
            bul_kill.append(a)
    for a in bul_kill:
        shoot_holes.remove(a)
    kill = []
    for a in bloods:
        if a.moaw(screenx,screeny):
            kill.append(a)
    for a in kill:
        bloods.remove(a)
    kill = []
    done = False
    for a in enemies:
        if a.move(wall,screenx,screeny):
            done = True
        if a.hit:
            a.hit = False
            wall_health-=1
        a.draw(screenx,screeny)
        death,damage,hit_by = a.shot(shoot_holes)
        game_info[0]+=damage
        if damage>0 and not shoot_holes[hit_by].landed:
            game_info[2]+=1
            shoot_holes[hit_by].landed = True
        if death:
            for b in range(random.randint(8,20)):
                bloods.append(blood((a.x+5),a.y+10))
            kill.append(a)
    for a in kill:
        enemies.remove(a)
    if wall+1!=0:
        screen.blit(walls_images[wall],(5/800*screenx,275))
    pygame.draw.polygon(screen,(100,100,100),b_rock_map)
    shoot_holes,game_info = gun.curser_stuf(shoot_holes,game_info,screenx,screeny)
    if wall_health>0 and wall != -1:
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(10/800*screenx,50/800*screeny,304/800*screenx,34/800*screeny))
        pygame.draw.rect(screen,(0,150,0),pygame.Rect(12/800*screenx,52/800*screeny,wall_health/((wall+1)*100)*300/800*screenx,30/800*screeny))
    return shoot_holes,g_rock_map,b_rock_map,t_rock_map,enemies,bloods,wall_health,done,level,win,game_info

def button(rectt,txt,mpos,mprs,col):
    if rectt.collidepoint(mpos):
        pygame.draw.rect(screen,(50,50,50),rectt)
        if mprs[0]:
            if not col: write(rectt.centerx,rectt.centery,txt,(0,250,0),45)
            else: write(rectt.centerx,rectt.centery,txt,(250,50,50),45)
            pygame.draw.rect(screen,(130,130,130),rectt,4)
            return True
    else:
        pygame.draw.rect(screen,(30,30,30),rectt)
    if not col: write(rectt.centerx,rectt.centery,txt,(0,180,0),45)
    else: write(rectt.centerx,rectt.centery,txt,(180,50,50),45)
    pygame.draw.rect(screen,(100,100,100),rectt,4)
    return False

def ug_button(rectt,txt,mpos,mprs,price,coins):
    if rectt.collidepoint(mpos):
        pygame.draw.rect(screen,(50,50,50),rectt)
        if mprs[0] and coins>=price:
            write(rectt.centerx,int(rectt.centery-rectt.height/4),txt,(0,180,0),45)
            if price == 10000000: write(rectt.centerx,int(rectt.centery+rectt.height/4),'MAXED',(0,180,0),45)
            else: write(rectt.centerx,int(rectt.centery+rectt.height/4),'Cost:'+str(price),(0,180,0),45)
            pygame.draw.rect(screen,(130,130,130),rectt,4)
            return True
    else:
        pygame.draw.rect(screen,(30,30,30),rectt)
    write(rectt.centerx,int(rectt.centery-rectt.height/4),txt,(0,180,0),45)
    if price == 10000000: write(rectt.centerx,int(rectt.centery+rectt.height/4),'MAXED',(0,180,0),45)
    else:  write(rectt.centerx,int(rectt.centery+rectt.height/4),'Cost:'+str(price),(0,180,0),45)
    pygame.draw.rect(screen,(100,100,100),rectt,4)
    return False
    
def pause(mpos,mprs,screenx,screeny):
    pygame.mouse.set_visible(True)
    pygame.draw.rect(screen,(10,10,10),pygame.Rect(180/800*screenx,220/800*screeny,440/800*screenx,360/800*screeny))
    pygame.draw.rect(screen,(100,100,100),pygame.Rect(180/800*screenx,220/800*screeny,440/800*screenx,360/800*screeny),5)
    write(400/800*screenx,270/800*screeny,'Shooter',(255,255,255),80)
    if button(pygame.Rect(280/800*screenx,320/800*screeny,240/800*screenx,60/800*screeny),'Return To Game',mpos,mprs,False): return 0
    if button(pygame.Rect(280/800*screenx,400/800*screeny,240/800*screenx,60/800*screeny),'Exit Game',mpos,mprs,False): return -1
    if button(pygame.Rect(280/800*screenx,480/800*screeny,240/800*screenx,60/800*screeny),'Main Menu',mpos,mprs,False): return 2
    return -10

def game(possible_gun,guns,levels,wall,upgrade_prices,gun_upgrades,misc_upgrade_prices):
    screen = pygame.display.set_mode((800, 800),pygame.RESIZABLE)
    game = 2
    coins = 0
    screenx = 800
    screeny = 800
    main_menu_mode = 0
    main_menu_mode_prev = 0
    esc_press = False
    button_press = False
    t_rock_map = rock_gen(300/800*screenx,80,screenx,screeny)
    b_rock_map = rock_gen(800/800*screenx,80,screenx,screeny)
    g_rock_map = rock_gen(300/800*screenx,30,screenx,screeny)
    pygame.mouse.set_pos([400/800*screenx,400])
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.VIDEORESIZE:
                screenx = event.w
                screeny = event.h
                screen = pygame.display.set_mode((event.w,event.h),pygame.RESIZABLE)
                t_rock_map = rock_gen(300/800*screeny,80,screenx,screeny)
                b_rock_map = rock_gen(800/800*screeny,80,screenx,screeny)
                g_rock_map = rock_gen(300/800*screeny,30,screenx,screeny)
            elif event.type == pygame.MOUSEBUTTONDOWN and game == 0:
                if len(possible_gun)>1:
                    new = False
                    if event.button == 4:
                        gun_num-=1
                        if gun_num == -1: gun_num = len(possible_gun)-1
                        new = True
                    if event.button == 5:
                        gun_num+=1
                        if gun_num == len(possible_gun): gun_num = 0
                        new = True
                    if new: gun.set_gun(guns[possible_gun[gun_num]][0],guns[possible_gun[gun_num]][1],guns[possible_gun[gun_num]][2],guns[possible_gun[gun_num]][3],guns[possible_gun[gun_num]][4],guns[possible_gun[gun_num]][5],guns[possible_gun[gun_num]][6],guns[possible_gun[gun_num]][7],guns[possible_gun[gun_num]][8],guns[possible_gun[gun_num]][9],guns[possible_gun[gun_num]][10],guns[possible_gun[gun_num]][11],guns[possible_gun[gun_num]][12],possible_gun[gun_num],gun_upgrades)


        kprs = pygame.key.get_pressed()
        if kprs[pygame.K_ESCAPE] and not esc_press:
            if game == 0:
                game = 1
                esc_press = True
            elif game == 1:
                game = 0
                esc_press = True
        elif not kprs[pygame.K_ESCAPE]:
            esc_press = False
          
        mpos = pygame.mouse.get_pos()
        mprs = pygame.mouse.get_pressed()
        if game == 0:
            
            if wall_health<0:
                wall = -1
            screen.fill((0,0,255))
            shoot_holes,g_rock_map,b_rock_map,t_rock_map,enemies,bloods,wall_health,don,level,win,game_info = main(gun,shoot_holes,g_rock_map,b_rock_map,t_rock_map,enemies,bloods,wall,wall_health,level,game_info,screenx,screeny)
            if don:
                won = False
                game = 3
            elif win == True:
                won = True
                game = 3
        elif game == 1:
            gam = pause(mpos,mprs,screenx,screeny)
            if gam != -10:
                game = gam
        elif game == 2:
            screen.blit(pygame.transform.scale(back_ground_image,(screenx,screeny)),(0,0))
            if main_menu_mode == 0:
                pygame.draw.polygon(screen,(10,10,10),[(300/800*screenx,180/800*screeny),(330/800*screenx,210/800*screeny),(470/800*screenx,210/800*screeny),(500/800*screenx,180/800*screeny),(470/800*screenx,150/800*screeny),(330/800*screenx,150/800*screeny)])
                pygame.draw.polygon(screen,(100,100,100),[(300/800*screenx,180/800*screeny),(330/800*screenx,210/800*screeny),(470/800*screenx,210/800*screeny),(500/800*screenx,180/800*screeny),(470/800*screenx,150/800*screeny),(330/800*screenx,150/800*screeny)],5)
                write(400/800*screenx,182/800*screeny,'SHOOTER',(255,255,255),50)
                if button(pygame.Rect(200/800*screenx,260/800*screeny,400/800*screenx,60/800*screeny),'Levels',mpos,mprs,False) and not button_press: main_menu_mode_prev,main_menu_mode = main_menu_mode,1
                elif button(pygame.Rect(200/800*screenx,360/800*screeny,400/800*screenx,60/800*screeny),'Weapons',mpos,mprs,False) and not button_press: main_menu_mode_prev,main_menu_mode = main_menu_mode,2
                elif button(pygame.Rect(200/800*screenx,460/800*screeny,400/800*screenx,60/800*screeny),'Upgrades',mpos,mprs,False) and not button_press: main_menu_mode_prev,main_menu_mode = main_menu_mode,3
            elif main_menu_mode == 1:
                write(400/800*screenx,100,'LEVELS',(255,255,255),50)
                for a in range(len(levels)):
                    if button(pygame.Rect(200/800*screenx,((180+a*(600//len(levels))))/800*screeny,400/800*screenx,60/800*screeny),'LEVEL '+str(a+1),mpos,mprs,False) and not button_press:
                        game,lev = 0,a
                if game == 0:
                    possible_gun.sort()
                    shoot_holes = []
                    enemies = []
                    bloods = []
                    won = False
                    gun_num = 0
                    wall_health = (wall+1)*100
                    timee = time.time()
                    level = levels[lev].copy()
                    game_info = [0,0,0,0]
                    gun_info = [[guns[a][1],guns[a][2]] for a in range(len(guns))]
                    gun = Gun(guns[gun_num][0],guns[gun_num][1],guns[gun_num][2],guns[gun_num][3],guns[gun_num][4],guns[gun_num][5],guns[gun_num][6],guns[gun_num][7],guns[gun_num][8],guns[gun_num][9],guns[gun_num][10],guns[possible_gun[gun_num]][11],guns[possible_gun[gun_num]][12],gun_num,gun_info,gun_upgrades)
            elif main_menu_mode == 2:
                write(400/800*screenx,100,'WEAPONS',(255,255,255),50)
                truths = []
                for a in range(0,7):
                    if a in possible_guns: truths.append(False)
                    else: truths.append(True)
                if button(pygame.Rect(200/800*screenx,180/800*screeny,400/800*screenx,60/800*screeny),'PISTOL',mpos,mprs,truths[0]) and not button_press: main_menu_mode_prev,main_menu_mode = main_menu_mode,4
                elif button(pygame.Rect(200/800*screenx,250/800*screeny,400/800*screenx,60/800*screeny),'SMG',mpos,mprs,truths[1]) and not button_press: main_menu_mode_prev,main_menu_mode = main_menu_mode,5
                elif button(pygame.Rect(200/800*screenx,320/800*screeny,400/800*screenx,60/800*screeny),'SHOTGUN',mpos,mprs,truths[2]) and not button_press: main_menu_mode_prev,main_menu_mode = main_menu_mode,6
                elif button(pygame.Rect(200/800*screenx,390/800*screeny,400/800*screenx,60/800*screeny),'LMG',mpos,mprs,truths[3]) and not button_press: main_menu_mode_prev,main_menu_mode = main_menu_mode,7
                elif button(pygame.Rect(200/800*screenx,460/800*screeny,400/800*screenx,60/800*screeny),'SNIPER',mpos,mprs,truths[4]) and not button_press: main_menu_mode_prev,main_menu_mode = main_menu_mode,8
                elif button(pygame.Rect(200/800*screenx,530/800*screeny,400/800*screenx,60/800*screeny),'RPG',mpos,mprs,truths[5]) and not button_press: main_menu_mode_prev,main_menu_mode = main_menu_mode,9
                elif button(pygame.Rect(200/800*screenx,600/800*screeny,400/800*screenx,60/800*screeny),'NUKE',mpos,mprs,truths[6]) and not button_press: main_menu_mode_prev,main_menu_mode = main_menu_mode,10
            elif main_menu_mode == 3:
                write(400/800*screenx,100,'UPGRADES',(255,255,255),50)
                if ug_button(pygame.Rect(200/800*screenx,370/800*screeny,400/800*screenx,100/800*screeny),'UPGRADE WALL',mpos,mprs,misc_upgrade_prices[0][wall+1],coins) and not button_press and wall<4:
                        wall+=1
                        coins-=misc_upgrade_prices[0][wall]
            elif main_menu_mode>3:
                write(300/800*screenx,100,str(guns[main_menu_mode-4][0]),(255,255,255),100)
                screen.blit(guns_images,(500/800*screenx,75/800*screeny),(0,(main_menu_mode-4)*60,204,60))
                if not main_menu_mode-4 in possible_gun:
                    if ug_button(pygame.Rect(200/800*screenx,370/800*screeny,400/800*screenx,100/800*screeny),'PURCHACE WEAPON',mpos,mprs,upgrade_prices[main_menu_mode-4][0],coins) and not button_press:
                        possible_gun.append(main_menu_mode-4)
                        coins-=upgrade_prices[main_menu_mode-4][0]
                else:
                    upgrade_types = ['DAMAGE','RELOAD SPEED','MAG SIZE','ZOOM']
                    for a in range(4):
                        if ug_button(pygame.Rect(200/800*screenx,(170+a*120)/800*screeny,400/800*screenx,100/800*screeny),upgrade_types[a],mpos,mprs,upgrade_prices[main_menu_mode-4][a+1][gun_upgrades[main_menu_mode-4][a][1]],coins) and not button_press and gun_upgrades[main_menu_mode-4][a][1]<len(upgrade_prices[main_menu_mode-4][a+1])-1:
                            coins-=upgrade_prices[main_menu_mode-4][a+1][gun_upgrades[main_menu_mode-4][a][1]]
                            gun_upgrades[main_menu_mode-4][a][1]+=1
            screen.blit(coin_image,(600/800*screenx,10/800*screeny))
            write(720/800*screenx,30/800*screeny,str(coins),(255,255,255),40)
        elif game == 3:
            pygame.mouse.set_visible(True)
            finished_timer = time.time()
            zoom_end_increase = 1
            game = 4
            game_info.append((wall+1)*100-wall_health)
            word_zooming = [0,0,0,0,0]
        elif game == 4:
            screen.blit(back_ground_image,(0,0))
            if won:
                write(400,80,'Level Complete!',(255,255,255),100)
                pygame.draw.rect(screen,(40,40,40),pygame.Rect(100/800*screenx,150/800*screeny,280/800*screenx,360/800*screeny))
                pygame.draw.rect(screen,(100,100,100),pygame.Rect(100/800*screenx,150/800*screeny,280/800*screenx,360/800*screeny),5)
                pygame.draw.rect(screen,(100,100,100),pygame.Rect(100/800*screenx,240/800*screeny,280/800*screenx,90/800*screeny),5)
                pygame.draw.line(screen,(100,100,100),(100/800*screenx,420/800*screeny),(380/800*screenx,420/800*screeny),5)
                pygame.draw.rect(screen,(40,40,40),pygame.Rect(100/800*screenx,560/800*screeny,280/800*screenx,90/800*screeny))
                pygame.draw.rect(screen,(100,100,100),pygame.Rect(100/800*screenx,560/800*screeny,280/800*screenx,90/800*screeny),5)
                write(240/800*screenx,195/800*screeny,'Damage',(255,255,255),60)
                write(240/800*screenx,285/800*screeny,'Accuracy',(255,255,255),60)
                write(240/800*screenx,375/800*screeny,'Ammo Costs',(255,255,255),60)
                write(240/800*screenx,465/800*screeny,'Wall Repair',(255,255,255),60)
                write(240/800*screenx,605/800*screeny,'Total',(255,255,255),60)
                
                if time.time()-finished_timer>1:
                    if word_zooming[0]<60: word_zooming[0]+=1
                    write(540/800*screenx,195/800*screeny,str(game_info[0]),(255,255,255),word_zooming[0])
                if time.time()-finished_timer>2:
                    if word_zooming[1]<60: word_zooming[1]+=1
                    write(540/800*screenx,285/800*screeny,str(int(game_info[2]/game_info[1]*100))+'%',(255,255,255),word_zooming[1])
                if time.time()-finished_timer>3:
                    if word_zooming[2]<60: word_zooming[2]+=1
                    write(540/800*screenx,375/800*screeny,str(game_info[3]),(255,255,255),word_zooming[2])
                if time.time()-finished_timer>4:
                    if word_zooming[3]<60: word_zooming[3]+=1
                    write(540/800*screenx,465/800*screeny,str(game_info[4]),(255,255,255),word_zooming[3])
                total = int(game_info[0]*(game_info[2]/game_info[1]*10))-game_info[3]-(game_info[4]*5)
                if total<0: total = 0
                if time.time()-finished_timer>5:
                    if word_zooming[4]<60: word_zooming[4]+=1
                    write(540/800*screenx,605/800*screeny,str(total),(255,255,255),word_zooming[4])
                if time.time()-finished_timer>6:
                    if button(pygame.Rect(300/800*screenx,700/800*screeny,200/800*screenx,80),'Continue',mpos,mprs,False) and not button_press:
                        game = 2
                        coins+=total
            else:
                write(400/800*screenx,350/800*screeny,'Level Failed!',(250,0,0),200)
                if time.time()-finished_timer>2:
                    if button(pygame.Rect(300/800*screenx,500/800*screeny,200/800*screenx,80/800*screeny),'Continue',mpos,mprs,False) and not button_press:
                        game = 2
        elif game == -1:
            done = True
        if game>1:
            if button(pygame.Rect(660/800*screenx,720/800*screeny,100/800*screenx,60/800*screeny),'QUIT',mpos,mprs,False) and not button_press:
                done = True
                won = False
        if game == 2 and main_menu_mode != 0:
            if button(pygame.Rect(40/800*screenx,720/800*screeny,100/800*screenx,60/800*screeny),'BACK',mpos,mprs,False) and not button_press:
                game = 2
                main_menu_mode = main_menu_mode_prev
                main_menu_mode_prev = 0
                
        if mprs[0]:button_press = True
        else:button_press = False
        
        pygame.display.flip()
        clock.tick(60)
        
#gun_typ,mag_size,rel_sped,aim_zoom,aim_normal,aim_back,sites_size,damage,aoe,automatic,kick_back,round_price,bullets        
guns = [['Pistol',10,200,10,20,1.4,100,10,1,False,20,3,1],
        ['SMG',20,300,14,25,1,150,8,1,True,8,1,1],
        ['Shot Gun',6,600,25,50,2,180,50,1,False,40,10,5],
        ['LMG',40,400,8,20,1.2,130,10,1,True,9,2,1],
        ['Sniper',3,400,7,12,0.6,80,500,1,False,60,20,1],
        ['RPG',1,500,15,40,0.8,120,300,80,False,80,100,1],
        ['NUKE',1,5000,30,60,0.2,140,1000000,3000,False,50,1000,1]]

#total spawn rate, 4 enemy spawn rates,4 enemy limit
levels = [[150,100,100,100,100,10,0,0,0],
          [125,85,100,100,100,17,3,0,0],
          [100,60,100,100,100,30,20,0,0],
          [80,70,90,100,100,50,25,10,0],
          [300,0,0,0,100,0,0,0,10],
          [10,10,50,90,100,20,80,100,10]]

misc_upgrade_prices = [[10000,25000,50000,100000,250000,10000000],
                       [1,2,3,4,5]]

#buy weapon, damage, reload speed, magazine size, zoom magnification
upgrade_prices = [[0,[100,250,500,1000,2000,10000000],[500,1000,1500,2000,2500,3000,10000000],[500,1000,2000,3000,4000,10000000],[200,400,600,800,1000,10000000]],
                  [2000,[500,1000,2000,5000,10000,10000000],[2000,4000,7000,11000,15000,10000000],[800,2000,4000,7000,10000,10000000],[100,250,500,1000,2000,10000000]],
                  [5000,[1000,2000,3000,4000,5000,10000000],[4000,7000,10000,14000,20000,10000000],[5000,8000,12000,16000,20000,10000000],[500,1000,2000,3000,5000,10000000]],
                  [20000,[8000,12000,16000,20000,25000,10000000],[5000,9000,14000,18000,25000,10000000],[10000,13000,16000,19000,22000,10000000],[4000,8000,12000,16000,20000,10000000]],
                  [30000,[10000,12000,15000,20000,30000,10000000],[6000,12000,18000,25000,35000,10000000],[20000,30000,50000,10000000],[5000,10000,15000,20000,10000000]],
                  [40000,[20000,25000,30000,40000,50000,10000000],[15000,20000,28000,35000,48000,10000000],[40000,60000,10000000],[10000,20000,30000,10000000]],
                  [100000,[10000000],[50000,75000,100000,250000,500000,10000000],[10000000],[5000,10000,15000,20000,10000000]]]


#game data
gun_upgrades = [[[1,0],[20,0],[1,0],[1,0]],
                [[1,0],[25,0],[4,0],[1,0]],
                [[4,0],[35,0],[1,0],[2,0]],
                [[2,0],[30,0],[6,0],[1,0]],
                [[15,0],[30,0],[1,0],[1,0]],
                [[30,0],[40,0],[1,0],[3,0]],
                [[100,0],[100,0],[1,0],[2,0]]]

possible_guns = [0]

wall = -1

game(possible_guns,guns,levels,wall,upgrade_prices,gun_upgrades,misc_upgrade_prices)
pygame.quit()
