#coding=utf-8
import pygame,sys
from pygame .locals import *
import time

#结束游戏
def terminate():
    pygame.quit()
    sys.exit()
    
#定义一个棋盘
class Chessboard:

    def __init__(table):
        #初始棋盘数值
        table.grid_size = 36
        table.start_x, table.start_y = 20, 20
        table.edge_size = table.grid_size / 2
        table.grid_count = 15
        table.piece = 'b'
        table.winner = None
        table.game_over = False	
        table.grid = []
        for i in range(table.grid_count):
            table.grid.append(list("." * table.grid_count))

    def handle_key_event(table, e):
        #棋子的位置设定
        origin_x = table.start_x - table.edge_size
        origin_y = table.start_y - table.edge_size
        size = (table.grid_count - 1) * table.grid_size + table.edge_size * 2
        pos = e.pos
        if origin_x <= pos[0] <= origin_x + size and origin_y <= pos[1] <= origin_y + size:
            if not table.game_over:
                x = pos[0] - origin_x
                y = pos[1] - origin_y
                r = int(y // table.grid_size)
                c = int(x // table.grid_size)
                if table.set_piece(r, c):
                    table.check_win(r, c)

#黑白棋手交换

    def set_piece(table, r, c):
        if table.grid[r][c] == '.':
            table.grid[r][c] = table.piece

            if table.piece == 'b':
                table.piece = 'w'
            else:
                table.piece = 'b'

            return True
        return False

#判断输赢

    def check_win(table, r, c):
        n_count = table.get_continuous_count(r, c, -1, 0) 
        s_count = table.get_continuous_count(r, c, 1, 0)

        e_count = table.get_continuous_count(r, c, 0, 1)
        w_count = table.get_continuous_count(r, c, 0, -1)

        se_count = table.get_continuous_count(r, c, 1, 1)
        nw_count = table.get_continuous_count(r, c, -1, -1)

        ne_count = table.get_continuous_count(r, c, -1, 1)
        sw_count = table.get_continuous_count(r, c, 1, -1)

        if (n_count + s_count + 1 >= 5) or (e_count + w_count + 1 >= 5) or \
                (se_count + nw_count + 1 >= 5) or (ne_count + sw_count + 1 >= 5):
            table.winner = table.grid[r][c]
            table.game_over = True

    def get_continuous_count(table, r, c, dr, dc):
        piece = table.grid[r][c]
        result = 0
        i = 1
        while True:
            new_r = r + dr * i
            new_c = c + dc * i
            if 0 <= new_r < table.grid_count and 0 <= new_c < table.grid_count:
                if table.grid[new_r][new_c] == piece:
                    result += 1
                else:
                    break
            else:
                break
            i += 1
        return result


#画出棋盘和

    def draw(table, screen):
        # 棋盘底色
        pygame.draw.rect(screen, (185, 122, 87),
                         [table.start_x - table.edge_size, table.start_y - table.edge_size,
                          (table.grid_count - 1) * table.grid_size + table.edge_size * 2,
                          (table.grid_count - 1) * table.grid_size + table.edge_size * 2], 0)

        for r in range(table.grid_count):
            y = table.start_y + r * table.grid_size
            pygame.draw.line(screen, (0, 0, 0), [table.start_x, y],
                             [table.start_x + table.grid_size * (table.grid_count - 1), y], 2)

        for c in range(table.grid_count):
            x = table.start_x + c * table.grid_size
            pygame.draw.line(screen, (0, 0, 0), [x, table.start_y],
                             [x, table.start_y + table.grid_size * (table.grid_count - 1)], 2)

        for r in range(table.grid_count):
            for c in range(table.grid_count):
                piece = table.grid[r][c]
                if piece != '.':
                    if piece == 'b':
                        color = (0, 0, 0)
                    else:
                        color = (255, 255, 255)

                    x = table.start_x + c * table.grid_size
                    y = table.start_y + r * table.grid_size
                    pygame.draw.circle(screen, color, [x, y], table.grid_size // 2)

#定义一个按钮类
class Button(object):
    def __init__(self, upimage, downimage,position):
        self.imageUp = pygame.image.load(upimage).convert_alpha()
        self.imageDown = pygame.image.load(downimage).convert_alpha()
        self.position = position
        self.game_start = False
        
    def isOver(self):
        point_x,point_y = pygame.mouse.get_pos()
        x, y = self. position
        w, h = self.imageUp.get_size()

        in_x = x - w/2 < point_x < x + w/2
        in_y = y - h/2 < point_y < y + h/2
        return in_x and in_y

    def render(self):
        w, h = self.imageUp.get_size()
        x, y = self.position
        
        if self.isOver():
            a.blit(self.imageDown, (x-w/2,y-h/2))
        else:
            a.blit(self.imageUp, (x-w/2, y-h/2))
    def is_start(self):
        if self.isOver():
            b1,b2,b3 = pygame.mouse.get_pressed()
            if b1 == 1:
                self.game_start = True

#定义一个初始音频和控制音乐的类的方法
def audio_init():
    global bg_au,bg_a
    pygame.mixer.init()
    bg_au = pygame.mixer.Sound("background.ogg")
    bg_a=pygame.mixer.Sound("akira.wav")
class Music():
    def __init__(self,sound):
        self.channel = None
        self.sound = sound     
    def play_sound(self):
        self.channel = pygame.mixer.find_channel(True)
        self.channel.set_volume(0.5)
        self.channel.play(self.sound)
    def play_pause(self):
        self.channel.set_volume(0.0)
        self.channel.play(self.sound)
        
#展现棋盘和下棋及输赢输出
class Go():

    def __init__(table):
        pygame.init()

        table.screen = pygame.display.set_mode((550, 550))
        pygame.display.set_caption("五子棋")
        table.clock = pygame.time.Clock()
        table.font = pygame.font.Font(r"C:\Windows\Fonts\consola.ttf", 48)
        table.font.set_bold(True)
        table.going = True
        table.chessboard = Chessboard()

    def loop(table):
        while table.going:
            table.update()
            table.draw()
            table.clock.tick(60)

        pygame.quit()

    def update(table):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                table.going = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                table.chessboard.handle_key_event(e)

    def draw(table):
        table.screen.fill((255, 255, 255))


        table.chessboard.draw(table.screen)
        if table.chessboard.game_over:
            table.screen.blit(table.font.render("{0} Win".
                    format("Black" if table.chessboard.winner =='b' else "White"),
                                        True,(255, 0, 0)), (150,240))
            table.screen.blit(table.font.render("press Esc out",
                                                True,(255,0,0)),(90,270))
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    terminate()
                if event.type ==QUIT:
                    terminate()
                if event.type ==KEYDOWN:
                    if event.key ==K_ESCAPE:
                        terminate()
        pygame.display.update()
        
#主函数
pygame.init()
audio_init()
a=pygame.display.set_mode((600,600),0,32)
pygame.display.set_caption('五子棋入门版')
pygame.display.set_icon(pygame.image.load('hh.jpg'))
upImageFilename = 'game_start_up.png'
downImageFilename = 'game_start_down.png'
q='game_over_up.png'
w='game_over_down.png'
h='state_up.png'
l='state_down.png'
#调整颜色
Black=(0,0,0)
White=(255,255,255)
brown=(200,125,0)
#创建按钮对象
button = Button(upImageFilename,downImageFilename,(300,350))
button1= Button(q,w,(300,450))
button2= Button(h,l,(300,400))
interface=pygame.image.load('qipan.jpg')
#使用系统字体
fontObj3 = pygame.font.SysFont('宋体', 45)
fontObj4 = pygame.font.SysFont('宋体', 20)
fontObj3.set_bold(True)
fontObj4.set_bold(True)
text = fontObj3.render(u'开心五子棋', True,Black)
d= fontObj4.render(u'Version 1.0',True,Black)
d1=d.get_rect()
d1.center=(530,10)
text1 = text.get_rect()
text1.center = (300, 200)
#定义变量
bg_sound=Music(bg_au)
my_sound=Music(bg_a)
bg_sound.play_sound()
index =1
#主循环
while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type==KEYDOWN:
            if event.key==K_a:
                bg_sound.play_sound()
            if event.key==K_b:
                bg_sound.play_pause()
            if event.key==K_c:
                my_sound.play_sound()
            if event.key==K_d:
                my_sound.play_pause()
    a.blit(interface,(0,0))
    a.blit(text, text1)
    a.blit(d,d1)
    button.render()
    button1.render()
    button2.render()
    button.is_start()
    button1.is_start()
    button2.is_start()
    
    #按钮判断，点击退出
    if button1.game_start ==True:
        pygame.quit()
        sys.exit()
    #按钮判断，点击开始双人游戏
    if button.game_start ==True:
        if index == 1:
            while True:
                game=Go()
                game.loop()
    #按钮判断，点击观看背景音乐说明
    if button2.game_start ==True:
        shuoming= fontObj4.render(u"按a开启背景音乐\n按b关闭背景音乐",True,Black)
        shuoming2= fontObj4.render(u"按c开启另一种音乐\n按d关闭该音乐",True,Black)
        dist=shuoming.get_rect()
        dist.center=(300,250)
        dist1=shuoming2.get_rect()
        dist1.center=(300,270)
        a.blit(shuoming,dist)
        a.blit(shuoming2,dist1)
    pygame.display.update()        
