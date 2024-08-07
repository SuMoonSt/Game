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
pygame.display.set_caption("웅냠냠") # 게임 이름

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
character_speed = 1

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
# 무기 발사 로직
weapons = []
# 무기 이동 속도
weapon_speed = 10

# 공 만들기
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))
]
# 공 크기에 따른 최초 스피드
ball_speed_y = [-18,-15,-12,-9]
# 공들
balls = []
balls.append({
    "pos_x" : 20,
    "pos_y" : 20,
    "img_idx" : 0,
    "to_x" : 3, # x축 이동방향, -3이면 왼쪽으로 3이동
    "to_y" : -6, # y축 이동방향, 6이면 아래쪽으로 6이동
    "init_spd_y" : ball_speed_y[0] # y 최초 속도
})

# 사라질 무기, 공 정보
weapon_to_remove = -1
ball_to_remove = -1

# 폰트 정의
game_font = pygame.font.Font(None, 40) # 폰트 객체 생성(폰트, 크기)
total_time = 100
start_ticks = pygame.time.get_ticks()

#game_result = "Game Over"

# 총 시간
total_time = 100

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
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])


        if event.type == pygame.KEYUP: # 방향키를 떼면
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
################################################################
    # 3. 게임 캐릭터 위치 정의
    character_x_pos += to_x * dt # dt를 곱해주지 않으면 fps에 따라서 게임속도가 차이나게 됨

    # 캐릭터가 화면 밖으로 나가지 않게 하기위한 코드
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width-character_width:
        character_x_pos = screen_width-character_width

    # 무기 위치 조정
    weapons = [ [w[0],w[1] - weapon_speed] for w in weapons]
    #천장에 닿은 무기 없애기
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_x_pos = ball_val["pos_x"]
        ball_y_pos = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]
        # 벽에 닿았을 때 공의 이동방향 전환
        if ball_x_pos < 0 or ball_x_pos > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1
        # 바닥에 닿았을 때 공 속도 초기화
        if ball_y_pos >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else: # 벽에 닿지 않으면 공의 속도가 점점 감소
            ball_val["to_y"] += 0.5
        
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]
################################################################
    # 4. 충돌 처리
    # 충돌 처리를 위한 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
  # 충돌 체크
    for ball_idx, ball_val in enumerate(balls):
        ball_x_pos = ball_val["pos_x"]
        ball_y_pos = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_x_pos
        ball_rect.top = ball_y_pos
        if character_rect.colliderect(ball_rect):
            running = False
            game_result = "Mission Failed"
            break

        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_x_pos, weapon_y_pos = weapon_val[0], weapon_val[1]
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_x_pos
            weapon_rect.top = weapon_y_pos
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx # 충돌한 무기 삭제를 위한 값
                ball_to_remove = ball_idx

                if ball_img_idx < 3: # 가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠주기
                    # 현재 공 정보
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]
                    # 다음 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    balls.append({
                        "pos_x" : ball_x_pos + (ball_width / 2) - (small_ball_width / 2),
                        "pos_y" : ball_y_pos + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx" : ball_img_idx + 1,
                        "to_x" : -3, # x축 이동방향, -3이면 왼쪽으로 3이동
                        "to_y" : -6, # y축 이동방향, 6이면 아래쪽으로 6이동
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1] # y 최초 속도
                    })
                    balls.append({
                        "pos_x" : ball_x_pos + (ball_width / 2) - (small_ball_width / 2),
                        "pos_y" : ball_y_pos + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx" : ball_img_idx + 1,
                        "to_x" : 3, # x축 이동방향, -3이면 왼쪽으로 3이동
                        "to_y" : -6, # y축 이동방향, 6이면 아래쪽으로 6이동
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1] # y 최초 속도
                    })
                break
        else:
            continue
        break
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 모든 공을 없앤경우
    if len(balls) == 0:
        game_result = "Misson Complete"
        running = False

################################################################
    # 5. 화면 그리기
    # screen.fill((255,255,255)) # RGB값으로 화면을 채움
    screen.blit(background, (0,0)) # background 그림을 (0,0)에 그려넣음
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    for idx, val in enumerate(balls):
        ball_x_pos, ball_y_pos, ball_img_idx = val["pos_x"], val["pos_y"], val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_x_pos, ball_y_pos))
    screen.blit(stage, (0,screen_height-stage_height))
    screen.blit(character,(character_x_pos,character_y_pos)) # 캐릭터 그리기



    # 타이머 집어 넣기
    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # 경과 시간(ms)을 1000으로 나누어서 초(s) 단위로 표시
    timer = game_font.render("Time : {} ".format(int(total_time - elapsed_time)), True, (255,255,255)) # 출력할 글자, True, 글자 생성
    screen.blit(timer, (10,10))

    # 시간 초과
    if total_time - elapsed_time < 0:
        game_result = "Time Over"
        running = False

    pygame.display.update() # 게임화면을 다시 그리기(반드시 필요)

# 게임 오버 메시지
msg = game_font.render(game_result, True, (255,255,0))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)

pygame.display.update()

pygame.time.delay(2000) # 2초 정도 대기
################################################################
# 6. 종료
pygame.quit()