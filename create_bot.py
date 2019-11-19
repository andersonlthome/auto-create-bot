from pynput.keyboard import Key, Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
import time, sys, re, os 
from datetime import datetime,timedelta

print('Code that create code for a Bot that record clicks, scroll and typing, instruction:\n'+
		'- ESC to finish.\n'+
		'- Alt Gr to add where you wanna modificate the code after.\n'+
		'- Home will restart record, and erase the past code.')

bot = input('The name of this bot will be:')
name = bot+'.py'
caminho = os.path.abspath(os.path.dirname(__file__))
i=8 #numero de linhas iniciais
time.sleep(0.2) #tempo pra não pegar o enter

def tempoIni(tempoIni):
	tempo = open(caminho+'/createbottemp.txt','w')
	tempo.write(str(tempoIni))
	tempo.close()	

def deltaT(tempoFim):
	tempo = open(caminho+'/createbottemp.txt','r')
	tempoIni = datetime.strptime(tempo.readline(),'%Y-%m-%d %H:%M:%S.%f')
	tempo.close()
	t = (tempoFim - tempoIni).total_seconds() 	
	return t 	

def on_click(x, y, button, pressed):	
	botao = str(button)
	a = open(caminho+'/'+name, 'a')
	global i	
	if botao == 'Button.left':
		posclick = 'mouse.position = ('+str(x)+', '+str(y)+')\n'
		r = open(caminho+'/'+name, 'r')
		ultimoclick = r.readlines()[i-4]
		r.close()
		if not ultimoclick == posclick :
			if pressed:	
				t = deltaT(datetime.now())
				a.write('time.sleep('+str(t)+'*vel)\n')
				a.write(posclick)		
				a.write('mouse.press(Button.left)\n')
				tempoIni(datetime.now())			
			else:
				t = deltaT(datetime.now())
				print('tempo: '+str(t))
				a.write('time.sleep('+str(t)+'*vel)\n')
				a.write('mouse.position = ('+str(x)+', '+str(y)+')\n')
				a.write('mouse.release(Button.left)\n')	
				i += 6		
				print('mouse.position = ('+str(x)+', '+str(y)+' '+botao+')\n')
				tempoIni(datetime.now())
	if botao == 'Button.right':
		posclick = 'mouse.position = ('+str(x)+', '+str(y)+')\n'
		r = open(caminho+'/'+name, 'r')
		ultimoclick = r.readlines()[i-3]
		r.close()
		if not ultimoclick == posclick :
			t = deltaT(datetime.now())
			a.write('time.sleep('+str(t)+'*vel)\n')
			a.write(posclick)	
			a.write('mouse.press(Button.right)\n')
			a.write('mouse.release(Button.right)\n')			
			i += 4
			print('mouse.position = ('+str(x)+', '+str(y)+' '+botao+')\n')
			tempoIni(datetime.now())

def on_scroll(x, y, dx, dy):
	t = deltaT(datetime.now())
	a = open(caminho+'/'+name, 'a')
	a.write('time.sleep('+str(t)+'*vel)\n')
	a.write('mouse.position = ('+str(x)+', '+str(y)+')\n')	
	a.write('mouse.scroll(0, '+str(dy*150)+')\n')
	global i
	i += 4
	print('mouse.position = ('+str(x)+', '+str(y)+')\n')
	print('mouse.scroll(0, '+str(dy*150)+')\n')
	tempoIni(datetime.now())	

def on_release(key):
	global i
	t = deltaT(datetime.now())	
	a = open(caminho+'/'+name, 'a')
	if key == Key.esc:		
		return False # Stop listener
	elif key == Key.alt_gr:
		a.write('#--------------input something\n')
		i += 1
	elif key == Key.home:
		i = 8
		criar()
	else:
		a.write('time.sleep('+str(t)+'*vel)\n')
		a.write('keyboard.press('+str(key)+')\n')
		a.write('keyboard.release('+str(key)+')\n')
		i += 3
		print('{0} pressed'.format(str(key)))
		print('{0} release'.format(str(key)))
		tempoIni(datetime.now())

def listener():
	try:
		with MouseListener(on_click=on_click, on_scroll=on_scroll) as listener:
			with KeyboardListener(on_release=on_release) as listener:
				listener.join() 
	except:
		time.sleep(0.2)
		print('Error: Do it again!')
		listener()	     

def criar():
	arq = open(caminho+'/'+name, 'w')
	arq.close()
	a = open(caminho+'/'+name, 'a')
	a.write('from pynput.mouse import Button, Controller as contmouse\nfrom pynput.keyboard import Key, Controller as contkey\nimport time\nfrom datetime import datetime\nmouse = contmouse()\nkeyboard = contkey()\nvel = 0.9 #fator multiplicador para deixar as acoes mais rapidas\n\n')
	a.close()  
	tempoIni(datetime.now()) #iniciando o tempo 
	listener()   

def main():
	criar() 

if __name__ == '__main__':
    main()