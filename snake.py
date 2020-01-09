from pygame.locals import *
from random import randint
import pygame
import time


WIDTH_SPACES = 30
HEIGHT_SPACES = 30
WIDTH = 300
HEIGHT = 300
HEIGHT_STEP = HEIGHT // HEIGHT_SPACES
WIDTH_STEP = WIDTH // WIDTH_SPACES
MAX_WIDTH = WIDTH_STEP * WIDTH_SPACES
MAX_HEIGHT = HEIGHT_STEP * HEIGHT_SPACES
CLOCK = pygame.time.Clock()
FPS = 15
FRAME_TIME = 1/FPS

dirs = ('right', 'left', 'up', 'down')
key_dirs = (K_RIGHT, K_LEFT, K_UP, K_DOWN)


class Apple:
    def __init__(self, x, y):
        self.x = x * WIDTH_STEP
        self.y = y * HEIGHT_STEP
        self.old = None
        self.cur = None

    def move(self, not_allowed):
        self.old = self.cur
        self.x = randint(2, WIDTH_SPACES-2) * WIDTH_STEP
        self.y = randint(2, HEIGHT_SPACES-2) * HEIGHT_STEP
        while (self.x, self.y) in not_allowed:
            self.x = randint(2, WIDTH_SPACES-2) * WIDTH_STEP
            self.y = randint(2, HEIGHT_SPACES-2) * HEIGHT_STEP
 
    def draw(self, surface, image):
        self.cur = surface.blit(image, (self.x, self.y))

    def get_update_rects(self):
        return [self.cur, self.old]
 
 
class Player:
    direction = 'right'
    opp_dir = {
        'left': 'right',
        'right': 'left',
        'up': 'down',
        'down': 'up'
    }
    moves = {
        'up': (0, -1),
        'right': (1, 0),
        'down': (0, 1),
        'left': (-1, 0)
    }
    last_tail = (0,0)
    rects = []
 
    def __init__(self, length):
        self.length = length
        self.score = 0
        self.x = [i*WIDTH_STEP for i in range(self.length)]
        self.y = [i*HEIGHT_STEP for i in range(self.length)]
        for i in range(5):
            self.x.append(-100)
            self.y.append(-100)

    def get_body_coords(self):
        body = set()
        for i in range(1, self.length):
            body.add((self.x[i], self.y[i]))
        return body

    def get_near(self):
        pos = (self.x[0], self.y[0])
        body = self.get_body_coords()
        moves = {}
        for key, m in self.moves.items():
            npos = (pos[0] + (m[0]*WIDTH_STEP), pos[1] + (m[1]*HEIGHT_STEP))
            if npos in body:
                moves[key] = False
            elif self.is_wall(*npos):
                moves[key] = False
            else:
                moves[key] = True
        return [int(i) for i in moves.values()]
 
    def update(self):
        # update position of head of snake
        self.last_tail = (self.x[self.length-1], self.y[self.length-1])
        m = self.moves[self.direction]
        self.x.insert(0, self.x[0] + (m[0]*WIDTH_STEP))
        self.y.insert(0, self.y[0] + (m[1]*HEIGHT_STEP))
        self.x.pop()
        self.y.pop()

    def draw(self, surface, image):
        rects = []
        for i in range(self.length):
            rects.append(surface.blit(image, (self.x[i], self.y[i])))
        self.rects = rects


    def is_hit_wall(self):
        if self.is_wall(self.x[0], self.y[0]):
            return True

    def is_wall(self, x, y):
        if x < 0 or x > MAX_WIDTH or y < 0 or y > MAX_HEIGHT:
            return True

    def is_hit_self(self):
        cur = (self.x[0], self.y[0])
        for i in range(1, self.length):
            tail = (self.x[i], self.y[i])
            if cur == tail:
                return True

    def is_eat_apple(self, apple):
        for i in range(self.length):
            pos = (self.x[i], self.y[i])
            if pos == (apple.x, apple.y):
                self.x.append(0)
                self.y.append(0)
                return True

    def get_update_rects(self):
        rects = list(self.rects)
        rects.append(pygame.Rect(self.last_tail[0], self.last_tail[1], WIDTH_STEP, HEIGHT_STEP))
        return rects
 
class App:
    player = 0
    apple = 0
    IMAGE_SIZE = WIDTH_STEP
 
    def __init__(self):
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.player = Player(3) 
        self.apple = Apple(5, 5)
        self.is_quit = False

    def get_relevant_inputs(self):
        inputs = []
        inputs += self.distance_to_apple()
        inputs += self.player.get_near()
        inputs += [self.player.direction]
        return inputs

    def distance_to_apple(self):
        x = (self.apple.x - self.player.x[0]) // WIDTH_STEP
        y = (self.apple.y - self.player.y[0]) // HEIGHT_STEP
        return x, y

    def shortest_path_to_apple(self):
        player_start = (self.player.x[0], self.player.y[0])
        dist_map = {player_start: 0}
        q = [((self.player.x[0], self.player.y[0]), 0)]
        opp = {'up': 'down', 'right': 'left', 'down': 'up', 'left': 'right'}

        apple_pos = (self.apple.x, self.apple.y)
        body = self.player.get_body_coords()
        while q:
            pos, dist = q.pop(0)
            if pos == apple_pos:
                dist_map[pos] = dist
                break

            for direction, m in self.player.moves.items():
                npos = (pos[0] + (m[0]*WIDTH_STEP), pos[1] + (m[1]*HEIGHT_STEP))
                if npos in body:
                    continue
                elif self.player.is_wall(*npos):
                    continue
                else:
                    ndist = dist+1
                    key = (npos, ndist)
                    if ndist < dist_map.get(npos, float('inf')):
                        q.append(key)
                        dist_map[npos] = ndist

        moves = []
        pos = apple_pos
        while pos != player_start:
            dist = dist_map.get(pos, None)
            if dist is None:
                return dist
            for move, step in self.player.moves.items():
                npos = (pos[0] + (step[0]*WIDTH_STEP), pos[1] + (step[1]*HEIGHT_STEP))
                ndist = dist_map.get(npos, float('inf'))
                if ndist == dist-1:
                    moves.append(opp[move])
                    pos = npos
                    break
        return reversed(moves)

 
    def on_init(self):
        pygame.init()
        self.is_quit = False
        self._display_surf = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE)
 
        pygame.display.set_caption('Pygame pythonspot.com example')
        self._image_surf = pygame.image.load("img/snake_100.jpg").convert()
        self._image_surf = pygame.transform.scale(self._image_surf, (self.IMAGE_SIZE, self.IMAGE_SIZE))
        self._apple_surf = pygame.image.load("img/apple.png").convert()
        self._apple_surf = pygame.transform.scale(self._apple_surf, (self.IMAGE_SIZE, self.IMAGE_SIZE))
 
    def on_loop(self):
        ox, oy = self.distance_to_apple()
        self.player.update()
        nx, ny = self.distance_to_apple()
        if (abs(nx) < abs(ox)) or (abs(ny) < abs(oy)):
            reward = 1
        else:
            reward = -1
 
        # does snake eat apple?
        if self.player.is_eat_apple(self.apple):
            reward = 50
            self.player.score += reward
            body = self.player.get_body_coords()
            self.apple.move(body)
            self.player.length += 1
 
        if self.player.is_hit_self():
            print('YOU RAN INTO YOURSELF.')
            reward = -100
            self.player.score += reward
            self.exit()

        if self.player.is_hit_wall():
            print('YOU HIT A WALL.')
            reward = -100
            self.player.score += reward
            self.exit()

        return reward

    def exit(self):
        print(f'SCORE: {self.player.score}')
        # exit(0)
        self.is_quit = True
        # pygame.quit()

    def on_render(self):
        updates = []
        self._display_surf.fill((10,10,10))
        self.player.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)

        # updates += self.apple.get_update_rects()
        # updates += self.player.get_update_rects()
        pygame.display.update()

    def on_execute(self):
        self.on_init()
 
        start = 0
        next_direction = 'right'
        while True:

            end = time.perf_counter()
            if (end - start) > (FRAME_TIME):
                start = time.perf_counter()
                # print(self.player.get_near())
                # print(self.distance_to_apple())
                next_direction, reward = self.do_step(next_direction=next_direction)
                

    def do_step(self, next_direction='right'):
        events = pygame.event.get()
        for event in reversed(events):
            if event.type == KEYDOWN:
                if event.key in key_dirs:
                    index = key_dirs.index(event.key)
                    next_direction = dirs[index]
                    break
                elif event.key == K_ESCAPE:
                    self.exit()
        
        # don't allow player to go backwards into themselves
        if self.player.direction != self.player.opp_dir[next_direction]:
            self.player.direction = next_direction

        reward = self.on_loop()

        render_start = time.perf_counter()
        self.on_render()
        render_end = time.perf_counter()
        # print(f'Time to render: {(render_end-render_start):.3f}')

        CLOCK.tick()
        fps = CLOCK.get_fps()
        # print(f'FPS: {fps}')
        return next_direction, reward

 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
