import pygame, random, sys, numpy

pygame.init()
HEIGHT, WIDTH = 800, 800 

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

slot = pygame.transform.scale(pygame.image.load("Fruit machine/assets/slot.png"), (60, 770)).convert_alpha()
slots_spinning = pygame.transform.scale(pygame.image.load("Fruit machine/assets/slots.png"), (192, 128)).convert_alpha()
slot_machine = pygame.transform.scale(pygame.image.load("Fruit machine/assets/slot_machine.png"), (272, 458)).convert_alpha()
coin = pygame.image.load("Fruit machine/assets/coin.png").convert_alpha()
bg = pygame.image.load("Fruit machine/assets/tempbg.png").convert_alpha()

fruits = {
    "cherry": pygame.image.load("Fruit machine/fruits/cherry.png").convert_alpha(),
    "grape": pygame.image.load("Fruit machine/fruits/grape.png").convert_alpha(),
    "lemon": pygame.image.load("Fruit machine/fruits/lemon.png").convert_alpha(),
    "melon": pygame.image.load("Fruit machine/fruits/melon.png").convert_alpha()
}

fruit_coords = {
    70 : "cherry",
    20 : "grape",
    230: "lemon",
    150: "melon",
}

jackpot = pygame.mixer.Sound("Fruit machine/music/jackpot_payout.wav")
win = pygame.mixer.Sound("Fruit machine/music/win_payout.wav")
spinning = pygame.mixer.Sound("Fruit machine/music/spinning.wav")

class Machine:
    def __init__(self):
        self.spinning = True
        self.fruit = [72 - random.randint(1, 4) * 72 for i in range(3)]
        self.coins = [[[450, 550], [0, 5], 0]]
        self.counter = 0

    def play_animation_win(self, jackpot):
        if jackpot:
            self.coins.append([[450, 550], [random.randint(0, 20) / 10 - 1, 10], 0])
        screen.fill((255, 255, 255))

        screen.blit(fruits[self.f1], (306, 308))
        screen.blit(fruits[self.f2], (369, 308))
        screen.blit(fruits[self.f3], (434, 308))
        screen.blit(bg,  (0, 0))
        screen.blit(slot_machine, (263, 171))

        for coin in self.coins:
            coin[2] += 5
            coin[0][0] += coin[1][0]
            coin[0][1] += coin[1][1]

            if coin[2] > random.randint(300, 400):
                self.coins.remove(coin)

            screen.blit(pygame.image.load("Fruit machine/assets/coin.png").convert_alpha(), coin[0])

        pygame.display.flip()
 
    def play_animation_spin(self):
        self.fruit1_y, self.fruit2_y, self.fruit3_y =  self.fruit[0], self.fruit[1], self.fruit[2]
        for _ in range(75):
            screen.blit(slots_spinning, (304, 308))

            self.fruit1_y += 3
            self.fruit2_y += 3
            self.fruit3_y += 3

            screen.blit(slot, (305, self.fruit1_y))
            screen.blit(slot, (370, self.fruit2_y))
            screen.blit(slot, (435, self.fruit3_y))

            screen.blit(bg,  (0, 0))
            screen.blit(slot_machine, (263, 171))
            pygame.display.flip()

    def playsound(self, win_type):   
        if win_type == "jackpot":
            jackpot.play()
        elif win_type == "win":
            win.play()
        
        return None

    def get_closest(self, input_list, input_value):
        arr = numpy.asarray(input_list)

        return arr[(numpy.abs(arr - input_value)).argmin()]
     
    def check_win(self, f1, f2, f3):
        if f1 == f2 == f3:
            return "jackpot"
        elif f1 == f2 or f2 == f3 or f1 == f3:
            return "win"
        else:
            return "loss"

    def reward(self):
        if self.win_type == "jackpot":
            self.play_animation_win(True)

        elif self.win_type == "win":
            self.play_animation_win(False)
 
    def spin(self):
        if self.spinning:
            if self.counter == 0:
                spinning.play()
            self.counter += 1
            self.play_animation_spin()
                      
        if self.counter > 20:
            spinning.stop()
            self.f1, self.f2, self.f3 = fruit_coords[self.get_closest(list(fruit_coords), self.fruit1_y)], fruit_coords[self.get_closest(list(fruit_coords), self.fruit2_y)], fruit_coords[self.get_closest(list(fruit_coords), self.fruit3_y)]
            self.win_type = self.check_win(self.f1, self.f2, self.f3)
            self.playsound(self.win_type)
            self.spinning = False
            self.counter = 0

        if not self.spinning:
            screen.blit(fruits[self.f1], (306, 308))
            screen.blit(fruits[self.f2], (369, 308))
            screen.blit(fruits[self.f3], (434, 308))
            self.reward()

    def update(self):
        if keys[pygame.K_SPACE]:
            self.__init__()

        self.spin()
        
machine = Machine()

while True:
    mx, my = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    screen.blit(slots_spinning, (304, 308))  
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    machine.update()
    pygame.display.flip()
    clock.tick(60)