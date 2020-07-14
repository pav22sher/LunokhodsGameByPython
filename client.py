import socket
import json
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from random import *

def quit():
	if messagebox.askokcancel("Выход", "Вы правда хотите выйти?"):
		if not game_over:
			messagebox.showerror(title_msg+'\nОшибка!','Игра не закончена!')
		root.destroy()
				
def gameOver(state):
	global play2_number
	for r in range(8):
		for c in range(8):
			if state[r][c]==play2_number:
				return False
	else: return True
	
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
	
	if not game_over:
		new_state=copy(state)
		if direction!='w':
			direction='w'
			image_play1=image_play1_w
			btns[r_play1][c_play1]['image']=image_play1
		elif (r_play1-1)>=0 and new_state[r_play1-1][c_play1]==0:
			new_state[r_play1][c_play1]=0
			r_play1=r_play1-1
			new_state[r_play1][c_play1]=play1_number
			refresh_draw(state,new_state,btns)
			state=copy(new_state)
			score=score-1
			root.title(title_msg+"У вас "+str(score)+" очко(а)(ов) действия!")
			game=sendproc()
			if game: 
				root.title(title_msg+"У вас "+str(score)+" очко(а)(ов) действия!")
				messagebox.showinfo("Ваш ход!",title_msg+"Противник сделал свое дело!")
		
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
	
	if not game_over:
		if score<3: 
			messagebox.showerror(title_msg+'Ошибка!','Недостаточно очков для выстрела!')
		else:
			new_state=copy(state)
			if direction=='w':
				for i in reversed(range(r_play1)):
					if new_state[i][c_play1]==3:
						new_state[i][c_play1]=0
						break
					elif new_state[i][c_play1]==play2_number:
						new_state[i][c_play1]=0
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
			refresh_draw(state,new_state,btns)
			state=copy(new_state)
			score=score-3
			root.title(title_msg+"У вас "+str(score)+" очко(а)(ов) действия!")
			game=sendproc()
			if game:
				root.title(title_msg+"У вас "+str(score)+" очко(а)(ов) действия!")
				messagebox.showinfo("Ваш ход!",title_msg+"Противник сделал свое дело!")
	
def skip(event):
	global score
	if not game_over:
		score=0
		root.title(title_msg+"У вас "+str(score)+" очко(а)(ов) действия!")
		game=sendproc()
		if game: 
			root.title(title_msg+"У вас "+str(score)+" очко(а)(ов) действия!")
			messagebox.showinfo("Ваш ход!",title_msg+"Противник сделал свое дело!")
		
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
	
def copy(a):
	b=[[0 for i in range(8)] for j in range(8)]
	for i in range(8):
		for j in range(8):
			b[i][j]=a[i][j]
	return b
	
def sendproc():
	global client
	global state
	global root
	global title_msg
	global score
	global game_over
	
	try:
		if score==0 or gameOver(state):
			if not gameOver(state): 
				messagebox.showinfo("Ваш ход закончился!", title_msg+"Ожидайте хода противника!")
				root.title(title_msg+"Ожидайте хода противника!")
			client.send(json.dumps(state).encode())
			#print("Ожидайте...")
			start=json.loads(client.recv(1024).decode())
			client.send(json.dumps("Okey").encode())
			if start!="Start":
				new_state=json.loads(client.recv(1024).decode())
				refresh_draw(state,new_state,btns)
				root.title(title_msg+"Игра закончилась!")
				messagebox.showinfo("Результат игры:",title_msg+start)
				client.close()
				game_over=True
				return False
			else:
				new_state=json.loads(client.recv(1024).decode())
				refresh_draw(state,new_state,btns)
				state=copy(new_state)
				score=randint(1, 6)
			return True
	except BaseException:
		messagebox.showerror(title_msg+'Ошибка!','Игра не может быть продолжена\n из-за второго игрока или сервера!')
		root.destroy()

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

def f1_control(event):
	if not game_over: game_rules()

def f2_control(event):
	if not game_over: game_control()
	
game_over=False
	
root = Tk()
root.geometry('680x680')
root.resizable(width=False, height=False)
root.protocol("WM_DELETE_WINDOW", quit)

root.bind("<w>", move_up)
root.bind("<s>", move_down)
root.bind("<a>", move_left)
root.bind("<d>", move_right)

root.bind("<Return>", shoot)
root.bind("<space>", skip)
root.bind("<F1>", f1_control)
root.bind("<F2>", f2_control)

SERVER = "localhost" #(localhost в диапазоне 127.0.0.1 — 127.255.255.255)
PORT = 8081 #системные (0—1023), пользовательские (1024—49151) и частные (49152—65535)

try:
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM ,0)
	client.connect((SERVER, PORT))
	
	play1_number=json.loads(client.recv(1024).decode())
	client.send(json.dumps("Okey").encode())
	play2_number=json.loads(client.recv(1024).decode())
	client.send(json.dumps("Okey").encode())
	state=json.loads(client.recv(1024).decode())
	client.send(json.dumps("Okey").encode())
	
	btns=[[None for c in range(8)] for r in range(8)]
	direction='w'
	image_play1_w= ImageTk.PhotoImage(file="play1/play1_w.jpg") if play1_number==1 else ImageTk.PhotoImage(file="play2/play2_w.jpg")  
	image_play1_s= ImageTk.PhotoImage(file="play1/play1_s.jpg") if play1_number==1 else ImageTk.PhotoImage(file="play2/play2_s.jpg")  
	image_play1_d= ImageTk.PhotoImage(file="play1/play1_d.jpg") if play1_number==1 else ImageTk.PhotoImage(file="play2/play2_d.jpg")  
	image_play1_a= ImageTk.PhotoImage(file="play1/play1_a.jpg") if play1_number==1 else ImageTk.PhotoImage(file="play2/play2_a.jpg")  
	image_play1=image_play1_w
	
	image_play2=ImageTk.PhotoImage(file="play2/play2_s.jpg") if play1_number==1 else ImageTk.PhotoImage(file="play1/play1_s.jpg")
	image_stena=ImageTk.PhotoImage(file="stena.jpg")
	image_space=ImageTk.PhotoImage(file="space.jpg")
	
	if play1_number==1: title_msg="Красный игрок: \n"
	else: title_msg="Синий игрок: \n"
	
	score=randint(1, 6)
	root.title(title_msg+"У вас "+str(score)+" очков действия!")
	
	print("Ожидайте...")
	start=json.loads(client.recv(1024).decode())
	client.send(json.dumps("Okey").encode())
	state=json.loads(client.recv(1024).decode())
	
	init_draw(state,btns)
	game_rules()
	game_control()
	root.mainloop()
	
except BaseException:
		messagebox.showerror('Ошибка!','Игра не может быть продолжена\n из-за второго игрока или сервера!')
		root.destroy()
	
client.close()
