import RPi.GPIO as IO

IO.setwarnings(False)
IO.setmode (IO.BCM)

IO.setup(20,IO.IN)
ultimo_estado = None
distancia = 0
barreiras = 9
diametro_roda = 12.0
direcao = 1 #frente=1, re=-1

if(IO.input(20)):
	ultimo_estado = 1

while 1:
	if IO.input(20)!=ultimo_estado:
		ultimo_estado = IO.input(20)
		if IO.input(20) == 1:
			distancia+=diametro_roda*direcao/barreiras
	print("distancia=",distancia)
