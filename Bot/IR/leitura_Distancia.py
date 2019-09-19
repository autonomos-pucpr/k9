import RPi.GPIO as IO
import time

IO.setwarnings(False)
IO.setmode (IO.BCM)

IO.setup(21,IO.IN)
ultimo_estado = None
distancia = 0
barreiras = 9
diametro_roda = 12.0
direcao = 1 #frente=1, re=-1

if(IO.input(21)):
	ultimo_estado = 1

while 1:
	if IO.input(21)!=ultimo_estado:
		ultimo_estado = IO.input(21)
		if IO.input(21) == 1:
			time.sleep(0.001)
			if(IO.input(21)) == 1:
				distancia+=diametro_roda*direcao/barreiras
			   	print(distancia)
