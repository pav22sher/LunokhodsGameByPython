# -*- coding: utf-8 -*-
import socket
import json
from random import *

def gameOver1(state):
	for r in range(8):
		for c in range(8):
			if state[r][c]==1:
				return False
	else: return True

def gameOver2(state):
	for r in range(8):
		for c in range(8):
			if state[r][c]==2:
				return False
	else: return True

def flip(a):
	b=[[0 for i in range(8)] for j in range(8)]
	for i in range(8):
		for j in range(8):
			b[i][j]=a[abs(i-7)][abs(j-7)]
	return b
	
def state_init(state):
	for r in range(8):
		for c in range(8):
			if r==r_play2 and c==c_play2:
				state[r][c]=2
			elif r==r_play1 and c==c_play1:
				state[r][c]=1
			elif (r>0 and r<7) and randint(0, 1)==1:
				state[r][c]=3
			else:
				state[r][c]=0

PORT = 8081

json_start=json.dumps("start")
json_stop=json.dumps("stop")
json_lose=json.dumps("Вы проиграли!")
json_win=json.dumps("Вы победили!")

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)
server.bind(("localhost", PORT))
server.listen(2)
print ("Ожидаем подключения игроков...")
conn1, adr1 = server.accept()
print ("Первый игрок подключился...")
conn2, adr2 = server.accept()
print ("Второй игрок подключился...")

state=[[0 for c in range(8)] for r in range(8)]
c_play1=randint(0, 7)
r_play1=7
c_play2=randint(0, 7)
r_play2=0
state_init(state)
win_num=0

try:
	conn1.send(json.dumps(1).encode())
	json.loads(conn1.recv(1024).decode())
	conn1.send(json.dumps(2).encode())
	json.loads(conn1.recv(1024).decode())
	conn1.send(json.dumps(state).encode())
	json.loads(conn1.recv(1024).decode())
	
	conn2.send(json.dumps(2).encode())
	json.loads(conn2.recv(1024).decode())
	conn2.send(json.dumps(1).encode())
	json.loads(conn2.recv(1024).decode())
	conn2.send(json.dumps(flip(state)).encode())
	json.loads(conn2.recv(1024).decode())
	
	while True:
		conn1.send(json.dumps("Start").encode())
		json.loads(conn1.recv(1024).decode())
		conn1.send(json.dumps(state).encode())
		state = json.loads(conn1.recv(1024).decode())
		if gameOver2(state):
			win_num=1
			break
		
		conn2.send(json.dumps("Start").encode())
		json.loads(conn2.recv(1024).decode())
		conn2.send(json.dumps(flip(state)).encode())
		state = flip(json.loads(conn2.recv(1024).decode()))
		if gameOver1(state):
			win_num=2
			break
	
	if win_num==1:
		conn1.send(json_win.encode())
		conn2.send(json_lose.encode())
	else:
		conn1.send(json_lose.encode())
		conn2.send(json_win.encode())
	
	json.loads(conn1.recv(1024).decode())
	conn1.send(json.dumps(state).encode())
	json.loads(conn2.recv(1024).decode())
	conn2.send(json.dumps(flip(state)).encode())
		
	print("Игра закончилась!")	
		
except BaseException:
	print("Ошибка!!!")

conn1.close()
conn2.close()
server.close()