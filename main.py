import pygame
import sys
from enum import Enum

# 初始化 Pygame
pygame.init()

# 游戏配置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.5
JUMP_POWER = -12

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

class GameState(Enum):
    PLAYING = 1
    GAME_OVER = 2
    WIN = 3

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.vel_y = 0
        self.on_ground = False
        self.speed = 5
    
    def update(self, platforms, enemies):
        # 获取按键
        keys = pygame.key.get_pressed()
        
        # 左右移动
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        
        # 边界检查
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        
        # 重力作用
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        
        # 碰撞检测 - 平台
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # 从上面落下
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
        
        # 碰撞检测 - 敌人
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                return False  # 游戏结束
        
        # 掉落死亡
        if self.rect.top > SCREEN_HEIGHT:
            return False
        
        return True
    
    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_POWER
            self.on_ground = False

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=GREEN):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 2
        self.direction = 1
        self.left_bound = x - 50
        self.right_bound = x + 50
    
    def update(self):
        self.rect.x += self.speed * self.direction
        
        if self.rect.x <= self.left_bound or self.rect.x >= self.right_bound:
            self.direction *= -1

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platform Jump Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.state = GameState.PLAYING
        
        self.init_level()
    
    def init_level(self):
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        # 创建平台
        self.platforms.add(Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40))  # 地面
        self.platforms.add(Platform(150, 500, 200, 20))
        self.platforms.add(Platform(500, 450, 200, 20))
        self.platforms.add(Platform(150, 350, 200, 20))
        self.platforms.add(Platform(500, 300, 200, 20))
        self.platforms.add(Platform(300, 150, 200, 20))  # 顶部平台
        
        # 创建玩家
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        
        # 创建敌人
        self.enemies.add(Enemy(500, 250, 30, 30))
        self.enemies.add(Enemy(200, 400, 30, 30))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                if event.key == pygame.K_r and self.state != GameState.PLAYING:
                    self.state = GameState.PLAYING
                    self.init_level()
        return True
    
    def update(self):
        if self.state != GameState.PLAYING:
            return
        
        # 更新敌人
        self.enemies.update()
        
        # 更新玩家
        is_alive = self.player.update(self.platforms, self.enemies)
        if not is_alive:
            self.state = GameState.GAME_OVER
        
        # 检查胜利条件（到达顶部平台）
        if self.player.rect.y < 100:
            self.state = GameState.WIN
    
    def draw(self):
        self.screen.fill(WHITE)
        
        # 绘制平台
        self.platforms.draw(self.screen)
        
        # 绘制敌人
        self.enemies.draw(self.screen)
        
        # 绘制玩家
        self.screen.blit(self.player.image, self.player.rect)
        
        # 绘制状态信息
        if self.state == GameState.GAME_OVER:
            text = self.font.render("GAME OVER! Press R to Restart", True, RED)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
        elif self.state == GameState.WIN:
            text = self.font.render("YOU WIN! Press R to Restart", True, GREEN)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
