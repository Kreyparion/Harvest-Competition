from env.utils import Action, State
import copy
import numpy as np
import pygame
import time

class Env:
    def __init__(self,seed=None):
        self.seed = seed
        self.score = 0
        self.size = 10
        self.max_step = 500
        self.step_num = 0
        self.action_logs = []
        
    def reset(self):
        self.state = State.generate(self.seed)
        self.score = 0
        self.step_num = 0
        self.action_logs = []
        return self.state
    
    def step(self, action : Action):
        self.action_logs.append(action)
        next_state_map = copy.deepcopy(self.state.map)
        reward = 0
        if action == 0:
            next_state_map = np.roll(next_state_map,1,axis=0)
            val = next_state_map[4,4]
            if val != 0:
                reward = val*2/5
                self.score += reward
                next_state_map[4,4] = max(10,val-reward)
            
            
        elif action == 1:
            next_state_map = np.rot90(next_state_map,1,axes=[0,1])
        
        
        next_state_map *= 1.015
        next_state_map = np.clip(next_state_map,0,500)
        self.step_num += 1
        done = False
        if self.step_num == self.max_step:
            done = True
        next_state = State(next_state_map,self.seed)
        self.state = next_state
        return next_state, reward, done
    
    def getPossibleActions(self, state=None):
        return [Action(0),Action(1)]
    
    def getPossibleActionsAsInt(self, state=None):
        return [0,1]
    
    def render(self):
        pass
    
    def save_solution(self):
        if self.step_num == self.max_step:
            np.save('predictions.npy', np.array(self.action_logs))
        else:
            raise Exception("Saved uncompleted solution.")

    def final_render(self,speed=5):
        init_state = State.generate(self.seed)
        tab_ore = np.flip(init_state.map,axis=1)
        tab_ore = np.rot90(tab_ore,1,axes=[0,1])
        ship_pos = [4,4]
        ship_dir = 0 # 0 North, 1 East, 2 South, 3 West
        
        pygame.display.set_caption("Mining Zone")
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 20)
        screen = None
        ship_img = pygame.image.load("env/789670.png")
        c = 5

        ship_img = pygame.transform.smoothscale(ship_img, (c*10, c*10))

        
        screen_size = None
        display_interface = True
        if screen_size == None:
            screen_width = 800  # dimension initiales de la fenêtre
            screen_heigth = 600
        else:
            (screen_width, screen_heigth) = screen_size

        background_color = (202, 231, 249)  # bleu clair
        if display_interface:
            if screen == None:
                screen = pygame.display.set_mode(
                    (screen_width, screen_heigth), pygame.RESIZABLE)

            screen.fill(background_color)
            pygame.display.set_caption("Mining Zone")
            
            pygame.display.flip()

        running = True
        t = 0
        score = 0
        while running:  # boucle traitant des event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # si on appuie sur la croix
                    running = False
                if event.type == pygame.VIDEORESIZE:  # si on change la taille de la fenêtre
                    screen_width = event.w
                    screen_heigth = event.h
                    screen = pygame.display.set_mode(
                        (screen_width, screen_heigth), pygame.RESIZABLE)
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] == 1:  # si on appuie sur echap
                running = False
            
            # refresh à chaque tour de boucle
            screen.fill(background_color)
            for i in range(len(tab_ore)):
                for j in range(len(tab_ore[0])):
                    if tab_ore[i][j] != 0:
                        strnum = str(int(abs(tab_ore[i][j])*10)/10)
                        textsurface = myfont.render(strnum, False, (0, 0, 0))
                        screen.blit(textsurface, (i*c*10+c, j*c*10+c*3))
            str_score = "score : " + str(int(score))
            text_score = myfont.render(str_score, False, (0, 0, 0))
            screen.blit(text_score,(11*c*10,3*c*10))
            screen.blit(ship_img, (ship_pos[0]*c*10, ship_pos[1]*c*10))
            action = self.action_logs[t]
            if action == 1:
                ship_img = pygame.transform.rotate(ship_img, -90)
                ship_dir = (ship_dir+1)%4
            if ship_dir == 0:
                ship_pos[1] = (ship_pos[1]-1)%10
            elif ship_dir == 2:
                ship_pos[1] = (ship_pos[1]+1)%10
            elif ship_dir == 1:
                ship_pos[0] = (ship_pos[0]+1)%10
            elif ship_dir == 3:
                ship_pos[0] = (ship_pos[0]-1)%10
            
            reward = 0
            if action == 0:
                val = tab_ore[ship_pos[0],ship_pos[1]]
                if val != 0:
                    reward = val*2/5
                    score += reward
                    tab_ore[ship_pos[0],ship_pos[1]] = max(10,val-reward)
                tab_ore = tab_ore *1.01
                
            elif action == 1:
                tab_ore = tab_ore *1.01
            
            tab_ore = np.clip(tab_ore,0,500)
            
            
            pygame.display.flip()
            t += 1
            if t >= len(self.action_logs):
                running = False
            time.sleep(1/speed)

        pygame.display.quit()
        print(score)
        print(t)
            