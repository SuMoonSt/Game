import os
import pygame
################################################################
# 기본 초기화 (반드시 필요)
pygame.init() # 초기화 (반드시 필요)

# 화면 크기 설정
screen_width = 640 # 가로 크기
screen_height = 480 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Nado Pang") # 게임 이름

# FPS
clock = pygame.time.Clock()
################################################################

# 1. 사용자 게임 초기화(배경화면, 게임이미지, 좌표, 속도, 폰트 등)

# 배경 이미지 불러오기
current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "images")
background = pygame.image.load(os.path.join(image_path, "background.png"))
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]


# 캐릭터(스프라이트) 불러오기
character = pygame.image.load(os.path.join(image_path, "_character.png"))
character_size = character.get_rect().size # 이미지 크기 구하기
character_width = character_size[0]
character_heigth = character_size[1]
character_x_pos = (screen_width - character_width) / 2  # 화면 가로의 중간
character_y_pos = screen_height - character_heigth - stage_height   # 화면 세로의 가장 아래

# 이동할 좌표
to_x = 0
to_y = 0

# 이동속도
character_speed = 0.6

# 적 enemy 캐릭터
enemy = pygame.image.load("C:/Users/Moon/Desktop/OneMinPython/pygame_basic/enemy.png")
enemy_size = enemy.get_rect().size # 이미지 크기 구하기
enemy_width = enemy_size[0]
enemy_heigth = enemy_size[1]
enemy_x_pos = (screen_width - enemy_width) / 2  # 화면 가로의 중간
enemy_y_pos = (screen_height - enemy_heigth) / 2 # 화면 세로의 가장 아래

# 폰트 정의
game_font = pygame.font.Font(None, 40) # 폰트 객체 생성(폰트, 크기)

# 총 시간
total_time = 10

# 시작 시간
start_ticks = pygame.time.get_ticks() # 현재 tick을 받아옴


# 이벤트 루프
running = True # 게임이 진행중인가?
while running:
    dt = clock.tick(60) # 게임화면의 FPS 설정(보통 30 or 60)
################################################################
    # 2. 이벤트 처리(키보드, 마우스 등)
    for event in pygame.event.get():# 어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가?(ex. X 버튼)
            running = False

        if event.type == pygame.KEYDOWN: # 키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed
            elif event.key == pygame.K_UP:
                to_y -= character_speed
            elif event.key == pygame.K_DOWN:
                to_y += character_speed

        if event.type == pygame.KEYUP: # 방향키를 떼면
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0
################################################################
    # 3. 게임 캐릭터 위치 정의
    character_x_pos += to_x * dt # dt를 곱해주지 않으면 fps에 따라서 게임속도가 차이나게 됨
    character_y_pos += to_y * dt # fps가 낮을수록 프레임이 끊기는 것으로 보임

    # 캐릭터가 화면 밖으로 나가지 않게 하기위한 코드
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width-character_width:
        character_x_pos = screen_width-character_width
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height-character_heigth:
        character_y_pos = screen_height-character_heigth
################################################################
    # 4. 충돌 처리
    # 충돌 처리를 위한 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    # 충돌 체크
    if character_rect.colliderect(enemy_rect):
        print("충돌")
        running = False
################################################################
    # 5. 화면 그리기
    # screen.fill((255,255,255)) # RGB값으로 화면을 채움
    screen.blit(background, (0,0)) # background 그림을 (0,0)에 그려넣음
    screen.blit(stage, (0,screen_height-stage_height))
    screen.blit(character,(character_x_pos,character_y_pos)) # 캐릭터 그리기
    screen.blit(enemy,(enemy_x_pos,enemy_y_pos))

    # 타이머 집어 넣기
    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # 경과 시간(ms)을 1000으로 나누어서 초(s) 단위로 표시
    timer = game_font.render(str(int(total_time - elapsed_time)), True, (255,255,255)) # 출력할 글자, True, 글자 생상
    screen.blit(timer, (10,10))
    if total_time - elapsed_time < 0:
        print("타임아웃")
        running = False

    pygame.display.update() # 게임화면을 다시 그리기(반드시 필요)

pygame.time.delay(2000) # 2초 정도 대기
################################################################
# 6. 종료
pygame.quit()