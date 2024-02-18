#Import and initialize necessary libraries
import pygame 
import os
pygame.font.init()
pygame.mixer.init()
pygame.init()

width,height=(1100,600)
Win=pygame.display.set_mode((width,height))
pygame.display.set_caption("First Game")

#Defining Colors
white=(255,255,255)
Black=(0,0,0)
Red=(255,0,0)
Blue=(0,0,255)

#Fonts and sounds
Border=pygame.Rect((width//2)-5,0,10,height)
Health_font=pygame.font.SysFont('cosmicsans',40)
Winner_font=pygame.font.SysFont('italic',100)
welcome_font=pygame.font.SysFont('Bauhaus',63)
music=pygame.mixer.music.load('space_music.mp3')
bullet_sound = pygame.mixer.Sound('blaster.mp3')  
boom_sound = pygame.mixer.Sound('explosion.mp3')  

#User events
Yellow_hit=pygame.USEREVENT+1
Red_hit=pygame.USEREVENT+2

FPS=60
clock=pygame.time.Clock()
vel=5
bul_vel=7
max_bullets=3
spaceship_width=95
spaceship_height=60

#Load images
yellow_spaceship_img=pygame.image.load('spaceship1.jpg')
red_spaceship_img=pygame.image.load('spaceship2.jpg')
welcome_img=pygame.image.load('welcome.jpg')
space=pygame.image.load('galaxy.jpg')


#scaled image:-
scaled_yellow=pygame.transform.scale(yellow_spaceship_img,(spaceship_width,spaceship_height))
scaled_red=pygame.transform.scale(red_spaceship_img,(spaceship_width,spaceship_height))
scaled_welcome=pygame.transform.scale(welcome_img,(width,height))
space_transform=pygame.transform.scale(space,(width,height))

#rotate image:-
rotate_yellow=pygame.transform.rotate(scaled_yellow,270)
rotate_red=pygame.transform.rotate(scaled_red,90)

#Controlling movement of yellow spaceship
def yellow_handle_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x - vel > 0:
        yellow.x-=vel
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width + vel < Border.x:
        yellow.x+=vel
    if keys_pressed[pygame.K_w] and yellow.y - vel > 0:
        yellow.y-=vel
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height + vel < height-36:
        yellow.y+=vel

#Controlling movement of red spaceship
def red_handle_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x - vel > (Border.width + Border.height) -27:
        red.x-=vel
    if keys_pressed[pygame.K_RIGHT] and red.x+red.width+vel < width+33:
        red.x+=vel
    if keys_pressed[pygame.K_UP] and red.y - vel >0:
        red.y-=vel
    if keys_pressed[pygame.K_DOWN]and red.y +red.height + vel< height-36:
        red.y+=vel


#Display bullets and health on screen
def draw_window(red,yellow,yellow_bullets,red_bullets,yellow_health,red_health):
    Win.blit(space_transform,(0,0))
    pygame.draw.rect(Win,Black,Border)

    red_health_text=Health_font.render(" Red's Health: " + str(red_health),1,white,Black)
    yellow_health_text=Health_font.render(" Blue's Health: " + str(yellow_health),1,white,Black)
    Win.blit(red_health_text,(width-red_health_text.get_width()-10,10))
    Win.blit(yellow_health_text,(10,10))

    Win.blit(rotate_yellow,(yellow.x,yellow.y))
    Win.blit(rotate_red,(red.x,red.y))

    for bullets in yellow_bullets:
        pygame.draw.rect(Win,Blue,bullets)
    for bullets in red_bullets:
        pygame.draw.rect(Win,Red,bullets)

    pygame.display.update()

#Handle movements of bullets
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += bul_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(Red_hit))
            yellow_bullets.remove(bullet)
        elif bullet.x > width:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= bul_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(Yellow_hit))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

#Winners info.
def draw_winner(text):
    draw_text = Winner_font.render(text, 1, white,90)
    Win.blit(draw_text, (width/2 - draw_text.get_width() /
                         2, height/2 - draw_text.get_height()/2))
    pygame.display.update()
    boom_sound.play()
    pygame.time.delay(7000)

#screen text
def text_screen(text,color,x,y,background):
    screen_text=welcome_font.render(text,True,color,background)
    Win.blit(screen_text,[x,y])

#Welcome Page
def welcome():
    pygame.mixer.music.play(-1)
    exit_game=False
    while not exit_game:
        Win.blit(scaled_welcome,(0,0))
        text_screen("Welcome to Duel Spaceship Battle ", white, 252, 250,Black)
        text_screen("Press Space Bar To Play", white, 315, 350,Black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # pygame.mixer.music.load('better-day-186374.mp3')
                    # pygame.mixer.music.play()
                    pygame.mixer.music.stop()
                    main()
        pygame.display.update()
        clock.tick(60)

#Main Function
def main():
    red=pygame.Rect(900,310,spaceship_width,spaceship_height)
    yellow=pygame.Rect(100,300,spaceship_width,spaceship_height)
    
    red_bullets=[]
    yellow_bullets=[]
    red_health,yellow_health=10,10
    clock=pygame.time.Clock()
    game_end = False
    # Load in-game background music
    in_game_music = pygame.mixer.Sound('space_music.mp3')
    in_game_music.set_volume(0.04)  # Adjust the volume as needed
    # Play the in-game music with lower volume
    in_game_music.play()

    run=True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run=False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < max_bullets:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    bullet_sound.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < max_bullets:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    bullet_sound.play()

            if event.type==Red_hit:
                red_health-=1
            if event.type==Yellow_hit:
                yellow_health-=1
        winner_text=""
        if red_health<=0:
            winner_text="Blue Wins!"
        if yellow_health<=0:
            winner_text="Red Wins!"
        if winner_text!="":
            draw_winner(winner_text)
            break
        keys_pressed=pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)
        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        draw_window(red,yellow,yellow_bullets,red_bullets,yellow_health,red_health)        
    # After the game loop exits due to a win
    
    pygame.mixer.music.stop()  # Stop the main music
    in_game_music.play()
    pygame.quit()
welcome()
main()