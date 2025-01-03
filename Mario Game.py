from typing import Self
import pygame
import math
import time

pygame.init()

# Screen size
width, height = 1500, 1500

# Create screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("IT'S ME MARIO 2D")

# Load images
sky = pygame.image.load('sky.png')
ground_images = [
    pygame.image.load('island1.png'),
    pygame.image.load('island2.png'),
    pygame.image.load('island3.png'),
    pygame.image.load('island4.png'),
    pygame.image.load('island5.png')
]

Boss_Island = pygame.image.load('DonkyKongIsland.png')

Player = pygame.image.load("mario.png")
Player = pygame.transform.scale(Player, (20, 35))

plant_size = (40, 50) 
PlantNpcs = [pygame.transform.scale(pygame.image.load("PlantNpc.webp"), plant_size)] * 2

FireBall = pygame.image.load("FireBall.png")
FireBall = pygame.transform.scale(FireBall, (20, 20))

# Plant positions for each island two per island
plant_positions = [
    [(200, 360), (250, 360)],  # Positions on island 1
    [(660, 280), (710, 280)],  # Positions on island 2
    [(1060, 230), (1110, 230)],  # Positions on island 3
    [(810, 480), (860, 480)],  # Positions on island 4
    [(500, 430), (550, 430)],  # Positions on island 5
]

# Set up the player rectangle
hitbox = Player.get_rect(topleft=(178, 170))

# Frames
FPS = 6000
clock = pygame.time.Clock()

# Gravity and jump variables
gravity = 1
jump_force = -15
velocity_y = 0
on_ground = False

# Size for ground images
new_ground_width = 300
new_ground_height = 130
GroundRectWidth = 300
GroundRectHeight = 16
Boss_island_width = 300
Boss_island_height = 600

# Resize all ground images
ground_images = [
    pygame.transform.scale(img, (new_ground_width, new_ground_height))
    for img in ground_images
]

Boss_Island = pygame.transform.scale(Boss_Island, (Boss_island_width, Boss_island_height))

# Ground image position
BossIslandImg_position = (1100, 460)
BossIslandRect_position = (1100, 500)

# Ground image position
ground_image_position = [
    (140, 380),
    (600, 300),
    (1000, 250),
    (750, 500),
    (450, 450)
]

# Ground rectangle position
ground_rect_position = [
    (140, 410),
    (600, 330),
    (1000, 280),
    (750, 530),
    (450, 480)
]

# Collision rectangles for ground
ground_rect = []
for position in ground_rect_position:
    ground_rect.append(pygame.Rect(position[0], position[1], GroundRectWidth, GroundRectHeight))

Boss_IslandRect = pygame.Rect(BossIslandRect_position[0], BossIslandRect_position[1], Boss_island_width, Boss_island_height)

# Fireball class for NPC 
class Fireball:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = 5
        self.angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        self.rect = FireBall.get_rect(center=(x, y))

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x, self.y)

    def draw(self):
        screen.blit(FireBall, self.rect)

# Fireball class for player 
class PlayerFireball:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.speed = 10
        self.direction = direction  
        self.dx = self.speed if direction == 'right' else -self.speed
        self.rect = FireBall.get_rect(center=(x, y))

    def move(self):
        self.x += self.dx
        self.rect.center = (self.x, self.y)

    def draw(self):
        screen.blit(FireBall, self.rect)

# Active fireballs
fireballs = []
player_fireballs = []
last_shot_time = {pos: 0 for positions in plant_positions for pos in positions}

# Function to handle plant shooting
def plant_shoot(player_rect):
    current_time = time.time()
    for positions in plant_positions:
        for pos in positions:
            plant_x, plant_y = pos
            distance = math.sqrt((player_rect.centerx - plant_x) ** 2 + (player_rect.centery - plant_y) ** 2)
            cooldown = 3
            if distance < 200 and current_time - last_shot_time[pos] >= cooldown:  # Range for shooting fireballs and cooldown
                fireballs.append(Fireball(plant_x + plant_size[0] // 2, plant_y + plant_size[1] // 2, player_rect.centerx, player_rect.centery))
                last_shot_time[pos] = int(current_time)

# Function to check for collision with plant NPCs
def check_player_fireball_collisions():
    global player_health
    for fireball in player_fireballs[:]:
        for positions in plant_positions:
            for pos in positions:
                plant_rect = pygame.Rect(pos, plant_size)
                if fireball.rect.colliderect(plant_rect):
                    player_fireballs.remove(fireball)  # Remove the fireball on collision
                    break  
def background():
    # Makes background tiles for the screen
    bg_width, bg_height = sky.get_size()
    tiles = []

    # creates tiles for the background
    for x in range(width // bg_width + 1):
        for y in range(height // bg_height + 1):
            tiles.append((x * bg_width, y * bg_height))

    return tiles

def draw_plants():
    # Draw PlantNpc plants 
    for positions in plant_positions:
        for pos in positions:
            screen.blit(PlantNpcs[0], pos)

def draw_window(background_tiles, player, hitbox):

    screen.fill((0, 0, 0))  

    # Draw the background tiles
    for tile_position in background_tiles:
        screen.blit(sky, tile_position)

    # Draw the ground
    for i, rect in enumerate(ground_rect):
        screen.blit(ground_images[i], ground_image_position[i])
        pygame.draw.rect(screen, (255, 0, 0), rect, 2)

    # Draw Boss Island
    screen.blit(Boss_Island, BossIslandImg_position)
    pygame.draw.rect(screen, (0, 255, 0), Boss_IslandRect, 2)

    # Draw the plants
    draw_plants()

    # Draw fireballs
    for fireball in fireballs:
        fireball.draw()

    # Draw player fireballs
    for player_fireball in player_fireballs:
        player_fireball.draw()

    # Draw the player
    screen.blit(player, hitbox)

    pygame.display.update()

def draw_health():
    # show player health on the screen
    font = pygame.font.Font(None, 36)
    health_text = font.render(f"Health: {player_health}", True, (255, 255, 255))
    screen.blit(health_text, (10, 10))

def check_fireball_collisions(player_rect):
    global player_health
    for fireball in fireballs[:]:
        if player_rect.colliderect(fireball.rect):
            fireballs.remove(fireball)  # deletes the fireball on collision
            player_health -= 1  # Decrease player health
            if player_health <= 0:
                print("Player deleted!")
                return True  # Player is killed
    return False

# Player health
player_health = 30

def main():
    #  background tiles
    background_tiles = background()

    global velocity_y, on_ground
    global player_health
    running = True
    facing_right = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # click to shoot fireball
                    direction = 'right' if facing_right else 'left'
                    player_fireballs.append(PlayerFireball(hitbox.centerx, hitbox.centery, direction))

        # Check if player is  alive
        if player_health <= 0:
            break

        # Get pressed keys
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_a]:  # Move left
            hitbox.x -= 5
            facing_right = False

        if keys[pygame.K_d]:  # Move right
            hitbox.x += 5
            facing_right = True

        on_ground = False
        for rect in ground_rect:
            if hitbox.colliderect(rect) and velocity_y >= 0:
                on_ground = True
                hitbox.bottom = rect.top
                velocity_y = 0
                break  
        if hitbox.colliderect(Boss_IslandRect) and velocity_y >= 0:  # Check collision with Boss Island
            on_ground = True
            hitbox.bottom = Boss_IslandRect.top
            velocity_y = 0

        # Jump logic
        if keys[pygame.K_SPACE] and on_ground:  # Only jump if on the ground
            velocity_y = jump_force
            on_ground = False

        # Apply gravity
        if not on_ground:
            velocity_y += gravity
            hitbox.y += velocity_y

        # Player image flip
        player = pygame.transform.flip(Player, facing_right, False)


        def main():
            #  background tiles
            background_tiles = background()

            global velocity_y, on_ground
            global player_health
            running = True
            facing_right = True

            while running:
                clock.tick(FPS)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                

                # Function for killing plants when hit by fireballs
                def killing_plant():
                    global plant_positions
                    global PlantNpcs



                    class Plant:
                        def __init__(self, x, y):
                            self.x = x
                            self.y = y
                            self.health = 5  #  health of the plant

                        def get_rect(self):
                            return pygame.Rect(self.x, self.y, plant_size[0], plant_size[1])

                    # Create plants at their island positions
                    PlantNpcs = [Plant(x, y) for positions in plant_positions for x, y in positions]


                    
                    # through each fireball check if it hits any plant
                    for fireball in player_fireballs[:]:
                        for plant in PlantNpcs[:]:
                            plant_rect = plant.get_rect()

                            # collision between fireball and plant
                            if fireball.rect.colliderect(plant_rect):
                                plant.health -= 1  # Decrease plant health
                                player_fireballs.remove(fireball)  
                                if plant.health <= 0:
                                    PlantNpcs.remove(plant)
                                break 
                        



                # Move player and check collisions
                plant_shoot(hitbox)
                check_player_fireball_collisions()

                # Update and draw everything
                draw_window(background_tiles, Player, hitbox)

                # Draw the plants
                draw_plants()








        # Plant shooting logic
        plant_shoot(hitbox)

        # Move fireballs
        for fireball in fireballs:
            fireball.move()

        # Move player fireballs
        for player_fireball in player_fireballs:
            player_fireball.move()

        #  collisions with player fireballs
        check_player_fireball_collisions()

        #  collisions with fireballs
        if check_fireball_collisions(hitbox):
            running = False  # End game if player is killed

        # Draw everything
        draw_window(background_tiles, player, hitbox)
        draw_health()  

    print("Game Over")
    pygame.quit()

# Run the game
main()