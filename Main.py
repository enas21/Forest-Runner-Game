from pygame import Rect

WIDTH = 1000
HEIGHT = 667
TITLE = "Forest Runner"

GRAVITY = 0.7
TARGET_SCORE = 5

PLAYER_START_X = 0
PLAYER_START_Y = 300
FLOOR_Y = 560

game_state = "menu"
sound_on = True
score = 0
music_started = False


class AnimatedSprite:
    def __init__(self, x, y, idle_frames, move_frames, rect_w, rect_h):
        self.x = x
        self.y = y
        self.idle_frames = idle_frames
        self.move_frames = move_frames
        self.image = idle_frames[0]
        self.frame_index = 0
        self.timer = 0
        self.is_moving = False
        self.rect_w = rect_w
        self.rect_h = rect_h

    def animate(self):
        self.timer += 1
        if self.timer >= 10:
            self.timer = 0
            if self.is_moving:
                self.frame_index = (self.frame_index + 1) % len(self.move_frames)
                self.image = self.move_frames[self.frame_index]
            else:
                self.frame_index = (self.frame_index + 1) % len(self.idle_frames)
                self.image = self.idle_frames[self.frame_index]

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def get_ground_rect(self):
        # lower body for slime collision
        return Rect((self.x +145 , self.y + 155), (50, 120))

    def get_air_rect(self):
        # upper body for fly collision
        return Rect((self.x + 145, self.y + 50), (50, 120))


class Player(AnimatedSprite):
    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            ["player_idle1", "player_idle2"],
            ["player_run1", "player_run2", "player_run3"],
            64, 64
        )
        self.speed = 5
        self.vx = 0
        self.vy = 0
        self.jump_power = -13
        self.lives = 3
        self.hit_cooldown = 0

    def move(self):
        self.vx = 0
        self.is_moving = False

        if keyboard.left:
            self.vx = -self.speed
            self.is_moving = True

        if keyboard.right:
            self.vx = self.speed
            self.is_moving = True

        self.x += self.vx

        self.vy += GRAVITY
        self.y += self.vy

        if self.y >= PLAYER_START_Y:
            self.y = PLAYER_START_Y
            self.vy = 0

        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.rect_w:
            self.x = WIDTH - self.rect_w

        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

    def jump(self):
        if self.y >= PLAYER_START_Y:
            self.vy = self.jump_power

    def get_rect(self):
        # tight body box for the player image
        return Rect((self.x + 18, self.y + 12), (28, 50))


class Enemy(AnimatedSprite):
    def __init__(self, x, y, idle_frames, move_frames, left_limit, right_limit, speed, rect_w, rect_h):
        super().__init__(x, y, idle_frames, move_frames, rect_w, rect_h)
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.speed = speed
        self.direction = 1

    def move(self):
        self.is_moving = True
        self.x += self.speed * self.direction

        if self.x <= self.left_limit or self.x >= self.right_limit:
            self.direction *= -1

    def get_rect(self):
        if "slime" in self.image:
            # collide box a little lower to really touches the player ground box
            return Rect((self.x , self.y  ), (100, 66))

        elif "fly" in self.image:
            # fly box larger and centered in the bird body
            return Rect((self.x+ 45 , self.y + 40), (70, 50))

        return Rect((self.x, self.y), (self.rect_w, self.rect_h))


class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        screen.blit("coin", (self.x, self.y))

    def get_rect(self):
        return Rect((self.x + 10, self.y + 10), (28, 30))


player = Player(PLAYER_START_X, PLAYER_START_Y)

slime = Enemy(
    250,
    FLOOR_Y - 33,
    ["slime_idle1", "slime_idle2"],
    ["slime_move1", "slime_move2"],
    220,
    450,
    2,
    50,
    33
)

fly_enemy = Enemy(
    650,
    200,
    ["fly_idle", "fly_idle"],
    ["fly_move", "fly_move"],
    600,
    850,
    3,
    128,
    128
)

coins = [
    Coin(220, 500),
    Coin(320, 470),
    Coin(460, 520),
    Coin(620, 480),
    Coin(800, 500)
]

start_button = Rect((380, 220), (240, 60))
sound_button = Rect((380, 310), (240, 60))
exit_button = Rect((380, 400), (240, 60))


def play_music():
    global music_started
    if sound_on and not music_started:
        music.play("background")
        music.set_volume(0.4)
        music_started = True


def stop_music():
    global music_started
    music.stop()
    music_started = False


def reset_game():
    global score, coins
    score = 0

    player.x = PLAYER_START_X
    player.y = PLAYER_START_Y
    player.vx = 0
    player.vy = 0
    player.lives = 3
    player.hit_cooldown = 0

    slime.x = 250
    slime.y = FLOOR_Y - 33
    slime.direction = 1

    fly_enemy.x = 650
    fly_enemy.y = 200
    fly_enemy.direction = 1

    coins = [
        Coin(200, 500),
        Coin(320, 470),
        Coin(460, 520),
        Coin(620, 480),
        Coin(800, 500)
    ]


def draw():
    screen.clear()
    screen.blit("background", (0, 0))

    if game_state == "menu":
        screen.draw.filled_rect(start_button, (60, 160, 60))
        screen.draw.filled_rect(sound_button, (60, 90, 180))
        screen.draw.filled_rect(exit_button, (180, 60, 60))

        screen.draw.text("FOREST RUNNER", center=(500, 120), fontsize=48, color="white")
        screen.draw.text("Start Game", center=start_button.center, fontsize=30, color="white")
        screen.draw.text(f"Sound: {'On' if sound_on else 'Off'}", center=sound_button.center, fontsize=28, color="white")
        screen.draw.text("Exit", center=exit_button.center, fontsize=30, color="white")

    elif game_state == "play":
        player.draw()
        slime.draw()
        fly_enemy.draw()

        for coin in coins:
            coin.draw()

        screen.draw.text(f"Score: {score}/{TARGET_SCORE}", (20, 20), fontsize=32, color="white")
        screen.draw.text(f"Lives: {player.lives}", (20, 55), fontsize=32, color="white")
        screen.draw.text("Arrows = move   Space = jump", (20, 90), fontsize=26, color="white")

        # collision boxes for testing
        #screen.draw.rect(player.get_ground_rect(), "green")
        #screen.draw.rect(player.get_air_rect(), "cyan")
        #screen.draw.rect(slime.get_rect(), "red")
        #screen.draw.rect(fly_enemy.get_rect(), "yellow")
        #for coin in coins:
            #screen.draw.rect(coin.get_rect(), "white")

    elif game_state == "win":
        screen.draw.text("YOU WIN!", center=(500, 250), fontsize=60, color="yellow")
        screen.draw.text("Press ENTER to return to menu", center=(500, 330), fontsize=28, color="white")

    elif game_state == "lose":
        screen.draw.text("GAME OVER", center=(500, 250), fontsize=60, color="red")
        screen.draw.text("Press ENTER to return to menu", center=(500, 330), fontsize=28, color="white")


def update():
    global game_state, score

    if sound_on and not music_started:
        play_music()

    if game_state != "play":
        return

    player.move()
    slime.move()
    fly_enemy.move()

    player.animate()
    slime.animate()
    fly_enemy.animate()

    ground_rect = player.get_ground_rect()
    air_rect = player.get_air_rect()

    slime_rect = slime.get_rect()
    fly_rect = fly_enemy.get_rect()

    for coin in coins[:]:
        if ground_rect.colliderect(coin.get_rect()) or air_rect.colliderect(coin.get_rect()):
            coins.remove(coin)
            score += 1
            if sound_on:
                sounds.coin.play()

    if player.hit_cooldown == 0:
        hit_slime = ground_rect.colliderect(slime_rect)
        hit_fly = air_rect.colliderect(fly_rect)

        if hit_slime or hit_fly:
            player.lives -= 1
            player.x = PLAYER_START_X
            player.y = PLAYER_START_Y
            player.vx = 0
            player.vy = 0
            player.hit_cooldown = 45

            if sound_on:
                sounds.hit.play()

    if score >= TARGET_SCORE:
        game_state = "win"
        stop_music()
        if sound_on:
            sounds.win.play()

    if player.lives <= 0:
        game_state = "lose"
        stop_music()
        if sound_on:
            sounds.lose.play()


def on_key_down(key):
    global game_state

    if game_state == "play" and key == keys.SPACE:
        player.jump()

    elif game_state in ["win", "lose"] and key == keys.RETURN:
        reset_game()
        game_state = "menu"
        play_music()


def on_mouse_down(pos):
    global game_state, sound_on

    if game_state != "menu":
        return

    if start_button.collidepoint(pos):
        reset_game()
        game_state = "play"

    elif sound_button.collidepoint(pos):
        sound_on = not sound_on
        if sound_on:
            play_music()
        else:
            stop_music()

    elif exit_button.collidepoint(pos):
        quit()