import pygame
import random
import os


class Game:

    def __init__(self, ai_playing):

        # AI Jogando
        self.ai_playing = ai_playing

        # Diretório do Arquivo
        self.filepath = os.path.dirname(__file__)

        # Inicia o Pygame
        pygame.init()

        # Escreve o Nome da Janela
        pygame.display.set_caption("Snake")

        # Determina o Ícone da Janela
        self.icon = pygame.image.load(os.path.join(self.filepath, "gfx/snake_ico.png"))
        pygame.display.set_icon(self.icon)

        # Criação da Janela
        self.screen_width = 1000
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Frame Rate
        self.fps = 20
        self.fps_clock = pygame.time.Clock()

        # Variáveis Controladoras do Jogo
        self.running = True

    def run(self, snake, apple, display):
        while self.running:

            move_per_tick = False

            self.screen.fill((0, 100, 0))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and snake.x_change != -10 and not move_per_tick:
                        snake.x_change = 10
                        snake.y_change = 0
                        move_per_tick = True
                    if event.key == pygame.K_LEFT and snake.x_change != 10 and not move_per_tick:
                        snake.x_change = -10
                        snake.y_change = 0
                        move_per_tick = True
                    if event.key == pygame.K_DOWN and snake.y_change != -10 and not move_per_tick:
                        snake.y_change = 10
                        snake.x_change = 0
                        move_per_tick = True
                    if event.key == pygame.K_UP and snake.y_change != 10 and not move_per_tick:
                        snake.y_change = -10
                        snake.x_change = 0
                        move_per_tick = True

            # Snake move
            snake.is_alive(self.screen_width, self.screen_height)

            if snake.alive:
                snake.move(self.screen_width, self.screen_height)

            if apple.is_score(snake.x[0], snake.y[0], self.screen_width, self.screen_height):
                snake.grow()
                display.score += 1

            # Desenha Objetos
            display.draw_score(self.screen)
            if self.ai_playing:
                display.draw_generation(self.screen)
            snake.draw(self.screen)
            apple.draw(self.screen)

            # Atualização da Tela
            pygame.display.update()

            # Finaliza o jogo caso tenha morrido colidido.
            if not snake.alive:
                self.running = False

            # Tick
            self.fps_clock.tick(self.fps)

        pygame.quit()


class Snake:

    def __init__(self, screen_width, screen_height):

        self.filepath = os.path.dirname(__file__)
        self.head_img = {'right': pygame.image.load(os.path.join(self.filepath, "gfx/sprites/snake/head/snake_head-right.png")),
                         'left': pygame.image.load(os.path.join(self.filepath, "gfx/sprites/snake/head/snake_head-left.png")),
                         'down': pygame.image.load(os.path.join(self.filepath, "gfx/sprites/snake/head/snake_head-down.png")),
                         'up': pygame.image.load(os.path.join(self.filepath, "gfx/sprites/snake/head/snake_head-up.png"))
                         }
        self.body_img = pygame.image.load(os.path.join(self.filepath, "gfx/sprites/snake/body/snake_body.png"))

        # Calculo da posição inicial
        while (screen_width / 2) % 10 != 0:
            screen_width -= 1
        while (screen_height / 2) % 10 != 0:
            screen_height -= 1

        self.x = [screen_width/2]
        self.y = [screen_height/2]
        self.x_change = 0
        self.y_change = 0
        self.direction = 'down'
        self.size = 0
        self.alive = True

    def move(self, screen_width, screen_height):
        for i in range(self.size, -1, -1):
            if i > 1:
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]
            elif i == 1:
                self.x[i] = self.x[0]
                self.y[i] = self.y[0]
            else:
                # Verifica a direção
                if self.x_change == 10:
                    self.direction = 'right'
                elif self.x_change == -10:
                    self.direction = 'left'
                elif self.y_change == 10:
                    self.direction = 'down'
                elif self.y_change == -10:
                    self.direction = 'up'

                # Limites Eixo X
                if self.x[0] <= 0:
                    self.x[0] = 0
                    if self.x_change <= -10:
                        self.x_change = 0
                if self.x[0] >= screen_width - self.head_img[self.direction].get_width():
                    self.x[0] = screen_width - self.head_img[self.direction].get_width()
                    if self.x_change >= 10:
                        self.x_change = 0

                # Limites Eixo Y
                if self.y[0] <= 0:
                    self.y[0] = 0
                    if self.y_change <= -10:
                        self.y_change = 0
                if self.y[0] >= screen_height - self.head_img[self.direction].get_width():
                    self.y[0] = screen_height - self.head_img[self.direction].get_width()
                    if self.y_change >= 10:
                        self.y_change = 0

                # Movimentação
                self.x[0] += self.x_change
                self.y[0] += self.y_change

    def is_alive(self, screen_width, screen_height):
        for i in range(self.size):
            if i == 0:
                continue
            elif self.x[0] == self.x[i] and self.y[0] == self.y[i]:
                self.alive = False
        if (self.x[0] + self.x_change) < 0:
            self.alive = False
        elif (self.x[0] + self.x_change) > (screen_width - self.head_img[self.direction].get_width()):
            self.alive = False
        elif (self.y[0] + self.y_change) < 0:
            self.alive = False
        elif (self.y[0] + self.y_change) > (screen_height - self.head_img[self.direction].get_height()):
            self.alive = False

    def grow(self):
        self.size += 1
        self.x.append(self.x[0])
        self.y.append(self.y[0])

    def draw(self, screen):
        for i in range(self.size, -1, -1):
            if i != 0:
                screen.blit(self.body_img, (self.x[i], self.y[i]))
            else:
                screen.blit(self.head_img[self.direction], (self.x[i], self.y[i]))


class Apple:

    def __init__(self, snake_x, snake_y, screen_width, screen_height):

        self.filepath = os.path.dirname(__file__)
        self.img = pygame.image.load(os.path.join(self.filepath, "gfx/sprites/apple/apple.png"))
        self.x = random.randrange(0, screen_width - self.img.get_width(), 10)
        self.y = random.randrange(0, screen_height - self.img.get_height(), 10)

        while self.x == snake_x and self.y == snake_y:
            self.x = random.randrange(0, screen_width - self.img.get_width(), 10)
            self.y = random.randrange(0, screen_height - self.img.get_height(), 10)

    def is_score(self, snake_x, snake_y, screen_width, screen_height):
        if self.x == snake_x and self.y == snake_y:
            while self.x == snake_x and self.y == snake_y:
                self.x = random.randrange(0, screen_width - self.img.get_width(), 10)
                self.y = random.randrange(0, screen_height - self.img.get_height(), 10)
            return True
        else:
            return False

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))


class Display:

    def __init__(self):
        # Fonte de Texto
        self.text_font = pygame.font.Font('freesansbold.ttf', 32)

        # Pontuação
        self.score = 0
        self.score_display = self.text_font.render("Score: " + str(self.score), True, (255, 255, 255))

        # Geração IA
        self.generation = 0
        self.generation_display = self.text_font.render("Generation: " + str(self.generation), True,
                                                        (255, 255, 255))

    def draw_score(self, screen):
        self.score_display = self.text_font.render("Score: " + str(self.score), True, (255, 255, 255))
        screen.blit(self.score_display, (0, 0))

    def draw_generation(self, screen):
        self.generation_display = self.text_font.render("Generation: " + str(self.generation), True, (255, 255, 255))
        screen.blit(self.generation_display, (0, 570))


def main():
    game = Game(ai_playing=True)
    player = Snake(game.screen_width, game.screen_height)
    point = Apple(player.x, player.y, game.screen_width, game.screen_height)
    display = Display()

    game.run(player, point, display)


if __name__ == '__main__':
    main()
