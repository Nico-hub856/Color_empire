import pygame as pg
import random
import time
from os import path

game = True
party_num = 1
players = 0

while game:
    
    running = False  
    gameover = False
    choose = True
    start = True

    
    GREEN = (204, 255, 153)
    GREEN2 = (20, 170, 0)
    BLUE = (0, 0, 255)
    YELLOW = (250, 250, 51)
    BEIGE = (217, 179, 130)
    BLACK = (0, 0, 0)
    RED = (200,0,0)
    WHITE = (255, 255, 255)
    BROWN = (255, 153, 51)
    FPS = 25
    WIDTH = 1023
    HEIGHT = 768

    pg.init()
    pg.mixer.init()
    pg.joystick.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Color empire")
    #screen = pg.display.set_mode((WIDTH, HEIGHT),pg.FULLSCREEN)
    clock = pg.time.Clock()

    font = path.join("font", "FONT.TTF")


    nb_joysticks = pg.joystick.get_count()

    try:
        joystick0 = pg.joystick.Joystick(0)
        joystick0.init()
        joystick1 = pg.joystick.Joystick(1)
        joystick1.init()
    except:
        pass

    running =True
    score1 = 0
    score2 = 0
    round_time = 20
    x_pos = 0
    y_pos = 0
    x_pos1 = 0
    y_pos1 = 0
    last_sec = 0
    index = 0
    score_for_calculs1 = 0
    score_for_calculs2 = 0

    map_world = []

    for i in range(391):
        map_world.append("0")
        
    def player2_draw(x_pos,y_pos):
        lagX = (x_pos*41)+42
        lagY = (y_pos*41)+42
        pg.draw.rect(screen, GREEN2, (1+lagX, 1+lagY, 41, 41))

    def player1_draw(x_pos,y_pos):
        lagX = (x_pos*41)+42
        lagY = (y_pos*41)+42
        pg.draw.rect(screen, RED, (1+lagX, 1+lagY, 41, 41))
        
    def draw_map(map_object):
        for i in range(17):
            for j in range(23):
                case_num = (i*23)+j
                if map_object[case_num] == "0":
                    color = WHITE
                    pg.draw.rect(screen, color, (43+j*41, 43+i*41, 41, 41)) 

    def update_score(map_object):
        global score_for_calculs1, score_for_calculs2
        score_for_calculs1 = 0
        score_for_calculs2 = 0
        for i in range(17):
            for j in range(23):
                case_num = (i*23)+j
                if map_object[case_num] == "1":
                    score_for_calculs1 += 1
                elif map_object[case_num] == "2":
                    score_for_calculs2 += 1
                
                
    def draw_objects(map_object):
        for i in range(17):
            for j in range(23):
                case_num = (i*23)+j
                if map_object[case_num] == "1":
                    player1_draw(j,i)
                elif map_object[case_num] == "2":
                    player2_draw(j,i)

    def count(map_object):
        score1 = 0
        score2 = 0
        for i in range(17):
            for j in range(23):
                case_num = (i*23)+j
                if map_object[case_num] == "1":
                    score1 += 1
                elif map_object[case_num] == "2":
                    score2 += 1
                    
    def draw_cursor(x_pos, y_pos):
        pg.draw.rect(screen, (250, 0, 0),(43+x_pos*41, 43+y_pos*41, 41, 41), 5)
    def draw_cursor2(x_pos1, y_pos1):
        pg.draw.rect(screen, (0, 100, 0),(43+x_pos1*41, 43+y_pos1*41, 41, 41), 5)
        
    def draw_text(text, font_name, size, color, x, y):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        screen.blit(text_surface, text_rect)
       
    def show_menu_screen():
        global gameover, running, score_memo1, score_memo2, party_num
        start = True
        select = 1
        while start:
            screen.fill(WHITE)
            if party_num > 1 and players > 1:
                if score_memo1 > score_memo2:
                    draw_text("PLAYER 1 WINS!", font ,60, RED,WIDTH/2 , 180 - 40)
                elif score_memo1 < score_memo2:
                    draw_text("PLAYER 2 WINS!", font ,60, GREEN2,WIDTH/2 , 180 - 40)
                elif score_memo1 == score_memo2:
                    draw_text("EQUALITY!", font ,60, BLACK,WIDTH/2 , 180 - 40)
                if select == 1:
                    draw_text("> Replay <", font ,60, BLACK,WIDTH/2 , HEIGHT / 2 - 40)
                    draw_text("Quit", font ,60, BLACK,WIDTH/2 , HEIGHT / 2 + 40)
                
            if select == 1:
                if party_num == 1:
                    draw_text("Color empire", font ,60, BLACK,WIDTH/2 , 180 - 40)
                if party_num > 1:
                    draw_text("> Replay <", font ,60, BLACK,WIDTH/2 , HEIGHT / 2 - 40)
                else:
                    draw_text("> Play <", font ,60, BLACK,WIDTH/2 , HEIGHT / 2 - 40)
                draw_text("Quit", font ,60, BLACK,WIDTH/2 , HEIGHT / 2 + 40)
                try:
                    if joystick0.get_button(1)==1:
                        start = False
                        running = False
                    if joystick1.get_button(1)==1:
                        start = False
                        running = False
                except:
                    pass
                    
            else:
                draw_text("> Quit <", font ,60, BLACK,WIDTH/2 , HEIGHT / 2 + 40)
                if party_num == 1:
                    draw_text("WHITEBOARD", font ,60, BLACK,WIDTH/2 , 180 - 40)
                    draw_text("Play", font ,60, BLACK,WIDTH/2 , HEIGHT / 2 - 40)
                if party_num > 1:
                    draw_text("Replay", font ,60, BLACK,WIDTH/2 , HEIGHT / 2 - 40)
                try:
                    if joystick0.get_button(1)==1:                    
                        pg.quit()
                    if joystick1.get_button(1)==1:                    
                        pg.quit()
                except:
                    pass
            for event in pg.event.get():
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                    if event.key == pg.K_UP:
                        select += 1
                    if event.key == pg.K_DOWN:
                        select -= 1
            try:
                axis1 = joystick0.get_axis(1)
                if axis1 > 0.5:
                    if select < 2:
                        select += 1
                    time.sleep(0.03)
                if axis1 < -0.5:
                    if select > 1:
                        select -= 1
                    time.sleep(0.03)
            except:
                pass
            try:
                axis2 = joystick1.get_axis(1)
                if axis2 > 0.5:
                    if select < 2:
                        select += 1
                    time.sleep(0.03)
                if axis2 < -0.5:
                    if select > 1:
                        select -= 1
                    time.sleep(0.03)
            except:
                pass
            pg.display.update()
            pg.display.flip()
            
        
    def choose_screen():
        global gameover, running, players, nb_joysticks
        choose = True
        select = 1
        last_click = 20
        while choose:
            screen.fill(WHITE)
            last_click -= 1
            if last_click <= 0:
                if select == 1:
                    draw_text("Number of players...", font ,60, BLACK,WIDTH/2 , 180 - 40)
                    draw_text("> 1 player <", font ,60, BLACK,WIDTH/2 , HEIGHT / 2 - 40)
                    draw_text("2 player", font ,60, BLACK,WIDTH/2 , HEIGHT / 2 + 40)
                    try:
                        if joystick0.get_button(1)==1:
                            if nb_joysticks >= 1:
                                choose = False
                                players = 1
                        
                            else:
                                draw_text("Not enought joysticks!", font ,40, RED,WIDTH/2 , HEIGHT / 2 + 120)
                        if joystick1.get_button(1)==1:
                            if nb_joysticks >= 1:
                                choose = False
                                players = 1
                            else:
                                draw_text("Not enought joysticks!", font ,40, RED,WIDTH/2 , HEIGHT / 2 + 120)
                    except:
                        pass
                        
                else:
                    draw_text("Number of players...", font ,60, BLACK,WIDTH/2 , 180 - 40)
                    draw_text("1 player", font ,60, BLACK,WIDTH/2 , HEIGHT / 2 - 40)
                    draw_text("> 2 player <", font ,60, BLACK,WIDTH/2 , HEIGHT / 2 + 40)
                    try:
                        if joystick0.get_button(1)==1:
                            if nb_joysticks >= 2:
                                choose = False
                                players = 2
                            else:
                                draw_text("Not enought joysticks!", font ,40, RED,WIDTH/2 , HEIGHT / 2 + 120)
                    except:
                        pass
                    try:
                        if joystick1.get_button(1)==1:
                            if nb_joysticks >= 2:
                                choose = False
                                players = 2
                            else:
                                draw_text("Not enought joysticks!", font ,40, RED,WIDTH/2 , HEIGHT / 2 + 120)
                    except:
                        pass
            for event in pg.event.get():
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
            try:
                axis1 = joystick0.get_axis(1)
                if axis1 > 0.5:
                    if select == 1:
                        select += 1
                    time.sleep(0.03)
                if axis1 < -0.5:
                    if select == 2:
                        select -= 1
                    time.sleep(0.03)
            except:
                pass
            try:
                axis2 = joystick1.get_axis(1)
                if axis2 > 0.5:
                    if select == 1:
                        select += 1
                    time.sleep(0.03)
                if axis2 < -0.5:
                    if select == 2:
                        select -= 1
                    time.sleep(0.03)
            except:
                pass
            pg.display.update()
            pg.display.flip()
 
        
    if party_num == 1:
        show_menu_screen()
        choose_screen()
        party_num += 1
    else:
        show_menu_screen()
        
    running = True
    while running:
        clock.tick(FPS)
        index = 0
        
        now = pg.time.get_ticks()
        if now - last_sec >= 1000:
            last_sec = now
            round_time -= 1
            
        def events():
            global x_pos, y_pos, index
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        
        try:
            axis0 = joystick0.get_axis(0)
            axis1 = joystick0.get_axis(1)
        except:
            pass
        try:
            if joystick0.get_button(1)==1:
                index = (y_pos*23)+x_pos
                map_world[index]="1"
                
            if axis1 > 0.5:
                if y_pos < 16:
                    y_pos += 1
            if axis1 < -0.5:
                if y_pos > 0:
                    y_pos -= 1
            if axis0 > 0.5:
                if x_pos < 22:
                    x_pos += 1
            if axis0 < -0.5:
                if x_pos > 0:
                    x_pos -= 1
            if players == 2:    
                if joystick1.get_button(1)==1:
                    index = (y_pos1*23)+x_pos1
                    map_world[index]="2"
                    
                axis0 = joystick1.get_axis(0)
                axis1 = joystick1.get_axis(1)
                if axis1 > 0.5:
                    if y_pos1 < 16:
                        y_pos1 += 1
                if axis1 < -0.5:
                    if y_pos1 > 0:
                        y_pos1 -= 1
                if axis0 > 0.5:
                    if x_pos1 < 22:
                        x_pos1 += 1
                if axis0 < -0.5:
                    if x_pos1 > 0:
                        x_pos1 -= 1
        except:
            pass
        
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    
        keystate = pg.key.get_pressed()
        
        
        screen.fill(BLACK)
        
        #pg.draw.rect(screen, (20, 20, 120),(43, 43, 1280 , 560 ))
        draw_map(map_world)
        update_score(map_world)
        score1 = score_for_calculs1
        score2 = score_for_calculs2
        
        dir = path.dirname(__file__)
        fichier = open("highscore.txt",'r')
        highscore = fichier.read()
        fichier.close()
        draw_objects(map_world)
        count(map_world)
        score_memo1 = score1
        score_memo2 = score2
        if players == 1:
            draw_cursor(x_pos, y_pos)
        else:
            draw_cursor2(x_pos1, y_pos1)
            draw_cursor(x_pos, y_pos)
        if players == 2:
            draw_text(str(score1), font ,80, (255, 0, 0),230, HEIGHT - 150)            
            draw_text(str(score2), font ,80, (0, 100, 0),WIDTH - 230, HEIGHT - 150)
        else:
            draw_text(str(score1), font ,80, (255, 0, 0),WIDTH / 2, 42)
        if round_time >= 0:
            draw_text(str(round_time), font ,80, (0, 0, 0),WIDTH/2 , HEIGHT - 150)
        elif round_time <= 0:
            draw_text("GAME OVER", font ,80, BLACK, WIDTH/2 + 22, HEIGHT - 150)
            if int(highscore) < score1:
                draw_text("NEW HIGH SCORE !", font ,80, BLACK,WIDTH/2 , HEIGHT/2 - 200)
                fichier = open("highscore.txt",'w')
                fichier.write(str(score1))
                fichier.close()
            elif int(highscore) < score2:
                draw_text("NEW HIGH SCORE !", font ,80, (0, 0, 0),WIDTH/2 , HEIGHT/2 - 200)
                fichier = open("highscore.txt",'w')
                fichier.write(str(score2))
                fichier.close()
        
            else:
                draw_text("HIGH SCORE: "+str(highscore), font ,80, BLACK,WIDTH/2 , HEIGHT/2 - 200)
            pg.display.update()
            time.sleep(2)
            running = False
            pg.display.update()
        pg.display.update()
