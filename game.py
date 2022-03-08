#import library
from cmath import pi
from venv import create
import pygame, sys, random

#function
def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos+432,650))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos-700))
    return  bottom_pipe,top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe,pipe)  

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            #music.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True

def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
    return new_bird

def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (211, 211, 211))
        score_rect = score_surface.get_rect(center = (432/2,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (211, 211, 211))
        score_rect = score_surface.get_rect(center = (432/2,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (211, 211, 211))
        high_score_rect = high_score_surface.get_rect(center = (432/2,620))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

#variable 
pygame.mixer.pre_init(frequency = 44100, size = -16, channels = 2, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)

    #score
score = 0
high_score = 0

    #background
bg = pygame.image.load('assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)

    #floor
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
   
    #bird
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100,768/2))
    
    #bird enviroment
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap,200)
    
    #physic enviroment
gravity = 0.25
bird_movement = 0
game_active = True
    
    #pipe
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
    
    #spawmpipe 
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe,1200)
pipe_height = [200,300,400]

#game over background
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (432/2,768/2))

#game sound
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
music = pygame.mixer.Sound('sound/music.mp3')
sound_time = 260
score_sound_countdown = sound_time

#main
while True:
    #event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and game_active:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement = -8
                flap_sound.play()
        if event.type == pygame.KEYDOWN and game_active == False:
            game_active = True
            pipe_list.clear()
            bird_rect.center = (100,384)
            bird_movement = 0
            score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()
    #make character
    screen.blit(bg,(0,0))
    if game_active :
        #bird
        rotated_bird = rotate_bird(bird)
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)
        #pipe
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.0039
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = sound_time 
    else:
        screen.blit(game_over_surface, game_over_rect)
        score_display('game over')
        high_score = update_score(score, high_score)
    #floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)