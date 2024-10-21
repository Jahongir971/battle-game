import pygame
import random

# Pygame ni boshlash
pygame.init()

# O'yin ekranining o'lchamlari
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Pixel Battle Grounds")

# Ranglar
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# O'yin obyektlari
class Player:
    def __init__(self):
        self.image = pygame.image.load('sprites/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))  # Kichikroq sprite
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.level = 1
        self.experience = 0
        self.skill_unlocked = False
        self.health = 100
        self.attack_damage = 10
        self.has_sword = False
        self.skill_active = False
        self.skill_duration = 0

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= 500 and not self.skill_unlocked:
            self.skill_unlocked = True

    def use_skill(self):
        if self.skill_unlocked and not self.skill_active:
            self.skill_active = True
            self.skill_duration = 300  # 10 sekund (30 fps * 10 sek)

    def level_up(self):
        self.level += 1
        self.attack_damage += 5

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, dx, dy):
        # Ekrandan chiqmaslik
        if 0 < self.rect.x + dx < WIDTH - self.rect.width:
            self.rect.x += dx
        if 0 < self.rect.y + dy < HEIGHT - self.rect.height:
            self.rect.y += dy

class Creature:
    def __init__(self):
        self.image = pygame.image.load('sprites/creature.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))  # Kichikroq sprite
        self.rect = self.image.get_rect(topleft=(random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 50)))
        self.health = 100  # Har bir maxluq 100 sog'liqga ega

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        # Sog'likni ko'rsatish
        health_text = font.render(f'HP: {self.health}', True, BLACK)
        surface.blit(health_text, (self.rect.x, self.rect.y - 20))

    def is_hit(self, damage):
        self.health -= damage
        return self.health <= 0

class Boss:
    def __init__(self):
        self.image = pygame.image.load('sprites/boss.png').convert_alpha()  # Boss sprite
        self.image = pygame.transform.scale(self.image, (80, 80))  # Katta boss
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.health = 1000

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        # Sog'likni ko'rsatish
        health_text = font.render(f'Boss HP: {self.health}', True, RED)
        surface.blit(health_text, (self.rect.x, self.rect.y - 20))

    def is_hit(self, damage):
        self.health -= damage
        return self.health <= 0

class Sword:
    def __init__(self):
        self.image = pygame.image.load('sprites/sword.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 10))  # Kichikroq qilich
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 50)))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class LongSword(Sword):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('sprites/long_sword.png').convert_alpha()  # Long sword sprite
        self.image = pygame.transform.scale(self.image, (50, 10))  # Katta qilich
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 50)))

# O'yin funksiyasi
def game_loop():
    global font
    clock = pygame.time.Clock()
    player = Player()
    sword = Sword()  # Oddiy qilich
    long_sword = LongSword()  # Long sword
    boss = Boss()  # Boss yaratish
    creatures = [Creature() for _ in range(5)]  # Maxluqlarni yaratish
    running = True
    font = pygame.font.Font(None, 36)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Ekranni tozalash
        screen.fill(WHITE)

        # O'yinchi harakatini nazorat qilish
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -5
        if keys[pygame.K_RIGHT]:
            dx = 5
        if keys[pygame.K_UP]:
            dy = -5
        if keys[pygame.K_DOWN]:
            dy = 5
        player.move(dx, dy)

        # Qilichni olish
        if keys[pygame.K_g]:  # Qilichni olish
            if player.rect.colliderect(sword.rect) and not player.has_sword:
                player.has_sword = True
                sword.rect.x, sword.rect.y = -100, -100  # Oddiy qilichni ekrandan olib tashlash

        # Long qilichni olish
        if keys[pygame.K_l]:  # Long qilichni olish
            if player.rect.colliderect(long_sword.rect) and player.has_sword:
                player.attack_damage += 15  # Long qilich urish kuchini oshiradi
                long_sword.rect.x, long_sword.rect.y = -100, -100  # Long qilichni ekrandan olib tashlash

        # Maxluqlarni chizish va urish
        for creature in creatures:
            creature.draw(screen)

            if keys[pygame.K_f]:  # Maxluqni urish
                attack_range = 150 if player.skill_active else 30  # Skill aktiv bo'lsa masofa kengayadi
                if player.rect.colliderect(creature.rect.inflate(attack_range, attack_range)) and player.has_sword:
                    if creature.is_hit(player.attack_damage):
                        player.gain_experience(50)
                        creatures.remove(creature)
                        break

        # Bossni urish
        if keys[pygame.K_b]:  # Bossni urish
            attack_range = 150 if player.skill_active else 30
            if player.rect.colliderect(boss.rect.inflate(attack_range, attack_range)) and player.has_sword:
                if boss.is_hit(player.attack_damage):
                    player.gain_experience(200)  # Bossni urganingizda ko'proq tajriba

        # Bossni urishdan o'zini himoya qilish
        if player.rect.colliderect(boss.rect) and player.health > 0:
            player.health -= 5  # Boss o'yinchiga zarba beradi

        # Maxluqlarni qayta paydo qilish
        if len(creatures) < 5:
            creatures.append(Creature())

        # Qilichni chizish
        if not player.has_sword:
            sword.draw(screen)
        else:
            long_sword.draw(screen)  # Long qilichni chizish

        # O'yinchini chizish
        player.draw(screen)
        boss.draw(screen)  # Bossni chizish

        # Hayotni ko'rsatish
        if player.health <= 0:
            game_over_text = font.render('Game Over', True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False

        # Level va skill holatini ko'rsatish
        text = font.render(f'Level: {player.level}, Health: {player.health}, Exp: {player.experience}, Skill: {"Unlocked" if player.skill_unlocked else "Locked"}', True, BLACK)
        screen.blit(text, (10, 10))

        # Skill ishlatilishini ko'rsatish
        if player.skill_active:
            player.skill_duration -= 1
            if player.skill_duration <= 0:
                player.skill_active = False
            skill_text = font.render(f'Skill Active! {player.skill_duration // 30} sec left', True, GREEN)
            screen.blit(skill_text, (WIDTH - 200, 10))

        # O'yin yangilash
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

game_loop()
