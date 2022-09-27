from tkinter import *
from random import *
import pygame

class storeTycoon:
    def __init__(self,window):
        self.window = window
        self.canvas = Canvas(self.window, bg = "white")
        self.keys = set()

        #Effect sound
        self.sounds = pygame.mixer
        self.sounds.init()
        self.footsteps = [self.sounds.Sound("sound/footsteps"+str(i+1)+".wav") for i in range(4)]
        self.doorbell = self.sounds.Sound("sound/doorbell.wav")
        self.doorclose = self.sounds.Sound("sound/doorclose.wav")
        self.counterdoor = self.sounds.Sound("sound/doorclose2.wav")
        self.pay = self.sounds.Sound("sound/pay.wav")
        self.itempick = self.sounds.Sound("sound/itempick.wav")

        self.backgroundimg = [PhotoImage(file="image/background.png"), PhotoImage(file="image/background_top.png")]
        self.background = self.canvas.create_image(320,240, image = self.backgroundimg[0])

        self.sale_img_list = []
        self.sale_img_idx = []
        

        for i in range(16):
            fname0 = "image/sale"+str(i+1)+".png"
            fname1 = "image/sale"+str(i+1)+"_none.png"
            self.sale_img_list.append([PhotoImage(file=fname0), PhotoImage(file=fname1)])
            self.sale_img_idx.append(self.canvas.create_image(320, 240, image = self.sale_img_list[i][0], tags = 'sale'))

        self.tableimg = [PhotoImage(file="image/table_close.png"), PhotoImage(file="image/table_open.png")]
        self.table = self.canvas.create_image(320,240, image = self.tableimg[0])

        self.consumer_img_idx = 0
        self.consumer_img = []
        for i in range(1,9):
            self.consumer_img.append([PhotoImage(file="image/consumer"+str(i)+"_front.png"), 
            PhotoImage(file="image/consumer"+str(i)+"_back.png"), 
            PhotoImage(file="image/consumer"+str(i)+"_left.png"), 
            PhotoImage(file="image/consumer"+str(i)+"_right.png")])

        self.playerimgs = [PhotoImage(file="image/player_front.png"), 
                           PhotoImage(file="image/player_back.png"), 
                           PhotoImage(file="image/player_left.png"), 
                           PhotoImage(file="image/player_right.png")]
        self.player = self.canvas.create_image(528,208, image = self.playerimgs[0], anchor='s')

        self.background_top = self.canvas.create_image(320,240, image = self.backgroundimg[1])

        self.money = 0

        self.moneystr = "MONEY: " + '{0:,}'.format(self.money)
        self.moneytext = self.canvas.create_text(20,450 ,font="Times 15 italic bold",text=self.moneystr, anchor='nw', fill='green')

        self.playerway = 'front'
        self.consumerway = 'front'
        self.consumerExists = 0
        self.consumerWant = ''
        self.loopcount = 0


        #방해물 배열
        self.block = [ [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
                      [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
                      [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
                      [ 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1 ],
                      [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1 ],
                      [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1 ],
                      [ 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1 ],
                      [ 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1 ],
                      [ 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1 ],
                      [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
                      [ 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1 ],
                      [ 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
                      [ 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ],
                      [ 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
                      [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ] ]
       
        self.salemax = 2
        self.salelist = [['컵라면', 1200, self.salemax,[80,80]],
                         ['콜라', 1800, self.salemax,[144,80]],
                         ['물',1000, self.salemax,[176,80]],
                         ['잡지', 2000, self.salemax, [400,112]],
                         ['프링글스', 3000, self.salemax,[48, 208]],
                         ['빼빼로', 1500, self.salemax, [112, 208]],
                         ['새우깡', 1400, self.salemax, [208, 240]],
                         ['마이쮸', 800, self.salemax, [304,240]],
                         ['오징어칩', 1400, self.salemax, [208, 336]],
                         ['봉지라면', 4000, self.salemax, [304, 336]],
                         ['스타킹', 3000, self.salemax, [48, 368]],
                         ['마스크', 3500, self.salemax, [112, 368]],
                         ['약', 2000, self.salemax, [304, 432]],
                         ['사탕', 200, self.salemax, [432, 432]],
                         ['젤리', 1000, self.salemax, [528, 432]],
                         ['계산', 0,  0, [496, 208]]] 
                        #[품명, 가격, 재고량, [x,y]]

        #for i in range(len(self.salelist)):
        #    self.salelist[i][2] = 0

        for i in range(len(self.salelist)-1):
            if self.salelist[i][2] == 0:
                self.canvas.itemconfig(self.sale_img_idx[i], image = self.sale_img_list[i][1])

        self.sale_name_list = [self.salelist[i][0] for i in range(len(self.salelist))]

    def saveload(self,data):
        self.money = int(data)
        self.moneystr = "MONEY: " + '{0:,}'.format(self.money)
        self.canvas.itemconfig(self.moneytext, text = self.moneystr)
        #print(self.moneystr)

    def viewcoor_front(self,x, y,way):
        #캐릭터가 바라보는 곳 좌표
        self.x = int(x)
        self.y = int(y)
        if way == 'left':
            return [self.x-32, self.y]
        if way == 'back':
            return [self.x, self.y-32]
        if way == 'right':
            return [self.x+32, self.y]
        if way == 'front':
            return [self.x, self.y + 32]

    def viewcoor_left(self,x, y,way):
        #캐릭터가 바라보는 곳 좌표
        self.x = int(x)
        self.y = int(y)
        if way == 'left':
            return [self.x, self.y + 32]
        if way == 'back':
            return [self.x -32, self.y]
        if way == 'right':
            return [self.x, self.y - 32]
        if way == 'front':
            return [self.x + 32, self.y]

    def viewcoor_right(self,x, y,way):
        #캐릭터가 바라보는 곳 좌표
        self.x = int(x)
        self.y = int(y)
        if way == 'left':
            return [self.x, self.y - 32]
        if way == 'back':
            return [self.x + 32, self.y]
        if way == 'right':
            return [self.x, self.y + 32]
        if way == 'front':
            return [self.x - 32, self.y]

    def exploring(self, x, y, way, want_idx):
        leftcoor = self.viewcoor_left(x, y, way)
        if self.salelist[want_idx][3][0] == leftcoor[0] and self.salelist[want_idx][3][1] == leftcoor[1]:
            if way == 'left':
                self.consumerway = 'front'
            if way == 'back':
                self.consumerway = 'left'
            if way == 'right':
                self.consumerway = 'back'
            if way == 'front':
                self.consumerway = 'right'
            

        rightcoor = self.viewcoor_right(x, y, way)
        if self.salelist[want_idx][3][0] == rightcoor[0] and self.salelist[want_idx][3][1] == rightcoor[1]:
            if way == 'left':
                self.consumerway = 'back'
            if way == 'back':
                self.consumerway = 'right'
            if way == 'right':
                self.consumerway = 'front'
            if way == 'front':
                self.consumerway = 'left'

    def walltest(self, x, y, way):
        #block[20][15]

        self.x = int(y / 32) 
        self.y = int(x / 32)
        #print('%d   %d' %(x, y))
        #print('%d   %d' %(self.x, self.y))
        if way == 'left':
            return self.block[self.x][self.y - 1]
        if way == 'back':
            return self.block[self.x - 1][self.y]
        if way == 'right':
            return self.block[self.x][self.y + 1]
        if way == 'front':
            return self.block[self.x + 1][self.y]

    def characterMove(self, character, characterimg, way):
        if way == 'left': #left
            self.canvas.move(character, -32, 0)
            self.canvas.itemconfig(character, image = characterimg[2])
        if way == 'back': #up
            self.canvas.move(character, 0, -32)
            self.canvas.itemconfig(character, image = characterimg[1])
        if way == 'right': #right
            self.canvas.move(character, 32, 0)
            self.canvas.itemconfig(character, image = characterimg[3])
        if way == 'front': #down
            self.canvas.move(character, 0, 32)
            self.canvas.itemconfig(character, image = characterimg[0])

        self.footsteps[randint(0,3)].play()

    def display(self):
        self.loopcount += 1
        #print(self.loopcount)

        #손님 랜덤 등장
        if self.loopcount == 49:
            self.loopcount = 0
            if self.consumerExists == 0:
                if randrange(1,2) == 1:
                    self.consumer_img_idx = randint(0,7)
                    self.consumer = self.canvas.create_image(336,112, image = self.consumer_img[self.consumer_img_idx][0], anchor='s')
                    self.consumerExists = 1
                    self.consumerWant = [choice(self.sale_name_list[3:-2]), False, False] #[원하는 품목, 원하는 물건을 집었는지, 계산이 되었는지]
                    self.doorbell.play()
                    #print(self.consumerWant)

        #손님 이동
        if self.consumerExists == 1:

            consumerX = self.canvas.coords(self.consumer)[0]
            consumerY = self.canvas.coords(self.consumer)[1]

            frontcoor = self.viewcoor_front(consumerX, consumerY, self.consumerway)
            if self.loopcount % 2 == 0: #손님 속도
                want_idx = self.sale_name_list.index(self.consumerWant[0])
                

                if self.consumerWant[2] == False:
                    if self.consumerWant[1] == True:
                        want_idx = -1
                        #print(self.sale_name_list[want_idx], '할 거에요')

                    if self.walltest(consumerX, consumerY, self.consumerway) == 1:
                        if self.consumerway == 'front' or self.consumerway == 'back':
                            self.consumerway = choice(['left','right'])
                        elif self.consumerway == 'left' or self.consumerway == 'right':
                            self.consumerway = choice(['front','back'])

                    elif self.walltest(consumerX, consumerY, self.consumerway) == 0:
                        self.characterMove(self.consumer, self.consumer_img[self.consumer_img_idx], self.consumerway)

                        if self.salelist[want_idx][3][0] > frontcoor[0]:
                            self.consumerway = 'right'
                        if self.salelist[want_idx][3][0] < frontcoor[0]:
                            self.consumerway = 'left'

                        if self.salelist[want_idx][3][1] > frontcoor[1]:
                                self.consumerway = 'front'
                        if self.salelist[want_idx][3][1] < frontcoor[1]:
                                self.consumerway = 'back'

                        if self.consumerWant[0] not in self.salelist[:2]:
                            if self.salelist[want_idx][3][1] == frontcoor[1]+32:
                                if self.salelist[want_idx][3][0] > frontcoor[0]:
                                    self.consumerway = 'right'
                                if self.salelist[want_idx][3][0] < frontcoor[0]:
                                    self.consumerway = 'left'

                    self.exploring(consumerX, consumerY, self.consumerway, want_idx)

                    if self.consumerWant[1] == False:
                        if self.salelist[want_idx][3][0] == frontcoor[0] and self.salelist[want_idx][3][1] == frontcoor[1]:
                            #print('물건을 집을거에요')
                            if self.salelist[want_idx][2] > 0:
                                self.salelist[want_idx][2] -= 1
                                self.consumerWant[1] = True
                                if self.salelist[want_idx][2] == 0:
                                    self.canvas.itemconfig(self.sale_img_idx[want_idx], image = self.sale_img_list[want_idx][1])
                                #print(self.consumerWant[0], '을 집었어요')
                                #print(self.consumerWant[0], self.salelist[want_idx][2],"개 남았어요")
                                self.itempick.play()
                            else:
                                print('물건이 없어요')

                    if self.consumerWant[1] == True:
                        if self.consumerWant[2] == False:
                            if 496 == frontcoor[0] and 208 == frontcoor[1]:
                                print(self.consumerWant[0], "계산해주세요")

                #손님 퇴장
                elif self.consumerWant[2] == True:
                    #("계산 다 했어요 나갈래요")
                    if consumerY == 208.0 and consumerX > 304.0:
                        self.consumerway = 'left'
                        self.characterMove(self.consumer, self.consumer_img[self.consumer_img_idx], self.consumerway)
                    if consumerX == 304.0:
                        self.consumerway = 'back'
                        self.characterMove(self.consumer, self.consumer_img[self.consumer_img_idx], self.consumerway)
                    if consumerX == 304.0 and consumerY == 112.0:
                        self.canvas.delete(self.consumer)
                        self.consumerExists = 0
                        self.doorclose.play()
                    
        self.playerX = self.canvas.coords(self.player)[0]
        self.playerY = self.canvas.coords(self.player)[1]

        for key in self.keys:
            if key == 40: # down direction key
                self.canvas.itemconfig(self.player, image = self.playerimgs[0])
                self.playerway = 'front'
                if self.walltest(self.playerX, self.playerY,self.playerway) == 0:
                    self.characterMove(self.player, self.playerimgs, self.playerway)

            if key == 39: # right direction key
                self.canvas.itemconfig(self.player, image = self.playerimgs[3])
                self.playerway = 'right'
                if self.walltest( self.playerX, self.playerY,self.playerway) == 0:
                    self.characterMove(self.player, self.playerimgs, self.playerway)

            if key == 38: # up direction key         
                self.canvas.itemconfig(self.player, image = self.playerimgs[1])
                self.playerway = 'back'
                if self.walltest( self.playerX, self.playerY,self.playerway) == 0:
                    self.characterMove(self.player, self.playerimgs, self.playerway)

            if key == 37: # left direction key                
                self.canvas.itemconfig(self.player, image = self.playerimgs[2])
                self.playerway = 'left'
                if self.walltest( self.playerX, self.playerY,self.playerway) == 0:
                    self.characterMove(self.player, self.playerimgs, self.playerway)

            if key == 32: #space key
                #캐릭터가 바라보고 있는 좌표
                frontcoor = self.viewcoor_front(self.playerX, self.playerY, self.playerway)
                #print(frontcoor)
                
                #손님 계산해주기
                if self.consumerExists == 1 and self.consumerWant[1] == True and self.consumerWant[2] == False:
                    if self.canvas.coords(self.consumer)[0] == 464.0 and self.canvas.coords(self.consumer)[1] == 208.0:
                        if frontcoor[0] == 496 and frontcoor[1] == 208:
                            self.money += self.salelist[self.sale_name_list.index(self.consumerWant[0])][1]
                            self.moneystr = "MONEY: " + '{0:,}'.format(self.money)
                            self.canvas.itemconfig(self.moneytext, text = self.moneystr)
                            self.consumerWant[2] = True
                            self.pay.play()

                #빈 물건 채우기
                for i in range(len(self.salelist)):
                    if self.salelist[i][3][0] == frontcoor[0] and self.salelist[i][3][1] == frontcoor[1]:
                        if self.salelist[i][2] == 0:
                            self.salelist[i][2] = self.salemax
                            self.canvas.itemconfig(self.sale_img_idx[i], image = self.sale_img_list[i][0])
                            self.itempick.play()
                
                #문열기
                if frontcoor[0] == 560 and frontcoor[1] == 272:
                    if self.block[8][17] == 1: 
                        self.canvas.itemconfig(self.table, image = self.tableimg[1]) #문열기
                        self.block[8][17] = 0
                        #print(self.block[8][17])
                    else: 
                        self.canvas.itemconfig(self.table, image = self.tableimg[0]) #문닫기
                        self.block[8][17] = 1
                        #print(self.block[8][17])
                    self.counterdoor.play()

    def keyPressHandler(self,event):        
        self.keys.add(event.keycode)

    def keyReleaseHandler(self, event):
        if event.keycode in self.keys:
            self.keys.remove(event.keycode)

        if event.keycode == 8:
            return 0
        else:
            return -1

    def pack(self):
        self.canvas.pack(expand=True, fill=BOTH)

    def unpack(self):
        self.canvas.pack_forget()

    def destroy(self):
        self.canvas.destroy()


class Menu:
    def __init__(self,window):
        self.window = window
        self.canvas=Canvas(self.window, bg ="white")
        self.canvas.pack(expand=True, fill=BOTH)
        self.menu_idx = 0

        self.backgroundimg = PhotoImage(file="image/menuimg.png")
        self.background = self.canvas.create_image(320,240, image = self.backgroundimg)

        self.start = self.canvas.create_text(120,400,font="Times 15 italic bold",text="게임시작")
        self.load = self.canvas.create_text(320,400,font="Times 15 italic bold",text="불러오기")
        self.exit = self.canvas.create_text(520,400,font="Times 15 italic bold",text="게임종료")

        self.arrowimg = PhotoImage(file="image/select.png")#.subsample(20)
        self.arrow = self.canvas.create_image(121,398, image = self.arrowimg,tags="arrow")

        self.sounds = pygame.mixer
        self.sounds.init()
        self.select = self.sounds.Sound("sound/select.wav")
        self.click = self.sounds.Sound("sound/click.wav")

    def display(self):
        pass

    def keyReleaseHandler(self, event):

        if event.keycode == 37 and self.menu_idx > 0: # up direction key
            self.menu_idx = self.menu_idx - 1
            self.canvas.move(self.arrow, -200, 0)
            self.select.play()
            return -1

        if event.keycode == 39 and self.menu_idx < 2: # down direction key
            self.menu_idx = self.menu_idx + 1
            self.canvas.move(self.arrow, 200, 0)
            self.select.play()
            return -1

        if event.keycode == 32:
            self.click.play()
            return self.menu_idx

    def keyPressHandler(self,event):
        pass

    def pack(self):
        self.canvas.pack(expand=True, fill=BOTH)

    def unpack(self):
        self.canvas.pack_forget()

    def destroy(self):
        self.canvas.destroy()


class SceneChange:
    def __init__(self):
        self.window = Tk()
        self.window.title("편의점 타이쿤")
        self.window.geometry("640x480")

        self.scene_idx = 0
        
        self.stage = storeTycoon(self.window)
        self.menu = Menu(self.window)
        self.menu.pack()

        self.canvas_list = []
        self.canvas_list.append(self.menu)
        self.canvas_list.append(self.stage)

        self.window.bind("<KeyPress>",self.keyPressHandler)
        self.window.bind("<KeyRelease>",self.keyReleaseHandler)

        file  = open('save.txt' , 'r' )
        self.savedata = file.read()
        file.close()

        pygame.init()
        pygame.mixer.music.load("sound/menubgm.mp3")
        pygame.mixer.music.play(-1)

        self.x = True
        while self.x == True:
            #for canvas in self.canvas_list:
            #    canvas.display()
            if self.scene_idx == 0:
                self.menu.display()
            if self.scene_idx == 1:
                self.stage.display()

            self.window.after(120)
            self.window.update()

    def update_x(self):
        self.x = False

    def on_closing(self):
        for canvas in self.canvas_list:
            canvas.destroy()

        self.window.destroy()

    def keyReleaseHandler(self, event):

        result = -1

        result = self.canvas_list[self.scene_idx].keyReleaseHandler(event)
        

        if self.scene_idx == 0 and result==0:
            self.menu.canvas.itemconfigure(self.menu.start, text="다시시작")
            self.menu.canvas.itemconfigure(self.menu.exit, text=" 저장 후\n게임종료")
            self.scene_idx = 1
            self.menu.unpack()
            self.stage.pack()
            pygame.mixer.music.load("sound/gamebgm.mp3")
            pygame.mixer.music.play(-1)

        elif self.scene_idx == 1 and result==0:
            self.scene_idx = 0
            self.menu.pack()#메뉴 canvas 나타남
            self.stage.unpack()# Main 장면 canvas 사라짐
            pygame.mixer.music.load("sound/menubgm.mp3")
            pygame.mixer.music.play(-1)
        
        #불러오기
        elif self.scene_idx == 0 and result == 1:
            self.menu.canvas.itemconfigure(self.menu.start, text="다시시작")
            self.menu.canvas.itemconfigure(self.menu.load, text="")
            self.menu.canvas.itemconfigure(self.menu.exit, text=" 저장 후\n게임종료")
            
            self.stage.saveload(self.savedata)
            self.scene_idx = 1
            self.menu.unpack()
            self.stage.pack()
            pygame.mixer.music.load("sound/gamebgm.mp3")
            pygame.mixer.music.play(-1)
    
        #종료
        elif self.scene_idx == 0 and result == 2:
            file  = open('save.txt' , 'w' )
            file.write(str(self.stage.money))
            file.close()
            self.on_closing()
            self.update_x()

    def keyPressHandler(self,event):
        self.canvas_list[self.scene_idx].keyPressHandler(event)

SceneChange()