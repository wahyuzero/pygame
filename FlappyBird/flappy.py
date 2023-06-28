import pygame
import random

pygame.init()
# Ukuran layar
width = 288
height = 500

# Warna Font
black = (0, 0, 0)
white = (0, 255, 255)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')

bird_images = ['bird1.png', 'bird2.png', 'bird3.png']
birds = []
for image in bird_images:
    bird = pygame.image.load(image).convert_alpha()
    birds.append(bird)

bird_index = 0

# Load gambar background
background_img = pygame.image.load('background.png').convert()

# Load suara background
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.set_volume(0.5)  # Mengatur volume suara latar belakang (misalnya 0.5)

# Load suara melompat
jump_sound = pygame.mixer.Sound('jump_sound.wav')
jump_sound.set_volume(10.5)  # Mengatur volume suara lompat (misalnya 0.2)

# Keadaan burung
bird_state = 'mid'  # mid: diam, up: naik, down: turun

# Load gambar pipa
pipe_img = pygame.image.load('pipe.png').convert_alpha()

# Mengatur kecepatan permainan
clock = pygame.time.Clock()
fps = 60

# Mengatur skor
score_font = pygame.font.Font('freesansbold.ttf', 12)
score = 0
high_score = 0

# Fungsi untuk menggambar burung
def draw_bird(x, y):
    screen.blit(birds[bird_index], (x, y))

# Fungsi untuk menggambar pipa
def draw_pipe(x, y, pipe_bottom, pipe_top):
    screen.blit(pipe_img, (x, y))
    screen.blit(pygame.transform.flip(pipe_img, False, True), (x, pipe_top))
    screen.blit(pygame.transform.flip(pipe_img, False, False), (x, pipe_bottom))

# Fungsi untuk menampilkan skor
def show_score(score):
    score_text = score_font.render(str(score), True, white)
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 50))

# Fungsi untuk menampilkan highscore
def show_high_score(high_score):
    high_score_text = score_font.render("High Score: " + str(high_score), True, white)
    screen.blit(high_score_text, (width - high_score_text.get_width() - 20, 20))  # Posisi highscore di kanan atas

# Fungsi untuk memainkan suara lompat
def play_jump_sound():
    jump_sound.play()

# Fungsi untuk memulai permainan
def game():
    global bird_index, bird_state, score, high_score

    # Koordinat awal burung
    bird_x = 100
    bird_y = height // 2

    bird_drop_speed = 0
    bird_jump = 10

    # Koordinat awal pipa
    pipe_x = width
    pipe_y = random.randint(50, 450)
    pipe_gap = 150
    pipe_speed = 5

    game_over = False

    # Memainkan suara latar belakang
    pygame.mixer.music.play(-1)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_drop_speed = 0
                    bird_drop_speed -= bird_jump
                    bird_state = 'up'
                    play_jump_sound()  # Memainkan suara lompat
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        bird_drop_speed += 1
        bird_y += bird_drop_speed

        # Menggambar elemen game
        screen.blit(background_img, (0, 0))
        draw_pipe(pipe_x, pipe_y, pipe_y + pipe_gap, pipe_y - pipe_gap - 500)
        show_score(score)
        show_high_score(high_score)
        draw_bird(bird_x, bird_y)

        # Memeriksa tabrakan burung dengan pipa
        bird_rect = birds[bird_index].get_rect()
        bird_rect.topleft = (bird_x, bird_y)

        pipe_rect_top = pygame.Rect(pipe_x, pipe_y - pipe_gap - 500, pipe_img.get_width(), pipe_img.get_height())
        pipe_rect_bottom = pygame.Rect(pipe_x, pipe_y + pipe_gap, pipe_img.get_width(), pipe_img.get_height())

        if bird_rect.colliderect(pipe_rect_top) or bird_rect.colliderect(pipe_rect_bottom) or bird_y > height or bird_y < 0:
            game_over = True

            if score > high_score:
                high_score = score

        # Memperbarui posisi pipa
        pipe_x -= pipe_speed

        # Memeriksa jika pipa sudah lewat dan menambahkan skor
        if pipe_x < -pipe_img.get_width():
            pipe_x = width
            pipe_y = random.randint(50, 450)
            score += 1

        # Mengganti gambar burung untuk animasi
        if bird_state == 'up':
            bird_index = 0  # Burung sedang naik
        elif bird_state == 'down':
            bird_index = 1  # Burung sedang turun

        # Memeriksa jika burung sedang turun
        if bird_drop_speed > 0:
            bird_state = 'down'

        pygame.display.update()
        clock.tick(fps)

    # Menghentikan suara latar belakang
    pygame.mixer.music.stop()

    # Pengecekan highscore sebelum memulai permainan baru
    if score > high_score:
        high_score = score

    # Memanggil fungsi choose_bird() untuk memilih burung baru
    choose_bird()
    score = 0  # Reset skor ketika memilih burung

# Fungsi untuk memilih burung
def choose_bird():
    global bird_index, score, high_score
    bird_selected = False

    while not bird_selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    bird_index = (bird_index - 1) % len(birds)
                elif event.key == pygame.K_RIGHT:
                    bird_index = (bird_index + 1) % len(birds)
                elif event.key == pygame.K_SPACE:
                    bird_selected = True
                    score = 0  # Reset skor ketika memilih burung

        screen.fill(black)
        bird_image = birds[bird_index]
        bird_rect = bird_image.get_rect()
        bird_rect.center = (width // 2, height // 2)
        screen.blit(background_img, (0, 0))
        screen.blit(bird_image, bird_rect)
        show_high_score(high_score)
        bird_text = score_font.render("Select Bird", True, white)
        screen.blit(bird_text, (width // 2 - bird_text.get_width() // 2, 50))
        pygame.display.update()
        clock.tick(fps)

# Fungsi untuk menu utama
def main_menu():
    menu_font = pygame.font.Font('freesansbold.ttf', 14)
    menu_selected = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_selected = 0
                elif event.key == pygame.K_DOWN:
                    menu_selected = 1
                elif event.key == pygame.K_SPACE:
                    if menu_selected == 0:
                        choose_bird()
                        score = 0
                        game()
                    elif menu_selected == 1:
                        pygame.quit()
                        quit()

        screen.fill(black)
        screen.blit(background_img, (0, 0))
        title_text = menu_font.render("Flappy Bird", True, white)
        start_text = menu_font.render("Start Game", True, white)
        quit_text = menu_font.render("Quit", True, white)

        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 200))
        if menu_selected == 0:
            pygame.draw.rect(screen, white, (width // 2 - start_text.get_width() // 2 - 10, 300, start_text.get_width() + 20, start_text.get_height()), 3)
        else:
            pygame.draw.rect(screen, white, (width // 2 - start_text.get_width() // 2 - 10, 300, start_text.get_width() + 20, start_text.get_height()), 1)
        screen.blit(start_text, (width // 2 - start_text.get_width() // 2, 300))
        if menu_selected == 1:
            pygame.draw.rect(screen, white, (width // 2 - quit_text.get_width() // 2 - 10, 400, quit_text.get_width() + 20, quit_text.get_height()), 3)
        else:
            pygame.draw.rect(screen, white, (width // 2 - quit_text.get_width() // 2 - 10, 400, quit_text.get_width() + 20, quit_text.get_height()), 1)
        screen.blit(quit_text, (width // 2 - quit_text.get_width() // 2, 400))

        pygame.display.update()
        clock.tick(fps)

# Menjalankan game
main_menu()
