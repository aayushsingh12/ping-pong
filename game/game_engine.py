import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.winning_score = 5  # default target
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        # Sounds
        self.sound_paddle = pygame.mixer.Sound("assets/paddle_hit.wav")
        self.sound_wall = pygame.mixer.Sound("assets/wall_bounce.wav")
        self.sound_score = pygame.mixer.Sound("assets/score.wav")

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # Move ball and handle wall bounce
        event = self.ball.move()
        if event == "wall":
            self.sound_wall.play()

        # Paddle collision
        event = self.ball.check_collision(self.player, self.ai)
        if event == "paddle":
            self.sound_paddle.play()

        # Scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
            self.sound_score.play()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()
            self.sound_score.play()

        # Move AI paddle
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

    def check_game_over(self, screen):
        if self.player_score == self.winning_score or self.ai_score == self.winning_score:
            winner = "Player Wins!" if self.player_score == self.winning_score else "AI Wins!"
            text = self.font.render(winner, True, WHITE)
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(2000)  # show result for 2 seconds

            # Show replay options
            return self.show_replay_menu(screen)
        return False

    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()

    def show_replay_menu(self, screen):
        menu_font = pygame.font.SysFont("Arial", 28)

        while True:
            screen.fill((0, 0, 0))
            options = [
                "Press 3 for Best of 3",
                "Press 5 for Best of 5",
                "Press 7 for Best of 7",
                "Press ESC to Exit"
            ]

            for i, option in enumerate(options):
                text = menu_font.render(option, True, WHITE)
                rect = text.get_rect(center=(self.width // 2, 200 + i * 50))
                screen.blit(text, rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True  # quit game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.winning_score = 2  # best of 3 → first to 2 wins
                        self.reset_game()
                        return False
                    elif event.key == pygame.K_5:
                        self.winning_score = 3  # best of 5 → first to 3 wins
                        self.reset_game()
                        return False
                    elif event.key == pygame.K_7:
                        self.winning_score = 4  # best of 7 → first to 4 wins
                        self.reset_game()
                        return False
                    elif event.key == pygame.K_ESCAPE:
                        return True  # quit game
