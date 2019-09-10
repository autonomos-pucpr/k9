import RPi.GPIO as IO
import time

IO.setwarnings(False)
IO.setmode (IO.BCM)

IO.setup(20,IO.IN)
ultimo_estado = None
tempo_ultima_barreira = None
rpm = [0]*4


if(IO.input(20)):
	ultimo_estado = 1
	tempo_ultima_barreira = time.time()

time.sleep(0.001)
while 1:
	if IO.input(20)!=ultimo_estado:
		ultimo_estado = IO.input(20)
		if IO.input(20) == 1:
			tempo_atual = time.time()
			rpm.insert(0,1/(tempo_atual-tempo_ultima_barreira))
			rpm.pop(3)
			tempo_ultima_barreira = tempo_atual
	time.sleep(0.001)
	print("rpm = ",sum(rpm)/len(rpm),"estado = ",ultimo_estado,"ultima barreira = ",tempo_ultima_barreira)
