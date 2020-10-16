import pygame as pg
import numpy as np

SCORE_BOARD_SIZE_Y = 100
SCORE_DISPLAY_OFFSET = 200

BALL_SIZE = pg.Vector2(10, 10)
PADDLE_SIZE = pg.Vector2(10, 50)
WINDOW_SIZE = pg.Vector2(800, 600)
PLAY_BOARD_OFFSET = pg.Vector2(0, SCORE_BOARD_SIZE_Y)
PLAY_BOARD_SIZE = WINDOW_SIZE - PLAY_BOARD_OFFSET

BALL_SPEED = 5

CENTRAL_LINE_DOTS_SIZE = pg.Vector2(3, 7)

display = pg.display.set_mode((int(WINDOW_SIZE.x), int(WINDOW_SIZE.y)))
background_color = (0, 0, 0)
foreground_color = (255, 255, 255)

pg.display.flip()

pg.display.set_caption('Pong')
display.fill(background_color)
    
pg.display.update()

PLAYER_1_CONTROLLS = (pg.K_w, pg.K_s)
PLAYER_2_CONTROLLS = (pg.K_UP, pg.K_DOWN)
PLAYER_MOVE_SPEED = 5
PLAYER_MOVE_EFFECT_COEF = .2

WINNING_SCORE = 5

clock = pg.time.Clock()
pg.font.init()

big_font = pg.font.SysFont("Consolas", 90)
small_font = pg.font.SysFont("Consolas", 40)

class Paddle:
    movement_y = 0
    position = pg.Vector2()
    size = pg.Vector2()
    last_movement = pg.Vector2()
    
    def __init__(self, position, size):
        self.position = pg.Vector2(position.x, position.y)
        self.size[:] = size.x, size.y
    
    def draw(self):
        pg.draw.rect(display, foreground_color, (self.position - (.5 * self.size) + PLAY_BOARD_OFFSET, self.size))
    
    def check_walls(self):
        if(self.position.y < self.size.y / 2):
            self.position.y = self.size.y / 2
            self.last_movement.y = 0
        if(self.position.y > PLAY_BOARD_SIZE.y - self.size.y / 2):
            self.position.y = PLAY_BOARD_SIZE.y - self.size.y / 2
            self.last_movement.y = 0
    def handle_input(self, event, player_controlls):
        if event.type == pg.KEYDOWN:
            if event.key == player_controlls[0]:
                self.movement_y = -1
            if event.key == player_controlls[1]:
                self.movement_y = 1
        if event.type == pg.KEYUP:
            if event.key == player_controlls[0]:
                self.movement_y = 0
                self.last_movement.y = 0
            if event.key == player_controlls[1]:
                self.movement_y = 0
                self.last_movement.y = 0
    
    def update(self):
        self.position.y += self.movement_y * PLAYER_MOVE_SPEED
        self.last_movement.y += self.movement_y * PLAYER_MOVE_SPEED * PLAYER_MOVE_EFFECT_COEF

class Ball:
    position = pg.Vector2()
    size = pg.Vector2()
    velocity = pg.Vector2()
    
    def __init__(self, position, size, velocity):
        self.position[:] = position.x, position.y
        self.size[:] = size.x, size.y
        self.velocity[:] = velocity.x, velocity.y
    
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
#            self.velocity.scale_to_length(BALL_SPEED)
    
    def check_walls(self):
        if(self.position.y < 0 + self.size.y / 2) :
            self.position.y = self.size.y / 2
            self.velocity.y = -self.velocity.y
        if(self.position.y > PLAY_BOARD_SIZE.y - self.size.y / 2) :
            self.position.y = PLAY_BOARD_SIZE.y - self.size.y / 2
            self.velocity.y = - self.velocity.y
    
    def check_for_point(self, reset_position):
        if(self.position.x < 0 + self.size.x / 2) :
            self.position = reset_position
            self.velocity[:] = BALL_SPEED, 0
            return 2
        if(self.position.x > PLAY_BOARD_SIZE.x - self.size.x / 2):
            self.position = reset_position
            self.velocity[:] = -BALL_SPEED, 0
            return 1
        return 0
    
def game() :
    
    player_1 = Paddle(pg.Vector2(30, PLAY_BOARD_SIZE.y / 2), pg.Vector2(PADDLE_SIZE))
    player_2 = Paddle(pg.Vector2(PLAY_BOARD_SIZE.x - 30, PLAY_BOARD_SIZE.y / 2), pg.Vector2(PADDLE_SIZE))
    ball = Ball(PLAY_BOARD_SIZE / 2, BALL_SIZE, pg.Vector2(BALL_SPEED, 0))
    
    player_1_score = 0
    player_2_score = 0
    
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    exit()
            player_1.handle_input(event, PLAYER_1_CONTROLLS)
            player_2.handle_input(event, PLAYER_2_CONTROLLS)
        
        display.fill(background_color)
        keys=pg.key.get_pressed()
        
        pg.draw.rect(display, foreground_color, (0, SCORE_BOARD_SIZE_Y - 10, WINDOW_SIZE.x, 10))
        
        for i in range(0, int(PLAY_BOARD_SIZE.y / (2 * CENTRAL_LINE_DOTS_SIZE.y)) + 1):
            y = i * (2 * CENTRAL_LINE_DOTS_SIZE.y) + PLAY_BOARD_OFFSET.y
            x = (PLAY_BOARD_SIZE.x / 2) - (CENTRAL_LINE_DOTS_SIZE.x / 2)
            pg.draw.rect(display, foreground_color, (pg.Vector2(x, y), CENTRAL_LINE_DOTS_SIZE))
        
        
        player_1.update()
        player_2.update()
        
        ball.update()
        
        player_1.check_walls()
        player_2.check_walls()
        
        ball.collision(player_1)
        ball.collision(player_2)
        ball.check_walls()
        result = ball.check_for_point(PLAY_BOARD_SIZE * 0.5)
        
        if result:
            if(result == 1):
                player_1_score += 1
            if(result == 2):
                player_2_score += 1
            #print( str(player_1_score) + " " + str(player_2_score))
            player_1 = Paddle(pg.Vector2(30, PLAY_BOARD_SIZE.y / 2), pg.Vector2(PADDLE_SIZE))
            player_2 = Paddle(pg.Vector2(PLAY_BOARD_SIZE.x - 30, PLAY_BOARD_SIZE.y / 2), pg.Vector2(PADDLE_SIZE))
        
        if(player_1_score == WINNING_SCORE or player_2_score == WINNING_SCORE):
            return (player_1_score, player_2_score)
        
        text_surface_1 = big_font.render(str(player_1_score), False, foreground_color)
        display.blit(text_surface_1, (WINDOW_SIZE.x / 2 - SCORE_DISPLAY_OFFSET,0))
        
        text_surface_2 = big_font.render(str(player_2_score), False, foreground_color)
        display.blit(text_surface_2, (WINDOW_SIZE.x / 2 + SCORE_DISPLAY_OFFSET,0))
        
        
        player_1.draw()
        player_2.draw()
        ball.draw()
        pg.display.update()
        clock.tick(60)



is_waiting = True
while is_waiting:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                exit()
            if event.key == pg.K_SPACE:
                is_waiting = False
    display.fill(background_color)
    message_1_surface = big_font.render("PONG", False, foreground_color)
    display.blit(message_1_surface, (WINDOW_SIZE / 2 + pg.Vector2(-100, -75)))
    message_2_surface = small_font.render("press \"space\" to start", False, foreground_color)
    display.blit(message_2_surface, (WINDOW_SIZE / 2 + pg.Vector2(-240, 50)))
    pg.display.update()

while(True):
    (s1, s2) = game()
    is_waiting = True
    while is_waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    exit()
                if event.key == pg.K_SPACE:
                    is_waiting = False
        display.fill(background_color)
        pg.draw.rect(display, background_color, (0, SCORE_BOARD_SIZE_Y - 10, WINDOW_SIZE.x, WINDOW_SIZE.y))
        win_message_surface = big_font.render("Player " + ("1" if s1 > s2 else "2") + " Won!", False, foreground_color)
        display.blit(win_message_surface, (WINDOW_SIZE / 2 + pg.Vector2(-300, -45)))
        message_2_surface = small_font.render("press \"space\" to restart", False, foreground_color)
        display.blit(message_2_surface, (WINDOW_SIZE / 2 + pg.Vector2(-260, 50)))
        pg.display.update()