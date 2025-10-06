import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 500, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Game")

WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

background_music = pygame.mixer.Sound("assets/bg_music.wav")
background_music.play()
laser_sound = pygame.mixer.Sound("assets/laser.wav")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")

space_bg = pygame.image.load("assets/space.png").convert()
space_bg = pygame.transform.scale(space_bg, (WIDTH, HEIGHT))

player_img = pygame.image.load("assets/player.png").convert_alpha()
enemy_img = pygame.image.load("assets/enemy.png").convert_alpha()

class Player:
    def __init__(self):
        self.image = pygame.transform.scale(player_img, (40, 80))
        self.rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 60, 50, 50)
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x + 23, y, 5, 10)
        self.speed = 8

    def move(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.rect)


class Enemy:
    def __init__(self):
        self.image = pygame.transform.scale(enemy_img, (40, 40))
        self.rect = pygame.Rect(random.randint(0, WIDTH - 40), -40, 40, 40)
        self.speed = random.randint(2, 5)

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def main():
    player = Player()
    bullets = []
    enemies = []
    enemy_spawn_delay = 30
    score = 0
    game_over = False
    bg_y = 0

    while True:
        SCREEN.blit(space_bg, (0, 0))
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullets.append(Bullet(player.rect.x, player.rect.y))
                laser_sound.play()
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                main()  
        
        bg_y += 1
        if bg_y >= HEIGHT:
            bg_y = 0
        SCREEN.blit(space_bg, (0, bg_y))
        SCREEN.blit(space_bg, (0, bg_y - HEIGHT))

        if not game_over:
            player.move(keys)
            player.draw(SCREEN)


        if not game_over:
            player.move(keys)
            player.draw(SCREEN)

            for bullet in bullets[:]:
                bullet.move()
                bullet.draw(SCREEN)
                if bullet.rect.y < 0:
                    bullets.remove(bullet)

            if random.randint(1, enemy_spawn_delay) == 1:
                enemies.append(Enemy())

            for enemy in enemies[:]:
                enemy.move()
                enemy.draw(SCREEN)

                if enemy.rect.colliderect(player.rect):
                    game_over = True

                for bullet in bullets[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        if bullet in bullets:
                            bullets.remove(bullet)
                        if enemy in enemies:
                            enemies.remove(enemy)
                        explosion_sound.play()
                        score += 1
                        break

                if enemy.rect.y > HEIGHT:
                    enemies.remove(enemy)

            score_text = font.render(f"Score: {score}", True, WHITE)
            SCREEN.blit(score_text, (10, 10))
        else:
            game_over_text = font.render("GAME OVER", True, RED)
            restart_text = font.render("Press [R] to Restart", True, WHITE)
            score_text = font.render(f"Final Score: {score}", True, YELLOW)

            SCREEN.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 60))
            SCREEN.blit(score_text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
            SCREEN.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 20))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()