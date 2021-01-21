from os import environ as env
from os import name as os_name
from os import system as cmd_run
from os import access as file_exists
from os import F_OK as file_exists_param
from time import sleep as time_sleep
from random import randint as random_int
env['PYGAME_HIDE_SUPPORT_PROMPT']='True'
env['__COMPAT_LAYER']='WinXPSp3'
if os_name=='nt':
    from ctypes import windll as windows_dll
    windows_dll.kernel32.SetConsoleTitleW('Pixelsuft Snake')
    cmd_run('color 0a')
import pygame


width=800
height=600
fps=60
grid=40
music=False
max_speed=20
default_fps=1


def set_music(vared):
    global music
    music=vared
def set_size(w, h):
    global width
    global height
    width=w
    height=h
def set_speed(vared):
    global default_fps
    default_fps=vared
def set_max_speed(vared):
    global max_speed
    max_speed=vared
def set_grid(vared):
    global grid
    grid=vared


def load_config(cfg):
    for i in cfg.split('\n'):
        if not i=='':
            eval(str(i))


if file_exists('config.txt', file_exists_param):
    temp_f=open('config.txt', 'r')
    txt_cfg=temp_f.read()
    temp_f.close()
    load_config(txt_cfg)


grid_width=int(width/grid)
grid_height=int(height/grid)
pygame.init()
pygame.mixer.init()
menu_color_back=False
menu_color_count=50
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pixelsuft Snake')
pygame.display.set_icon(pygame.image.load('favicon.ico').convert())
if music==True:
    pygame.mixer.music.load('menu.wav')
    pygame.mixer.music.play()
running=True
typer='menu'
menu_font = pygame.font.SysFont('Segoe Script', 26, bold=True)
score_font = pygame.font.SysFont('Segoe Script', 15, bold=True)
game_over_font = pygame.font.SysFont('Segoe Script', 40, bold=True)
snake=[[5, 2], [4, 2], [3, 2]]
apple=[random_int(0, grid_width-3), random_int(0, grid_height-3)]
score=0
snake_vector='right'
clock = pygame.time.Clock()
speed_gameover=0


def game_over():
    global typer
    global fps
    global speed_gameover
    speed_gameover=fps
    typer='game_over'
    fps=60
    if music==True:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('fail'+str(random_int(1,3))+'.wav')
        pygame.mixer.music.play()


def main_loop():
    global typer
    global score
    global snake
    global snake_vector
    global apple
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]==1:
            global running
            running = False
    pygame.draw.rect(screen, pygame.Color('#000000'), (0, 0, width, height))
    if typer=='menu':
        global menu_color_back
        global menu_color_count
        if menu_color_back==False:
            if menu_color_count<0:
                menu_color_count=50
                menu_color_back=True
            else:
                pygame.draw.rect(screen, pygame.Color('#000000'), ((width/2)-(286/2)-15, (height/2)-(25/2)-15, 400, 80))
                render_menu_text = menu_font.render('Press Space to Start...', 1, pygame.Color('#00ff00'))
                screen.blit(render_menu_text, ((width/2)-(286/2), (height/2)-(25/2)))
                menu_color_count-=1
        else:
            if menu_color_count<0:
                menu_color_count=50
                menu_color_back=False
            else:
                pygame.draw.rect(screen, pygame.Color('#00ff00'), ((width/2)-(286/2)+3, (height/2)-(25/2)+5, 286, 30))
                render_menu_text = menu_font.render('Press Space to Start...', 1, pygame.Color('#000000'))
                screen.blit(render_menu_text, ((width/2)-(286/2), (height/2)-(25/2)))
                menu_color_count-=1
        if keys[pygame.K_SPACE]:
            global fps
            fps=default_fps
            if music==True:
                pygame.mixer.music.stop()
            typer='game'
    elif typer=='game_over':
        render_menu_text1 = game_over_font.render('Game Over :(', 1, pygame.Color('#00ff00'))
        render_menu_text2 = game_over_font.render('Score: '+str(score)+'.', 1, pygame.Color('#00ff00'))
        render_menu_text3 = game_over_font.render('Speed: '+str(speed_gameover)+'.', 1, pygame.Color('#00ff00'))
        render_menu_text4 = game_over_font.render('R - Restart, ESC - Exit', 1, pygame.Color('#00ff00'))
        screen.blit(render_menu_text1, (20, 20))
        screen.blit(render_menu_text2, (20, 80))
        screen.blit(render_menu_text3, (20, 140))
        screen.blit(render_menu_text4, (20, 200))
        if keys[pygame.K_r]:
            fps=default_fps
            if music==True:
                pygame.mixer.music.stop()
            snake=[[5, 2], [4, 2], [3, 2]]
            apple=[random_int(0, grid_width-3), random_int(0, grid_height-3)]
            score=0
            snake_vector='right'
            typer='game'       
    elif typer=='game':
        no_delete=False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if not snake_vector=='right' and not snake_vector=='left':
                snake_vector='right'
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if not snake_vector=='right' and not snake_vector=='left':
                snake_vector='left'
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            if not snake_vector=='up' and not snake_vector=='down':
                snake_vector='up'
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if not snake_vector=='up' and not snake_vector=='down':
                snake_vector='down'
        for i in range(len(snake)):
            j=len(snake)-1
            if not j==0:
                snake[j][0]=snake[j-1][0]
                snake[j][1]=snake[j-1][1]
        
        if snake[0][0]==apple[0] and snake[0][1]==apple[1]:
            no_delete=True
            score+=1
            apple=[random_int(1,grid_width-3),random_int(2,grid_height-3)]
            if fps<=max_speed:
                fps+=random_int(0,2)
        
        if snake_vector=='left':
            if snake[0][0]>0:
                if no_delete==False:
                    snake.remove(snake[len(snake)-1])
                snake.insert(0, [snake[0][0]-1,snake[0][1]])
            else:
                game_over()
        elif snake_vector=='right':
            if snake[0][0]<grid_width:
                if no_delete==False:
                    snake.remove(snake[len(snake)-1])
                snake.insert(0, [snake[0][0]+1,snake[0][1]])     
            else:
                game_over()      
        elif snake_vector=='up':
            if snake[0][1]>0:
                if no_delete==False:
                    snake.remove(snake[len(snake)-1])
                snake.insert(0, [snake[0][0],snake[0][1]-1])    
            else:
                game_over()  
        elif snake_vector=='down':
            if snake[0][1]<grid_height:
                if no_delete==False:
                    snake.remove(snake[len(snake)-1])
                snake.insert(0, [snake[0][0],snake[0][1]+1])
            else:
                game_over()
        for i in range(len(snake)):
            if int(snake[0][0])==int(snake[i][0]) and int(snake[0][1]==snake[i][1]) and not i==0:
                game_over()
        pygame.draw.rect(screen, pygame.Color('#ff0000'), (apple[0]*grid, apple[1]*grid, grid, grid))
        
        for i in range(len(snake)):
            if i==0:
                pygame.draw.rect(screen, pygame.Color('#ff0000'), (snake[i][0]*grid, snake[i][1]*grid, grid, grid))
            else:
                pygame.draw.rect(screen, pygame.Color('#00ff00'), (snake[i][0]*grid, snake[i][1]*grid, grid, grid))
        render_score_text = score_font.render('Score: ' + str(score), 1, pygame.Color('#00ff00'))
        screen.blit(render_score_text, (5, 5))
    pygame.display.flip()

while running==True:
    main_loop()
    #time_sleep(1/fps)
    clock.tick(fps)