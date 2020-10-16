import pygame as pg
import numpy as np

SCORE_BOARD_SIZE_Y = 100

BALL_SIZE = pg.Vector2(10, 10)
PADDLE_SIZE = pg.Vector2(10, 50)
WINDOW_SIZE = pg.Vector2(800, 600)
PLAY_BOARD_OFFSET = pg.Vector2(0, SCORE_BOARD_SIZE_Y)
PLAY_BOARD_SIZE = WINDOW_SIZE - PLAY_BOARD_OFFSET

CENTRAL_LINE_DOTS_SIZE = pg.Vector2(3, 7)

display = pg.display.set_mode((int(WINDOW_SIZE.x), int(WINDOW_SIZE.y)))
background_color = (0, 0, 0)
foreground_color = (255, 255, 255)

PLAYER_1_CONTROLLS = (pg.K_w, pg.K_s)
PLAYER_2_CONTROLLS = (pg.K_UP, pg.K_DOWN)
PLAYER_MOVE_SPEED = 5
PLAYER_MOVE_EFFECT_COEF = .2

clock = pg.time.Clock()

class Paddle:
    position = pg.Vector2()
    size = pg.Vector2()
    last_movement = pg.Vector2()
    
    def __init__(self, position, size):
        self.position = position
        self.size = size
    
    def draw(self):
        pg.draw.rect(display, foreground_color, (self.position - (.5 * self.size) + PLAY_BOARD_OFFSET, self.size))

class Ball:
    position = pg.Vector2()
    size = pg.Vector2()
    velocity = pg.Vector2()
    
    def __init__(self, position, size, velocity):
        self.position = position
        self.size = size
        self.velocity = velocity
    
    def update(self):
        self.position += self.velocity
    
    def draw(self):
        pg.draw.rect(display, foreground_color, (self.position - (.5 * self.size) + PLAY_BOARD_OFFSET, self.size))
    
    def collision(self, paddle):
        assert isinstance(paddle, Paddle), "Argument should be a Paddle"
        diff = self.position - paddle.position
        abs_diff = pg.Vector2(abs(diff.x), abs(diff.y))
        size_sum = (self.size + paddle.size) / 2
        if abs_diff.x < size_sum.x and abs_diff.y < size_sum.y :
            self.velocity.x = -self.velocity.x
            self.position.x = paddle.position.x + np.sign(diff.x) * size_sum.x
            self.velocity += .3 * paddle.last_movement
    
    def check_walls(self):
        if(self.position.y < 0 + self.size.y / 2) :
            self.position.y = self.size.y / 2
            self.velocity.y = -self.velocity.y
        if(self.position.y > PLAY_BOARD_SIZE.y - self.size.y / 2) :
            self.position.y = PLAY_BOARD_SIZE.y - self.size.y / 2
            self.velocity.y = - self.velocity.y
    
    def check_for_point(reset_position, player):
        if(self.position.x < 0 + self.size.x / 2) :
            self.position = reset_position
            return 2
        if(self.position.x > PLAY_BOARD_SIZE - self.size.x / 2)
            self.position = reset_position
            return 1
    
def main () :
    pg.display.flip()

    pg.display.set_caption('Pong')
    display.fill(background_color)
    
    pg.display.update()
    
    paddles = []
    
    player_1 = Paddle(pg.Vector2(30, PLAY_BOARD_SIZE.y / 2), pg.Vector2(PADDLE_SIZE))
    player_2 = Paddle(pg.Vector2(PLAY_BOARD_SIZE.x - 30, PLAY_BOARD_SIZE.y / 2), pg.Vector2(PADDLE_SIZE))
    ball = Ball(PLAY_BOARD_SIZE / 2, BALL_SIZE, pg.Vector2(5, 0))
    keys = pg.key.get_pressed()
    
    player_1_score = 0
    player_1_score = 0
    
    movement_1_y = 0
    movement_2_y = 0
    
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                if event.key == PLAYER_1_CONTROLLS[0]:
                    movement_1_y = -1
                if event.key == PLAYER_1_CONTROLLS[1]:
                    movement_1_y = 1
                if event.key == PLAYER_2_CONTROLLS[0]:
                    movement_2_y = -1
                if event.key == PLAYER_2_CONTROLLS[1]:
                    movement_2_y = 1
            if event.type == pg.KEYUP:
                if event.key == PLAYER_1_CONTROLLS[0]:
                    movement_1_y = 0
                    player_1.last_movement.y = 0
                if event.key == PLAYER_1_CONTROLLS[1]:
                    movement_1_y = 0
                    player_1.last_movement.y = 0
                if event.key == PLAYER_2_CONTROLLS[0]:
                    movement_2_y = 0
                    player_2.last_movement.y = 0
                if event.key == PLAYER_2_CONTROLLS[1]:
                    movement_2_y = 0
                    player_2.last_movement.y = 0
        
        display.fill(background_color)
        keys=pg.key.get_pressed()
        
        pg.draw.rect(display, foreground_color, (0, SCORE_BOARD_SIZE_Y - 10, WINDOW_SIZE.x, 10))
        
        for i in range(0, int(PLAY_BOARD_SIZE.y / (2 * CENTRAL_LINE_DOTS_SIZE.y)) + 1):
            y = i * (2 * CENTRAL_LINE_DOTS_SIZE.y) + PLAY_BOARD_OFFSET.y
            x = (PLAY_BOARD_SIZE.x / 2) - (CENTRAL_LINE_DOTS_SIZE.x / 2)
            pg.draw.rect(display, foreground_color, (pg.Vector2(x, y), CENTRAL_LINE_DOTS_SIZE))
        
        player_1.position.y += movement_1_y * PLAYER_MOVE_SPEED
        player_1.last_movement.y += movement_1_y * PLAYER_MOVE_SPEED * PLAYER_MOVE_EFFECT_COEF
        
        player_2.position.y += movement_2_y * PLAYER_MOVE_SPEED
        player_2.last_movement.y += movement_2_y * PLAYER_MOVE_SPEED * PLAYER_MOVE_EFFECT_COEF
        
        
        ball.update()
        
        ball.collision(player_1)
        ball.collision(player_2)
        ball.check_walls()
        
        player_1.draw()
        player_2.draw()
        ball.draw()
        pg.display.update()
#        print(clock.get_fps())
        clock.tick(60)
        
main()