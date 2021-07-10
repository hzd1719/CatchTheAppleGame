import pygame, random, time
from pygame.locals import *
from time import sleep
import sys

HEIGHT = 800
WIDTH = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (126,200,80)
FPS = 60
APPLEMINSIZE = 40
APPLEMAXSIZE = 60
APPLEMINSPEED = 4
APPLEMAXSPEED = 8
ADDNEWAPPLERATE = 20
PLAYERMOVERATE = 5

def terminate():
    pygame.quit()
    sys.exit()

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def player_has_picked_apple(player_rect, apples):
    for a in apples:
        if player_rect.colliderect(a["rect"]):
            apples.remove(a)
            return True
    return False

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_p or event.key == K_SPACE:
                    return
                    #break
                #return 
def prep_timer(surface):
       
        current_time = round(t_end - time.time())
        if(current_time < 0):
            current_time = 10
      

        current_time_str = "Time: {:,}".format(current_time)
        time_image = font.render(current_time_str, True, TEXTCOLOR, BACKGROUNDCOLOR)

        time_rect = time_image.get_rect()
        time_rect.left = WIDTH - 150
        time_rect.top = 20
        surface.blit(time_image, time_rect)
# Set up pygame
pygame.init()
main_clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pick the apple")
pygame.mouse.set_visible(False)

# Set up font
font = pygame.font.SysFont(None, 48)

# Set up sounds
game_over_sound = pygame.mixer.Sound("gameover.wav")
pick_up_sound = pygame.mixer.Sound("pickup.wav")
bad_pick_up_sound = pygame.mixer.Sound("badpickup.wav")
pygame.mixer.music.load("background.mid")

# Set up images
basket_image = pygame.image.load("basket.bmp")
basket_rect = basket_image.get_rect()
apple_image = pygame.image.load("apple6.png")
burger_image = pygame.image.load("burger2.png")

# Displaying the start screen
window.fill(BACKGROUNDCOLOR)
drawText("Pick the apples", font, window, (WIDTH / 3) - 20, (HEIGHT / 3))
drawText("Press p or Space key to start.", font, window, (WIDTH / 3) - 120, (HEIGHT / 3) + 180)
pygame.display.update()
waitForPlayerToPressKey()

top_score = 0

while True:

    # Set up the start of the game
    apples = []
    score = 0
    basket_rect.topleft = (WIDTH / 2, HEIGHT - 60)
    move_left = move_right = False
    apple_add_counter = 0
    pygame.mixer.music.play(-1, 0.0)
    t_end = time.time() + 30           #Duration of the game
 
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    mover_ight = False
                    move_left = True
                if event.key == K_RIGHT or event.key == K_d:
                    move_left = False
                    move_right = True
                

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == K_a:
                    move_left = False
                if event.key == K_RIGHT or event.key == K_d:
                    move_right = False

        apple_add_counter += 1

        if apple_add_counter == ADDNEWAPPLERATE:
            apple_add_counter = 0
            apple_size = random.randint(APPLEMINSIZE, APPLEMAXSIZE)
            r = random.randint(0, 1)
            if r == 1:
                image = apple_image
            else:
                image = burger_image
            new_apple = {'rect': pygame.Rect(random.randint(0, WIDTH - apple_size), 0 - apple_size,apple_size, apple_size),
                        'speed': random.randint(APPLEMINSPEED, APPLEMAXSPEED),
                        'surface':pygame.transform.scale(image,(apple_size, apple_size)),
                        'image': image,
                        'size': apple_size}
            apples.append(new_apple)
        
        # Move the player around.
        if move_left and basket_rect.left > 0:
            basket_rect.move_ip(-1 * PLAYERMOVERATE, 0)
        if move_right and basket_rect.right < WIDTH:
            basket_rect.move_ip(PLAYERMOVERATE, 0)
        
        
        # Move the apples down.
        for a in apples:
            m = random.randint(-1, 1)          #Remove this ako se trese mnogo
            a['rect'].move_ip(m, a['speed'])
        
        for a in apples[:]:
            if a['rect'].top > HEIGHT:
                apples.remove(a)
        

        # Draw the game world on the window.
        window.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, window, 10, 0)
        drawText('Top Score: %s' % (top_score), font, window,
                10, 40)

        # Draw the player's rectangle.
        window.blit(basket_image, basket_rect)

        # Draw each apple.
        for a in apples:
            window.blit(a['surface'], a['rect'])

        # Draw the timer
        prep_timer(window)
        
        pygame.display.update()

        # Check if any of the apples have hit the basket.
        # Delete apples that have fallen past the bottom.
        for a in apples:
            if basket_rect.colliderect(a["rect"]):
                if a['image'] == apple_image:
                    pick_up_sound.play()
                    score += 10 * int(a['size']/10)
                else:
                    bad_pick_up_sound.play()
                    score -= 10 * int(a['size']/10)
                apples.remove(a)
        #pick_up_sound.stop()
        main_clock.tick(FPS)
        if time.time() >= t_end:
            break
            
    
    if score > top_score:
        top_score = score
    pygame.mixer.music.stop()
    game_over_sound.play()
    
    sleep(0.5)
    window.fill(BACKGROUNDCOLOR)
    drawText('Score: %s' % (score), font, window, 10, 0)
    drawText('Top Score: %s' % (top_score), font, window,
            10, 40)
    drawText("Pick the apples", font, window, (WIDTH / 3) - 20, (HEIGHT / 3))
    drawText("Press p or Space key to start.", font, window, (WIDTH / 3) - 120, (HEIGHT / 3) + 180)
    pygame.display.update()
    waitForPlayerToPressKey()


    game_over_sound.stop()