# This script creates simple 2D python game as a means of learning the pygame module.

import pygame # Imports a game library that lets you use specific functions in your program.
import random # Import to generate random numbers. 
import os # Import operating system to handle path directories
pygame.font.init()

# Initialize the pygame modules to get everything started.

pygame.init() 

# The screen that will be created needs a width and a height.

screen_width = 900
screen_height = 500
screen = pygame.display.set_mode((screen_width,screen_height)) # This creates the screen and gives it the width and height specified as a 2 item sequence.

# Define constant variables that are used throughout the game

white = (255, 255, 255) # Creates variable for colour white.
yellow = (255, 255, 0) # Creates variable for colour yellow.
bullets = [] # Create a list for bullets.
bullet_velocity = 7 # The speed at which the bullet moves across the screen.
max_bullets = 3 # The maximum number of bullets the player can have on the screen at any given time.
enemies_hit = 0 # Initialise score
enemies_hit_font = pygame.font.SysFont("comfortaa", 30)
result_font = pygame.font.SysFont("comfortaa", 100)

# This creates the player and enemies and gives it the image found in the Assets folder.

player_image = pygame.image.load(os.path.join('Assets', 'spaceship_red.png')) # Load player image
player = pygame.transform.scale(player_image, (125, 80)) # Resize image to fit screen
player = pygame.transform.rotate(player,(90)) # Rotate player

enemy_1_image = pygame.image.load(os.path.join('Assets', 'enemy_1.png')) # Load enemy_1 image
enemy_1 = pygame.transform.scale(enemy_1_image, (120, 90)) # Resize enemy

enemy_2_image = pygame.image.load(os.path.join('Assets', 'enemy_2.png')) # Load enemy_2 image
enemy_2 = pygame.transform.scale(enemy_2_image, (95,60)) # Resize enemy

enemy_3_image = pygame.image.load(os.path.join('Assets', 'enemy_3.png')) # Load enemy_3 image
enemy_3 = pygame.transform.scale(enemy_3_image, (130, 70)) # Resize enemy

prize_image = pygame.image.load(os.path.join('Assets', 'prize.png')) # Load prize image
prize = pygame.transform.scale(prize_image, (100,130)) # Resize enemy

# The sound files below have been replaced and converted to .wav files as the mp3 files previously used appeared to be corrupted.
# Having tested, the sound files are working correctly. 

bullet_fire_sound = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.wav')) # Load shooting sound
bullet_hit_sound = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.wav')) # Load target hit sound

# Load background image and scale it to fit the screen
space_image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (screen_width, screen_height)) 

# Get the width and height of the images in order to do boundary detection (i.e. make sure the image stays within screen boundaries or know when the image is off the screen).

player_height = player.get_height() # Player height
player_width = player.get_width() # Player width

enemy_1_height = enemy_1.get_height() # Enemy 1 height
enemy_1_width = enemy_1.get_width() # Enemy 1 width

enemy_2_height = enemy_2.get_height() # Enemy 2 height
enemy_2_width = enemy_2.get_width() # Enemy 2 width

enemy_3_height = enemy_3.get_height() # Enemy 3 height
enemy_3_width = enemy_2.get_width() # Enemy 3 width

# Store the positions of the player and enemy as variables so that you can change them later. 

playerXPosition = 100
playerYPosition = screen_height/3

# Make the enemies start off screen and at a random y position.

enemy_1_XPosition =  screen_width
enemy_1_YPosition =  random.randint(0, screen_height - 100)

enemy_2_XPosition =  screen_width
enemy_2_YPosition =  random.randint(0, screen_height - 100)

enemy_3_XPosition =  screen_width
enemy_3_YPosition =  random.randint(0, screen_height - 100)

# Make the prize start off the screen
prizeXPosition = screen_width
prizeYPosition = random.randint(0, screen_height - 400)

# This checks if the up, down, left or right keys are pressed.

keyUp= False
keyDown = False
keyLeft = False
keyRight = False

# This is the game loop.
# In games you will need to run the game logic over and over again.
# You need to refresh/update the screen window and apply changes to 
# represent real time game play. 

FPS = 60 # Sets frames per second to 60 to ensure that the game runs consistently on all machines.
clock = pygame.time.Clock() 
run = True
while run: # This is a looping structure that will loop the indented code until you tell it to stop(in the event where you exit the program by quitting). In Python the int 1 has the boolean value of 'true'. In fact numbers greater than 0 also do. 0 on the other hand has a boolean value of false. You can test this out with the bool(...) function to see what boolean value types have. You will learn more about while loop structers later. 

    clock.tick(FPS) # run the loop 60 times per second. Most machines are capable of this, and the game renders well at this frame rate. 
    #screen.fill(space_image) # Clears the screen and sets background colour to white
    screen.blit(space_image, (0,0))
    score_text = enemies_hit_font.render("Enemies hit: " + str(enemies_hit), 1, white)
    screen.blit(score_text, (10, 10))
    screen.blit(player, (playerXPosition, playerYPosition))# This draws the player image to the screen at the postion specfied. I.e. (100, 50).
    screen.blit(enemy_1, (enemy_1_XPosition, enemy_1_YPosition))
    screen.blit(enemy_2, (enemy_2_XPosition, enemy_2_YPosition))
    screen.blit(enemy_3, (enemy_3_XPosition, enemy_3_YPosition))
    screen.blit(prize, (prizeXPosition, prizeYPosition))
    for bullet in bullets:
        pygame.draw.rect(screen, yellow, bullet)
    
    pygame.display.flip()# This updates the screen. 

    for event in pygame.event.get():

        # This event checks if the user quits the program, then if so it exits the program. 
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        # This event checks if the user presses a key down.
        if event.type == pygame.KEYDOWN:
        
            # Test if the key pressed is the one we want.
            if event.key == pygame.K_UP or event.key == pygame.K_w: # Test for up arrow or w key
                keyUp = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s: # Test for down arrow or s key
                keyDown = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a: # Test for left arrow or a key
                    keyLeft = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d: # Test for right arrow or d key
                keyRight = True
            # Game logic to handle creation and shooting of bullets
            if event.key == pygame.K_SPACE and len(bullets) < max_bullets:
                bullet = pygame.Rect(playerXPosition, playerYPosition + player_height // 2, 10, 5)
                bullets.append(bullet)
                bullet_fire_sound.play()
        
        # This event checks if the key is up(i.e. not pressed by the user).
        if event.type == pygame.KEYUP:
        
            # Test if the key released is the one we want.
            if event.key == pygame.K_UP or event.key == pygame.K_w: # Test for up arrow or w key
                keyUp = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s: # Test for down arrow or s key
                keyDown = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a: # Test for left arrow or a key
                    keyLeft = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d: # Test for right arrow or d key
                keyRight = False
            
    # After events are checked for in the for loop above and values are set,
    # check key pressed values and move player accordingly.
    
    # The coordinate system of the game window(screen) is that the top left corner is (0, 0).
    # This means that if you want the player to move down you will have to increase the y position. 
    
    if keyUp == True:
        if playerYPosition > 0 : # This makes sure that the user does not move the player above the window.
            playerYPosition -= 4
    if keyDown == True:
        if playerYPosition < screen_height - player_height:# This makes sure that the user does not move the player below the window.
            playerYPosition += 4
    if keyLeft == True:
        if playerXPosition > 0: # This makes sure that the user does not move the player left of the window.
            playerXPosition -= 4
    if keyRight == True:
        if playerXPosition < screen_width - player_width: # This makes sure that the user does not move the player right of the window.
            playerXPosition += 4

    # Check for collision of the enemy with the player.
    # To do this we need bounding boxes around the images of the player and enemy.
    # We the need to test if these boxes intersect. If they do then there is a collision.
    
    # Bounding box for the player:
    
    playerBox = pygame.Rect(player.get_rect())
    
    # The following updates the playerBox position to the player's position,
    # in effect making the box stay around the player image. 
    
    playerBox.top = playerYPosition
    playerBox.left = playerXPosition
    
    # Bounding box for the enemy:
    
    enemy_1_box = pygame.Rect(enemy_1.get_rect())
    enemy_1_box.top = enemy_1_YPosition
    enemy_1_box.left = enemy_1_XPosition

    enemy_2_box = pygame.Rect(enemy_2.get_rect())
    enemy_2_box.top = enemy_2_YPosition
    enemy_2_box.left = enemy_2_XPosition

    enemy_3_box = pygame.Rect(enemy_3.get_rect())
    enemy_3_box.top = enemy_3_YPosition
    enemy_3_box.left = enemy_3_XPosition

    prize_box = pygame.Rect(enemy_1.get_rect())
    prize_box.top = prizeYPosition
    prize_box.left = prizeXPosition
    
    # Test collision of the boxes:
    
    if ((playerBox.colliderect(enemy_1_box)) or (playerBox.colliderect(enemy_2_box)) or (playerBox.colliderect(enemy_3_box))):
    
        # Display losing status to the user: 
        
        lose_text = result_font.render("You lose!", 1, white)
        screen.blit(lose_text, (screen_width//2 - lose_text.get_width()//2, screen_height//2 - lose_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000) # Pause the game for 5 seconds to display results before quitting
       
        # Quit game and exit window: 
        
        pygame.quit()
        exit(0)

    # Test collision of the bullets:
    for bullet in bullets:
        bullet.x += bullet_velocity
        if enemy_1_box.colliderect(bullet) or enemy_2_box.colliderect(bullet) or enemy_3_box.colliderect(bullet):
            bullets.remove(bullet)
            enemies_hit += 1
            bullet_hit_sound.play()
        elif bullet.x > screen_width:
            bullets.remove(bullet)
        
    # If the enemy is off the screen the user wins the game:
    
    if ((enemy_1_XPosition < 0 - enemy_1_width) or (enemy_2_XPosition < 0 - enemy_2_width) or (enemy_3_XPosition < 0 - enemy_3_width) or (playerBox.colliderect(prize_box))):
    
        # Display wining status to the user: 
                
        win_text = result_font.render("You win!", 1, white)
        screen.blit(lose_text, (screen_width//2 - win_text.get_width()//2, screen_height//2 - win_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000) # Pause the game for 5 seconds to display results before quitting
       
        # Quit game and exit window: 
        pygame.quit()
        exit(0)
    elif enemies_hit >= 10:

        # Display wining status to the user: 
                
        win_text = result_font.render("10 enemy hits. YOU WIN!", 1, white)
        screen.blit(win_text, (screen_width//2 - win_text.get_width()//2, screen_height//2 - win_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000) # Pause the game for 5 seconds to display results before quitting
       
        # Quit game and exit window: 
        pygame.quit()
        exit(0)

    # Make enemy approach the player.
    
    enemy_1_XPosition -= random.uniform(0.5, 1.4)
    enemy_2_XPosition -= random.uniform(0.8, 1.7)
    enemy_3_XPosition -= random.uniform(0.4, 1.4)
    prizeXPosition -= random.uniform(0.5, 1.4)
    
    # ================The game loop logic ends here. =============

    # Reflections on this project: 

    # Much of the code I wrote was done via copy and paste, meaning that code is being repeated. 
    # This is an indication that the program can be written more efficiently, perhaps through the use of objects and functions. 
    # Pygame is a wonderful library to learn with, with a low floor and high ceiling. I look forward to returning to this program
    # and trying to optimise it further. 

    # This code is adapted from the example.py file included in this folder. Additionally, 
    # I have used code and assets from this video tutorial (https://www.youtube.com/watch?v=jO6qQDNa2UY). 
    # While the game created in the tutorial is different to the game created here, I have used and adapted 
    # the code to create the shooting effect, as well as the sound effects. This was valuable as it allowed
    # me to practice integrating other peoples code into mine. It was necessary to have a strong grasp of how 
    # my code worked before I began implementing other code. 
  