from time import sleep

import pygame
import secrets

class Projectile_Entity:

    def __init__(self, name, x, y, speed, image_path):
        self.x = x
        self.y = y
        self.name = name
        self.speed = speed
        self.image = pygame.image.load(image_path)
        self.on_screen = True

    def move(self, y_border):
        if 0 < (self.y + self.speed) < y_border - 32:
            self.y -= self.speed
        else:
            self.on_screen = False

class Bot_Entity:

    def __init__(self, name, x, y, speed, image_path):
        self.x = x
        self.y = y
        self.new_x = 0
        self.new_y = 0
        self.name = name
        self.speed = speed
        self.on_screen = True
        self.image = pygame.image.load(image_path)

    def move_direction_y(self):
        self.new_y = self.speed

    def move(self, y_border):
        if 0 < (self.y + self.new_y) < y_border - 32:
            self.y += self.new_y
        else:
            self.on_screen = False

class Player_Entity:

    def __init__(self, name, x, y, image_path):
     self.x = x
     self.y = y
     self.new_x = 0
     self.new_y = 0
     self.name = name
     self.score = 0
     self.lives = 3
     self.image = pygame.image.load(image_path)

    def move_direction_x(self, new_x):
        self.new_x = new_x

    def move_direction_y(self, new_y):
        self.new_y = new_y


    def move(self, x_border, y_border):
        if 0 < self.x + self.new_x < x_border - 32:
            self.x += self.new_x

        if 0 < (self.y + self.new_y) < y_border - 32:
            self.y += self.new_y

    def increase_score(self, score_add):
        self.score += score_add

    def decrease_lives(self, live_decrease):
        self.lives -= live_decrease

class Game:

    def __init__(self, x_border, y_border, caption, alien_count, background=None):
        self.x_border = x_border
        self.y_border = y_border
        self.alien_count = alien_count
        self.screen = pygame.display.set_mode((x_border, y_border))
        self.game_is_running = True

        self.background = None
        self.__set_background(background)

        pygame.display.set_caption(caption)

        self.Player_Entities = []
        self.Bot_Entities = []
        self.Projectile_Entities = []

    def start_main_loop(self):
        pygame.init()

        stats_font = pygame.font.SysFont("Times New Roman", 18)

        missiles_to_remove = []

        while self.game_is_running:

            # Display background
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))

            # Move and display Entities

            # Player
            for p_entity in self.Player_Entities:
                p_entity.move(self.x_border, self.y_border)
                self.screen.blit(p_entity.image, (p_entity.x, p_entity.y))

            # Alien
            # Filter out aliens which were hit by a missile or are not on the screen
            self.Bot_Entities = list(filter(lambda x:x.on_screen == True, self.Bot_Entities))

            for _ in range(0, self.alien_count - len(self.Bot_Entities)):
                alien = Bot_Entity("Bot", secrets.choice(range(0, 614)), 1, 1, "space-invaders-alien.png")
                self.Bot_Entities.append(alien)

            for b_entity in self.Bot_Entities:
                b_entity.move_direction_y()
                b_entity.move(self.y_border)
                self.screen.blit(b_entity.image, (b_entity.x, b_entity.y))

            # Missiles

            # Filter missiles which are not on screen
            self.Projectile_Entities = list(filter(lambda x:x.on_screen == True, self.Projectile_Entities))

            for index, projectile_entity in enumerate(self.Projectile_Entities):
                projectile_entity.move(self.y_border)
                self.screen.blit(projectile_entity.image, (projectile_entity.x, projectile_entity.y))

            missiles_to_remove.clear()

            # Check for collision

            # Alien Player collision
            for p_entity in self.Player_Entities:
                for b_entity in self.Bot_Entities:
                    if set(range(p_entity.x, p_entity.x + 33)).intersection(range(b_entity.x, b_entity.x + 33)).__len__() > 0 and set(range(p_entity.y, p_entity.y + 33)).intersection(range(b_entity.y, b_entity.y + 33)).__len__() > 0:
                        p_entity.decrease_lives(1)
                        b_entity.on_screen = 0

            # Missile Alien collision
            for missile in self.Projectile_Entities:
                for b_entity in self.Bot_Entities:
                    if set(range(missile.x, missile.x + 33)).intersection(range(b_entity.x, b_entity.x + 33)).__len__() > 0 and set(range(missile.y, missile.y + 33)).intersection(range(b_entity.y, b_entity.y + 33)).__len__() > 0:
                        b_entity.on_screen = False
                        missile.on_screen = False
                        for player in self.Player_Entities:
                            player.increase_score(1)

            # Show score
            for p_entity in self.Player_Entities:
                player_score = stats_font.render(str(p_entity.score), True, (255, 255, 255))
                self.screen.blit(player_score, (0, 0))

            # Show lives
            for p_entity in self.Player_Entities:
                player_lives = stats_font.render(str(p_entity.lives), True, (255, 255, 255))
                self.screen.blit(player_lives, (600, 0))

            # Check events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_is_running = False
                    break

                # If key was pressed
                if event.type == pygame.KEYDOWN:

                    # Movement
                    if event.key == pygame.K_w:
                        for entity in self.Player_Entities:
                            entity.move_direction_y(-1)

                    if event.key == pygame.K_s:
                        for entity in self.Player_Entities:
                            entity.move_direction_y(1)

                    if event.key == pygame.K_a:
                        for entity in self.Player_Entities:
                            entity.move_direction_x(-1)

                    if event.key == pygame.K_d:
                        for entity in self.Player_Entities:
                            entity.move_direction_x(1)

                    # Fire
                    if event.key == pygame.K_SPACE:
                        for entity in self.Player_Entities:
                            projectile_1 = Projectile_Entity("projectile1", entity.x , entity.y, 1, "missile.png")
                            projectile_2 = Projectile_Entity("projectile2", entity.x + 16, entity.y, 1, "missile.png")
                            self.Projectile_Entities.append(projectile_1)
                            self.Projectile_Entities.append(projectile_2)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        for entity in self.Player_Entities:
                            entity.move_direction_y(0)

                    if event.key == pygame.K_a or event.key == pygame.K_d:
                        for entity in self.Player_Entities:
                            entity.move_direction_x(0)

            sleep(0.003)
            pygame.display.update()

    def __set_background(self, background_path):
        if background_path:
            self.background = pygame.image.load(background_path)

    def add_player_entity(self, entity):
        self.Player_Entities.append(entity)

    def add_bot_entity(self, bot):
        self.Bot_Entities.append(bot)

if __name__ == '__main__':
    game = Game(614, 335, "Space - Invaders", 3, "Starfield.png")

    player_entity = Player_Entity("Player", 307, 115, "space-invaders-ship.png")

    game.add_player_entity(player_entity)


    game.start_main_loop()
