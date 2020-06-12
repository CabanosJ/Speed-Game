# Jeremiah Cabanos
# Zenva game tutorial
# 6/12/20
import pygame


# Size of screen constants
SCREEN_TITLE = 'Crossy'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
# Colors with RGB codes
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
# Creates clock and constant tick rate
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('arial', 75)
level = 1

class Game:
    TICK_RATE = 60

    # Initializer for the game class to set display
    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        # Creates window display with specified size
        self.game_screen = pygame.display.set_mode((width, height))
        # Sets the window color to white
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)

        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width, height))

    # Function to run lose status
    def collided(self):
        is_game_over = True
        did_win = False
        text = font.render('You lose!', True, BLACK_COLOR)
        self.game_screen.blit(text, (300, 350))
        pygame.display.update()
        clock.tick(1)
    
    def run_game_loop(self, level_speed):
        is_game_over = False
        did_win = False
        direction = 0
        global level
        level += 1

        # Player character creation
        player_character = PlayerCharacter('player.png', 375, 700, 50, 50)
        player_character.SPEED += .10

        # Enemy character creation
        enemy_0 = NPC('enemy.png', 20, 200, 50, 50)
        enemy_0.SPEED *= level_speed
        enemy_1 = NPC('enemy.png', self.width - 50, 400, 50, 50)
        enemy_1.SPEED *= level_speed
        enemy_2 = NPC('enemy.png', 350, 600, 50, 50)
        enemy_2.SPEED *= level_speed

        # Treasure creation
        treasure = GameObject('treasure.png', 375, 50, 50, 50)
        
        # Main game loop, updates at each tick
        while not is_game_over:
        # Loop to read all the events (mouse clicks, button clicks, etc)
            for event in pygame.event.get():
                # Quit type event will exit out of the game loop
                if event.type == pygame.QUIT:
                    is_game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction = 1
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0

            # Draws background with updated data
            self.game_screen.fill(WHITE_COLOR)
            self.game_screen.blit(self.image, (0, 0))
            treasure.draw(self.game_screen)

            # Draws character
            player_character.move(direction, self.height)
            player_character.draw(self.game_screen)

            #Draws enemies at certain levels
            enemy_0.move(self.width)
            enemy_0.draw(self.game_screen)

            if level_speed > 1:
                enemy_1.move(self.width)
                enemy_1.draw(self.game_screen)
                if player_character.detect_collision(enemy_1):
                    self.collided()
                    break
                
            if level_speed > 2:
                enemy_2.move(self.width)
                enemy_2.draw(self.game_screen)
                if player_character.detect_collision(enemy_2):
                    self.collided()
                    break

            if player_character.detect_collision(enemy_0):
                self.collided()
                break

            # Prints next level on win status
            elif player_character.detect_collision(treasure):
                is_game_over = True
                did_win = True
                text = font.render('LEVEL: ' + str(level), True, BLACK_COLOR)
                self.game_screen.blit(text, (275, 350))
                pygame.display.update()
                clock.tick(1)
                break
            
            # Updates the graphics
            pygame.display.update()
            clock.tick(self.TICK_RATE)

        # Recursively runs the game when in a winning state
        if did_win:
            self.run_game_loop(level_speed + 0.25)
        else:
            return

class GameObject:
    def __init__(self, image_path, x, y, width, height):
        object_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(object_image, (width, height))
        
        self.x_pos = x
        self.y_pos = y

        self.width = width
        self.height = height

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))


class PlayerCharacter(GameObject):
    SPEED = 10

    
    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    # Moves character and places bounds on y axis
    def move(self, direction, max_height):
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED
        if self.y_pos >= max_height - 50:
            self.y_pos = max_height - 50

    # Checks if x or y positions intersect with each other
    def detect_collision(self, other_body):
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False
        
        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            return False
        
        return True

# Class for non player characters
class NPC(GameObject):
    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

        
    def move(self, max_width):
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >= max_width - 50:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED


pygame.init()
new_game = Game('background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(1)
pygame.quit()
quit()

