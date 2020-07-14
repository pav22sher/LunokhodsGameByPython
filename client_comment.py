import socket
import json
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from random import *

def quit():#выход из оконного приложения
	global game_over
	if messagebox.askokcancel("Выход", "Вы правда хотите выйти?"):
		if not game_over:#если игрок выходит, но игра не закончилась
			messagebox.showerror(title_msg+'\nОшибка!','Игра не закончена!')
		root.destroy()#уничтожаем окно
				
def gameOver(state):#проверяем выиграли ли мы
	global play2_number
	for r in range(8):
		for c in range(8):
			if state[r][c]==play2_number:
				return False
	else: return True
	
#изменение направления или перемещение вверх
def move_up(event):
	global direction
	global state
	global btns
	global r_play1
	global c_play1
	global image_play1
	global image_play1_w
	global image_space
	global play1_number
	global play2_number
	global score
	global root
	global title_msg
	global game_over
	#если игра не закончилась
	if not game_over:
		new_state=copy(state)
		#если направление не вперед, то меняем направление
		if direction!='w':
			direction='w'#изменили напрвавление
			image_play1=image_play1_w#изменили картинку лунохода
			btns[r_play1][c_play1]['image']=image_play1
		#иначе перемещаемся на одну клетку вперед, если она пустая
		elif (r_play1-1)>=0 and new_state[r_play1-1][c_play1]==0:
			new_state[r_play1][c_play1]=0#пердыдущее положение стало пустой клеткой
			r_play1=r_play1-1
			new_state[r_play1][c_play1]=play1_number#нынешнее положение стало луноходом
			refresh_draw(state,new_state,btns)#перерисовали в окне эти изменения 
			state=copy(new_state)#поменяли состояние доски 
			score=score-1#минус 1 очко за перемещение
			root.title(title_msg+"У вас "+str(score)+" очко(а)(ов) действия!")
			game=sendproc()#обмениваемся информацией с сервером и заканчиваем ход, если необходимо 
			if game: 
				root.title(title_msg+"У вас "+str(score)+" очко(а)(ов) действия!")
				messagebox.showinfo("Ваш ход!",title_msg+"Противник сделал свое дело!")
	
#изменение направления или перемещение вниз	
def move_down(event):
	global direction
	global state
	global btns
	global r_play1
	global c_play1
	global image_play1
	global image_play1_s
	global image_space
	global play1_number
	global play2_number
	global score
	global root
	global title_msg
	global game_over
	#аналогично функции move_up
	if not game_over:
		new_state=copy(state)
		if direction!='s':
			direction='s'
			image_play1=image_play1_s
			btns[r_play1][c_play1]['image']=image_play1
		elif (r_play1+1)<=7 and new_state[r_play1+1][c_play1]==0:
			new_state[r_play1][c_play1]=0
			r_play1=r_play1+1
			new_state[r_play1][c_play1]=play1_number
			refresh_draw(state,new_state,btns)
			state=copy(new_state)
			score=score-1
			root.title(title_msg+"У вас "+str(score)+" очко(а)(ов) действия!")
			game=sendproc()
			if game: 
				root.title(title_msg+"У вас "+str(score)+" очко(а)(ов) действия!")
				messagebox.showinfo("Ваш ход!",title_msg+"Противник сделал свое дело!")

#изменение направления или перемещение влево	
def move_left(event):
	global direction
	global state
	global btns
	global r_play1
	global c_play1
	global image_play1
	global image_play1_a
	global image_space
	global play1_number
	global play2_number
	global score
	global root
	global title_msg
	global game_over
	#аналогично функции move_up
	if not game_over:
		new_state=copy(state)
		if direction!='a':
			direction='a'
			image_play1=image_play1_a
			btns[r_play1][c_play1]['image']=image_play1
		elif (c_play1-1)>=0 and new_state[r_play1][c_play1-1]==0:
			new_state[r_play1][c_play1]=0
			c_play1=c_play1-1
			new_state[r_play1][c_play1]=play1_number
			refresh_draw(state,new_state,btns)
			state=copy(new_state)
			score=score-1
			root.title(title_msg+"У вас "+str(score)+" очко(а)(ов) действия!")
			game=sendproc()
			if game: 
				root.title(title_msg+"У вас "+str(score)+" очко(а)(ов) действия!")
				messagebox.showinfo("Ваш ход!",title_msg+"Противник сделал свое дело!")

#изменение направления или перемещение вправо				
def move_right(event):
	global direction
	global state
	global btns
	global r_play1
	global c_play1
	global image_play1
	global image_play1_d
	global image_space
	global play1_number
	global play2_number
	global score
	global root
	global title_msg
	global game_over
	#аналогично функции move_up
	if not game_over:
		new_state=copy(state)
		if direction!='d':
			direction='d'
			image_play1=image_play1_d
			btns[r_play1][c_play1]['image']=image_play1
		elif (c_play1+1)<=7 and new_state[r_play1][c_play1+1]==0:
			new_state[r_play1][c_play1]=0
			c_play1=c_play1+1
			new_state[r_play1][c_play1]=play1_number
			refresh_draw(state,new_state,btns)
			state=copy(new_state)
			score=score-1
			root.title(title_msg+"У вас "+str(score)+" очко(а)(ов) действия!")
			game=sendproc()
			if game:
				root.title(title_msg+"У вас "+str(score)+" очко(а)(ов) действия!")
				messagebox.showinfo("Ваш ход!",title_msg+"Противник сделал свое дело!")

#выстрел в указанном напрвлении
def shoot(event):
	global direction
	global state
	global btns
	global image_stena
	global image_space	
	global play1_number
	global play2_number
	global score
	global root
	global title_msg
	#если не конец игры
	if not game_over:
		if score<3: #если меньше 3 очков выстрел не возможен
			messagebox.showerror(title_msg+'Ошибка!','Недостаточно очков для выстрела!')
		else:#инчае стреляем 
			new_state=copy(state)
			if direction=='w':#выстрел вперед 
				for i in reversed(range(r_play1)):
					if new_state[i][c_play1]==3:#на пути выстрела препятствие
						new_state[i][c_play1]=0 #уничтожаем препятствие 
						break#уничтожается первое препятствие на линии огня
					elif new_state[i][c_play1]==play2_number:#на пути выстрела противник
						new_state[i][c_play1]=0 #уничтожаем противника 
						break
			if direction=='s':
				for i in range(r_play1,8):
					if new_state[i][c_play1]==3:
						new_state[i][c_play1]=0
						break
					elif new_state[i][c_play1]==play2_number:
						new_state[i][c_play1]=0
						break
			if direction=='a':
				for i in reversed(range(c_play1)):
					if new_state[r_play1][i]==3:
						new_state[r_play1][i]=0
						break
					elif new_state[r_play1][i]==play2_number:
						new_state[r_play1][i]=0
						break
			if direction=='d':
				for i in range(c_play1,8):
					if new_state[r_play1][i]==3:
						new_state[r_play1][i]=0
						break
					elif new_state[r_play1][i]==play2_number:
						new_state[r_play1][i]=0
						break
			refresh_draw(state,new_state,btns)#перерисовывам игровую доску
			state=copy(new_state)
			score=score-3#количество очков уменьшается на 3
			root.title(title_msg+"У вас "+str(score)+" очко(а)(ов) действия!")
			game=sendproc()#обмениваемся информацией с сервером и заканчиваем ход, если необходимо
			if game: 
				root.title(title_msg+"У вас "+str(score)+" очко(а)(ов) действия!")
				messagebox.showinfo("Ваш ход!",title_msg+"Противник сделал свое дело!")

#закончить свой ход			
def skip(event):
	global score
	global game_over
	if not game_over:
		score=0
		root.title(title_msg+"У вас "+str(score)+" очко(а)(ов) действия!")
		game=sendproc()
		if game: 
			root.title(title_msg+"У вас "+str(score)+" очко(а)(ов) действия!")
			messagebox.showinfo("Ваш ход!",title_msg+"Противник сделал свое дело!")

#рисуем доску в начале игры		
def init_draw(state,btns):
	global r_play1
	global c_play1
	global play1_number
	global play2_number
	for r in range(8):
		for c in range(8):
			if state[r][c]==play1_number:
				r_play1=r
				c_play1=c
				btns[r][c] = Label(root, image=image_play1, width=80,height=80)
			elif state[r][c]==play2_number:
				btns[r][c] = Label(root, image=image_play2, width=80,height=80)
			elif state[r][c]==3:
				btns[r][c] = Label(root, image=image_stena, width=80,height=80)
			elif state[r][c]==0:
				btns[r][c] = Label(root, image=image_space, width=80,height=80)
			btns[r][c].grid(row=r , column=c)
		
#перерисовываем только то, что было изменено		
def refresh_draw(state,new_state,btns):
	global image_play1
	global image_play2
	global r_play1
	global c_play1
	global play1_number
	global play2_number
	global image_stena
	global image_space
	for r in range(8):
		for c in range(8):
			if state[r][c]!=new_state[r][c]:
				if new_state[r][c]==play1_number:
					btns[r][c]['image']=image_play1
				elif new_state[r][c]==play2_number:
					btns[r][c]['image']=image_play2
				elif new_state[r][c]==3:
					btns[r][c]['image']=image_stena
				elif new_state[r][c]==0:
					btns[r][c]['image']=image_space

#копируем один лист в другой					
def copy(a):
	b=[[0 for i in range(8)] for j in range(8)]
	for i in range(8):
		for j in range(8):
			b[i][j]=a[i][j]
	return b

#передача и прием сообщений от сервера	
def sendproc():
	global client
	global state
	global root
	global title_msg
	global score
	global game_over
	
	try:#если очки, которые были даны на ход закончились
		if score==0 or gameOver(state):#или мы решили закончить свой ход или мы убили противника
			if not gameOver(state): 
				messagebox.showinfo("Ваш ход закончился!", title_msg+"Ожидайте хода противника!")
				root.title(title_msg+"Ожидайте хода противника!")
			client.send(json.dumps(state).encode())#посылаем серверу состояние доски 
			
			#print("Ожидайте...")
			start=json.loads(client.recv(1024).decode())
			client.send(json.dumps("Okey").encode())
			if start!="Start":#если гра закончилась
				new_state=json.loads(client.recv(1024).decode())#принимаем коненчое состояние доски
				refresh_draw(state,new_state,btns)#перерисуем окно в конечное состояние 
				root.title(title_msg+"Игра закончилась!")
				messagebox.showinfo("Результат игры:",title_msg+start)#вывод результата
				client.close()#закрываем сокет
				game_over=True
				return False
			else:#если игра не закончилась
				new_state=json.loads(client.recv(1024).decode())
				refresh_draw(state,new_state,btns)
				state=copy(new_state)
				score=randint(1, 6)#даем ему очки на следующий ход
			return True
	except BaseException:
		messagebox.showerror(title_msg+'Ошибка!','Игра не может быть продолжена\n из-за второго игрока или сервера!')
		root.destroy()
		client.close()

#вывод правил игры	
def game_rules():
	messagebox.showinfo('Правила игры : ','Каждый игрок управляет луноходом,\n'
	+'перемещающимся по шахматной доске 8×8, \n'
	+'на которой случайным образом расставлены \n'
	+'препятствия. Игроки ходят по очереди. \n'
	+'В начале хода игрок равновероятно \n'
	+'получает от 1 до 6 очков действия. \n'
	+'Перемещения лунохода в соседнюю клетку стоит 1 очко, \n'
	+'а выстрел в некотором направлении – 3 очка. \n'
	+'При выстреле, первый объект, находящийся в \n'
	+'заданном направлении от лунохода, уничтожается. \n'
	+'Побеждает игрок, уничтоживший луноход противника. \n')

#вывод управления	
def game_control():
	messagebox.showinfo('Управление : ','Клавиши: \n'
	+'w-развернутся или переместится вперед;\n'
	+'s-развернутся или переместится назад;\n'
	+'a-развернутся или переместится влево;\n'
	+'d-развернутся или переместится вправо;\n'
	+'enter-выстрелить в направление куда направлено дуло;\n'
	+'space-закончить свой ход;\n'
	+'f1-правила игры\n'
	+'f2-управление;\n'
	+'w-развернутся или переместится вперед.')

#обработка нажатия на f1
def f1_control(event):
	if not game_over: game_rules()

#обработка нажатия на f2
def f2_control(event):
	if not game_over: game_control()
	
game_over=False #игра закончилась или нет
	
root = Tk()#главное окно
root.geometry('680x680')
root.resizable(width=False, height=False)
root.protocol("WM_DELETE_WINDOW", quit)

#bind() связываются между собой событие и действие(оброботчик события)
root.bind("<w>", move_up)
root.bind("<s>", move_down)
root.bind("<a>", move_left)
root.bind("<d>", move_right)

root.bind("<Return>", shoot)
root.bind("<space>", skip)
root.bind("<F1>", f1_control)
root.bind("<F2>", f2_control)

SERVER = "localhost" #(localhost в диапазоне 127.0.0.1 — 127.255.255.255)
PORT = 2222 #системные (0—1023), пользовательские (1024—49151) и частные (49152—65535)

try:
	#создаем сокет
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM ,0)
	client.connect((SERVER, PORT))#конектимся к серверу
	
	play1_number=json.loads(client.recv(1024).decode())#Свой номер
	client.send(json.dumps("Okey").encode())#синхронизация
	play2_number=json.loads(client.recv(1024).decode())#Номер противника
	client.send(json.dumps("Okey").encode())#синхронизация
	state=json.loads(client.recv(1024).decode())#игровая доска
	client.send(json.dumps("Okey").encode())#синхронизация
	
	btns=[[None for c in range(8)] for r in range(8)]
	direction='w'#направление игрока
	#изображения луноходов во всех направлениях
	image_play1_w= ImageTk.PhotoImage(file="play1/play1_w.jpg") if play1_number==1 else ImageTk.PhotoImage(file="play2/play2_w.jpg")  
	image_play1_s= ImageTk.PhotoImage(file="play1/play1_s.jpg") if play1_number==1 else ImageTk.PhotoImage(file="play2/play2_s.jpg")  
	image_play1_d= ImageTk.PhotoImage(file="play1/play1_d.jpg") if play1_number==1 else ImageTk.PhotoImage(file="play2/play2_d.jpg")  
	image_play1_a= ImageTk.PhotoImage(file="play1/play1_a.jpg") if play1_number==1 else ImageTk.PhotoImage(file="play2/play2_a.jpg")  
	image_play1=image_play1_w
	
	#изображения лунохода противника, препятствия и пустых полей
	image_play2=ImageTk.PhotoImage(file="play2/play2_s.jpg") if play1_number==1 else ImageTk.PhotoImage(file="play1/play1_s.jpg")
	image_stena=ImageTk.PhotoImage(file="stena.jpg")
	image_space=ImageTk.PhotoImage(file="space.jpg")
	
	#Окно и сообщения какого игрока выводятся 
	if play1_number==1: title_msg="Красный игрок: \n"
	else: title_msg="Синий игрок: \n"
	
	#Количество очков действия на ход
	score=randint(1, 6)
	root.title(title_msg+"У вас "+str(score)+" очков действия!")

	print("Ожидайте...")
	start=json.loads(client.recv(1024).decode())#начало игры
	client.send(json.dumps("Okey").encode())#для синхронизации
	state=json.loads(client.recv(1024).decode())#нынешннее состояние доски
	
	init_draw(state,btns)#начальная отрисовка
	game_rules()#вывод правил игры
	game_control()#вывод управления
	root.mainloop()#запускаем главный цыкл оконоого приложения
except BaseException:#ловим ошибку
	messagebox.showerror('Ошибка!','Игра не может быть продолжена\n из-за второго игрока или сервера!')
	root.destroy()#уничтожаем окно приложения
	client.close()#закрываем сокет
