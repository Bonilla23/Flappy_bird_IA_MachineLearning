import pygame
import neat
import os
import random

pygame.init()

# Dimensiones
WIN_WIDTH = 500
WIN_HEIGHT = 800

# Cargar imágenes
BIRD_IMG = pygame.Surface((30,30))
BIRD_IMG.fill((255,255,0))
PIPE_IMG = pygame.Surface((70,400))
PIPE_IMG.fill((0,255,0))
BASE_IMG = pygame.Surface((WIN_WIDTH,100))
BASE_IMG.fill((139,69,19))
BG_COLOR = (135,206,250)

STAT_FONT = pygame.font.SysFont("comicsans", 50)

# Clases del juego
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0

    def jump(self):
        self.vel = -10

    def move(self):
        self.vel += 1
        self.y += self.vel

    def draw(self, win):
        win.blit(BIRD_IMG, (self.x, self.y))

class Pipe:
    GAP = 200
    VEL = 5
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, WIN_HEIGHT-300)
        self.passed = False

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        # Superior
        win.blit(PIPE_IMG, (self.x, self.height - PIPE_IMG.get_height()))
        # Inferior
        win.blit(PIPE_IMG, (self.x, self.height + self.GAP))

    def collide(self, bird):
        bird_rect = pygame.Rect(bird.x, bird.y, 30, 30)
        top_rect = pygame.Rect(self.x, self.height - PIPE_IMG.get_height(), 70, PIPE_IMG.get_height())
        bottom_rect = pygame.Rect(self.x, self.height + self.GAP, 70, PIPE_IMG.get_height())
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)

class Base:
    VEL = 5
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = WIN_WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + WIN_WIDTH < 0:
            self.x1 = self.x2 + WIN_WIDTH
        if self.x2 + WIN_WIDTH < 0:
            self.x2 = self.x1 + WIN_WIDTH

    def draw(self, win):
        win.blit(BASE_IMG, (self.x1, self.y))
        win.blit(BASE_IMG, (self.x2, self.y))

# Dibujar ventana
def draw_window(win, birds, pipes, base, score):
    win.fill(BG_COLOR)
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    for bird in birds:
        bird.draw(win)
    text = STAT_FONT.render(f"Score: {score}", 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    pygame.display.update()

# Evaluación de NEAT
def eval_genomes(genomes, config):
    nets = []
    birds = []
    ge = []

    for _, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230,350))
        genome.fitness = 0
        ge.append(genome)

    base = Base(700)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0

    run = True
    while run and len(birds) > 0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return

        pipe_ind = 0
        if len(pipes) > 1 and birds[0].x > pipes[0].x + 70:
            pipe_ind = 1

        for i, bird in enumerate(birds):
            bird.move()
            ge[i].fitness += 0.1
            output = nets[i].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - (pipes[pipe_ind].height + Pipe.GAP))))
            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            pipe.move()
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[i].fitness -= 1
                    birds.pop(i)
                    nets.pop(i)
                    ge.pop(i)
            if pipe.x + 70 < 0:
                rem.append(pipe)
            if not pipe.passed and pipe.x < birds[0].x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)

        for i, bird in enumerate(birds):
            if bird.y + 30 >= 700 or bird.y < 0:
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)

        base.move()
        draw_window(win, birds, pipes, base, score)

# Ejecutar NEAT
def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    winner = p.run(eval_genomes, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
