import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 500, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Dodge - Smooth Racing")

WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

road_img = pygame.image.load("assets/road.png").convert()
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))

player_img = pygame.image.load("assets/player_car.png").convert_alpha()
enemy_images = [
    pygame.image.load("assets/enemy_car1.png").convert_alpha(),
    pygame.image.load("assets/enemy_car2.png").convert_alpha(),
    pygame.image.load("assets/enemy_car3.png").convert_alpha(),
    pygame.image.load("assets/enemy_car4.png").convert_alpha()
]

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

LANES = [110, 200, 300, 390]


class Player:
    def __init__(self):
        self.image = pygame.transform.scale(player_img, (40, 80))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 120))
        self.speed = 8  
        self.velocity = 5.0 

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 40:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH - 40:
            self.rect.x += self.speed

        if keys[pygame.K_DOWN]:
            self.velocity = max(2.0, self.velocity - 0.3)  
        else:
            self.velocity = min(15.0, self.velocity + 0.03)  

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Enemy:
    def __init__(self, lane_x):
        self.image = pygame.transform.scale(random.choice(enemy_images), (60, 120))
        self.rect = self.image.get_rect(center=(lane_x, -120))
        self.lane_x = lane_x
        self.speed = random.uniform(4.0, 7.0)

    def update(self, player_speed):
        self.rect.y += self.speed + (player_speed / 6)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.road_y = 0
        self.running = True
        self.game_over = False

    def draw_road(self):
        self.road_y += self.player.velocity
        if self.road_y >= HEIGHT:
            self.road_y = 0
        SCREEN.blit(road_img, (0, self.road_y))
        SCREEN.blit(road_img, (0, self.road_y - HEIGHT))

    def spawn_enemies(self):
        for lane_x in LANES:
            lane_occupied = any(e.lane_x == lane_x for e in self.enemies)
            if not lane_occupied and random.random() < 0.03:
                self.enemies.append(Enemy(lane_x))

    def update_enemies(self):
        for enemy in self.enemies[:]:
            enemy.update(self.player.velocity)
            if enemy.rect.top > HEIGHT:
                self.enemies.remove(enemy)
        self.spawn_enemies()

    def check_collision(self):
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.game_over = True

    def draw_speedometer(self):
        speed = int(self.player.velocity * 10)
        speed_text = font.render(f"Speed: {speed} km/h", True, WHITE)
        SCREEN.blit(speed_text, (10, 10))

    def restart(self):
        self.__init__()

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.game_over and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart()

            if not self.game_over:
                self.draw_road()

                self.player.move(keys)
                self.update_enemies()

                self.player.draw(SCREEN)
                for enemy in self.enemies:
                    enemy.draw(SCREEN)

                self.draw_speedometer()

                self.check_collision()

            else:
                SCREEN.fill(BLACK)
                game_over_text = big_font.render("CRASHED!", True, RED)
                restart_text = font.render("Press [R] to Restart", True, WHITE)
                SCREEN.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 60))
                SCREEN.blit(restart_text, (WIDTH // 2 - 140, HEIGHT // 2 + 10))

            pygame.display.update()
            clock.tick(60)


if __name__ == "__main__":
    Game().run()
