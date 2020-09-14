import pygame, sys , random


#creat 2 floor and make a continue move at the bottom
def draw_floor():       
    screen.blit(floor_surface,(floor_x_pos,800))
    screen.blit(floor_surface,(floor_x_pos + 576,800))

def create_pipe():
   random_pipe_pos = random.choice(pipe_height)
   bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
   top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))
   return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
    
def draw_pipes(pipes):
   for pipe in pipes:
      if pipe.bottom >= 824:
         screen.blit(pipe_surface, pipe)
      else:
         flip_pipe = pygame.transform.flip(pipe_surface,False, True)
         screen.blit(flip_pipe, pipe)

def check_collision(pipes):
   for pipe in pipes:
      if bird_rect.colliderect(pipe):
         death_sound.play()
         return False

   if bird_rect.top <= -10 or bird_rect.bottom >= 800:
      return False
   return True

def rotate_bird(bird):
   new_bird = pygame.transform.rotozoom(bird, bird_mov * -3,1)
   return new_bird

def bird_animation():
   new_bird = bird_frames[bird_index]
   new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
   return new_bird, new_bird_rect

def score_display(game_state):
   if game_state == 'main game':
         score_surface = game_font.render(str(int(score)),True,(255,255,255))
         score_rect = score_surface.get_rect(center = (288,100))
         screen.blit(score_surface, score_rect)
         
   if game_state == 'game over':
         score_surface = game_font.render(f'Score:{int(score)}',True,(255,255,255))
         score_rect = score_surface.get_rect(center = (288,100))
         screen.blit(score_surface, score_rect)

         high_score_surface = game_font.render(f'High Score:{int(high_score)}',True,(255,255,255))
         high_score_rect = high_score_surface.get_rect(center = (288,50))
         screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
   if score > high_score:
      high_score = score
   return high_score

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)

pygame.init()
#setup screen size
screen = pygame.display.set_mode((576,824))
#setup FPS
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)

#game variables
gravity = 0.25
bird_mov = 0
game_active = True
score = 0
high_score = 0



#load the background image/image location
bg_surface = pygame.image.load('assets/background-day.png').convert()
#fit the image into the screen size/ can just use the line blow
bg_surface = pygame.transform.scale2x(bg_surface)

#load the floor image/image location
floor_surface = pygame.image.load('assets/base.png').convert()
#fit the image into the screen size/ can just use the line blow
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0  #this set the floor start position

#load the image for bird
bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,414))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)
#bird_surface = pygame.image.load('D://FlipBird/FlappyBird_Python-master/assets/bluebird-midflap.png').convert_alpha()
#bird_surface = pygame.transform.scale2x(bird_surface)
#bird_rect = bird_surface.get_rect(center = (100,414))

#load the image for pipe
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
#1200 is mili-sec/1200ms=1.2s
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [200,250,300,400,450,500,550,600]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,414))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

while True:
    
    #catach every input event
    for event in pygame.event.get():
        #Close the window
        if event.type == pygame.QUIT:       
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
               bird_mov = 0
               bird_mov -= 9
               flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
               game_active = True
               pipe_list.clear()
               bird_rect.center = (100,414)
               bird_mov = 0
               score = 0
               
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        
        if event.type == BIRDFLAP:
           if bird_index < 2:
                 bird_index += 1
           else:
              bird_index = 0
              
           bird_surface,bird_rect = bird_animation()

            
        
    #position the background image
    screen.blit(bg_surface,(0,0))
    if game_active:
          #bird
          #add gravity to bird movment
          bird_mov += gravity
          rotated_bird = rotate_bird(bird_surface)
          #add gravity on Y 
          bird_rect.centery += bird_mov
          screen.blit(rotated_bird,bird_rect)
          game_active = check_collision(pipe_list)
          #pipes
          pipe_list = move_pipes(pipe_list)
          draw_pipes(pipe_list)
          score += 0.01
          score_display('main game')
          score_sound_countdown -= 1
          if score_sound_countdown <= 0:
             score_sound.play()
             score_sound_countdown = 100
    else:
          screen.blit(game_over_surface,game_over_rect)
          high_score = update_score(score,high_score)
          score_display('game over')
          
      
    
    #floor
    floor_x_pos -= 1  #this make the floor moves to left side

    draw_floor()   #call function and reposition the used one to exit one
    if floor_x_pos <= -576:
        floor_x_pos = 0
    
    screen.blit(floor_surface,(floor_x_pos,800))
    
    pygame.display.update()
    #set FPS as 60/120,or more than 30
    clock.tick(60)
