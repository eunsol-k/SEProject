import pygame
import setting

pygame.init()

# Set the window size and caption
WINDOW_SIZE = setting.get_screen(setting.get_screen_num())
pygame.display.set_caption("Test")
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)

# Set font
font = pygame.font.Font(None, 40)
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 205, 18)

# global 변수 설정
DIFFICULTY = int(setting.get_difficulty_num())
SOUND = bool(setting.get_sound_bool())
SCREEN = int(setting.get_screen_num())
COLORBLIND = bool(setting.get_colorblind_bool())
screen_size = setting.get_screen(SCREEN)

# setting option list
options = setting.get_mod_list() + ['Set Control', 'rollback', 'save', 'exit']
options_control = setting.get_control_list() + ['rollback', 'save', 'back']
initial_control = setting.get_control_list_all()
selected_option = 0

# Main loop
menu_flag = True # 메인 화면
control_flag = False # 사용자 커스터마이징 입력 키 화면

# setting 텍스트 정렬
def get_common_option_rec(option_text, is_option):
    option_rect = option_text.get_rect()
    if is_option:
        option_rect.center = (screen.get_width()/3, screen.get_height()/7 + i * 45)
        option_rect.left = screen.get_width()/4
    else:
        option_rect.center = (screen.get_width()/2, screen.get_height()/7 + i * 45)
        option_rect.right = screen.get_width() - screen.get_width()/4
    return option_rect

def change_process(option, is_next):
    flag = True
    if option == 0:
        global DIFFICULTY
        if is_next:
            if DIFFICULTY < 2:
                DIFFICULTY = DIFFICULTY + 1
            else:
                DIFFICULTY = 0
        else:
            if DIFFICULTY != 0:
                DIFFICULTY = DIFFICULTY - 1
            else:
                DIFFICULTY = 2
        setting.set_difficulty(DIFFICULTY)
    elif option == 1:
        global SOUND
        if SOUND:
            SOUND = False
        else:
            SOUND = True
        setting.set_sound(SOUND)
    elif option == 2:
        global SCREEN
        if is_next:
            if SCREEN < 2:
                SCREEN = SCREEN + 1
            else:
                SCREEN = 0
        else:
            if SCREEN != 0:
                SCREEN = SCREEN - 1
            else:
                SCREEN = 2
        setting.set_screen(SCREEN)
    elif option == 3:
        global COLORBLIND
        if COLORBLIND:
            COLORBLIND = False
        else:
            COLORBLIND = True
        setting.set_colorblind(COLORBLIND)
    return flag

def menu_process(option, is_next, is_enter, is_option):
    global control_flag
    mod_len = len(setting.get_mod_list())
    flag = True
    if option < mod_len and not is_option:
        if not control_flag:
            change_process(option, is_next)
    elif option == mod_len:
        if is_enter:
            print("set control")
            control_flag = True
    elif option == (mod_len + 1):
        if is_enter:
            print("set rollback")
            setting.mod_back()
    elif option == (mod_len + 2):
        if is_enter:
            print("save mod setting")
            setting.save()
    elif option == (mod_len + 3):
        if is_enter:
            print("menu exit")
            flag = False
    return flag

def change_control_process(option, value, is_clicked):
    global initial_control
    if not is_clicked:
        initial_control[0][option] = pygame.key.name(value) # 문자 저장
        initial_control[1][option] = value # 수 저장

def control_process(option, value, is_clicked):
    global control_flag
    global initial_control
    control_len = len(setting.get_control_list())
    flag = True
    if option < control_len:
        if control_flag:
            change_control_process(option, value, is_clicked)
    elif option == control_len:
        if((value == setting.get_keymap_check()) or is_clicked):
            print("set rollback")
            setting.control_back()
            initial_control = setting.get_control_list_all()
    elif option == (control_len + 1):
        if((value == setting.get_keymap_check()) or is_clicked):
            print("save control setting")
            for i, value in enumerate(initial_control[1]):
                setting.set_keymap_by_index(i, value)
            setting.save()
    else:
        if((value == setting.get_keymap_check()) or is_clicked):
            print("back to setting menu")
            flag = False
    return flag

while menu_flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_flag = False
        elif event.type == pygame.KEYDOWN:
            if not control_flag:
                # 모드 설정
                if event.key == setting.get_keymap_up():
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == setting.get_keymap_down():
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == setting.get_keymap_check():
                    menu_flag = menu_process(selected_option, True, True, False)
                elif event.key == setting.get_keymap_right():
                    menu_flag = menu_process(selected_option, True, False, False)
                elif event.key == setting.get_keymap_left():
                    menu_flag = menu_process(selected_option, False, False, False)
            else:
                # 키 설정
                if event.key == setting.get_keymap_up():
                    selected_option = (selected_option - 1) % len(options_control)
                elif event.key == setting.get_keymap_down():
                    selected_option = (selected_option + 1) % len(options_control)
                else:
                    print("event.key : ", event.key)
                    control_flag = control_process(selected_option, event.key, False)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if control_flag:
                option_list = options_control
            else:
                option_list = options
            for i, option in enumerate(option_list):
                # 선택된 옵션 처리
                option_text = font.render(option, True, white)
                option_rect = get_common_option_rec(option_text, True)
                if control_flag:
                    if i < len(setting.get_control_list()):
                        value_text = font.render(initial_control[0][i], True, white)
                    else:
                        value_text = font.render('', True, white)
                else:
                    value_text = font.render(setting.get_mod_all(i), True, white)
                value_rect = get_common_option_rec(value_text, False)

                if option_rect.collidepoint(mouse_pos):
                    selected_option = i
                    if not control_flag:
                        menu_flag = menu_process(selected_option, True, True, True)
                    else:
                        control_flag = control_process(selected_option, 0, True)
                if value_rect.collidepoint(mouse_pos):
                    selected_option = i
                    if not control_flag:
                        menu_flag = change_process(selected_option, True)
                    else:
                        control_flag = control_process(selected_option, 0, True)
    
    # 메뉴 화면 그리기
    screen.fill(black)
    if control_flag:
        option_list = options_control
    else:
        option_list = options

    for i, option in enumerate(option_list):
        # options 출력
        if i == selected_option:
            option_text = font.render(option, True, yellow)
        else:
            option_text = font.render(option, True, white)
        option_rect = get_common_option_rec(option_text, True)
        screen.blit(option_text, option_rect)

        #options value 출력
        if control_flag:
            if i < len(setting.get_control_list()):
                value_text = font.render(initial_control[0][i], True, white)
            else:
                value_text = font.render('', True, white)
        else:
            value_text = font.render(setting.get_mod_all(i), True, white)
        value_rect = get_common_option_rec(value_text, False)
        screen.blit(value_text, value_rect)
    pygame.display.flip()

pygame.quit()
