from movimentacao import inicializar, mover, parar, finalizar, pulso_receptor
#from navegacao import move_to_pose

import time

pi, p1 = inicializar()
distancia = 0.248

try:
   while(pulso_receptor(p1)<1600):
      print("Aguardando...")
      time.sleep(0.1)
   while(1):
      for ang in range(1200, 1800, 100):
          if(pulso_receptor(p1) > 1900):
             mover(distancia, ang, 1, pi)
             print(ang)
             time.sleep(0.01)
          else:
             parar(pi)
             while(pulso_receptor(p1) < 1600):
                print("Em espera", ang)
                time.sleep(0.1)
      for ang in range(1800, 1200, -100):
          if(pulso_receptor(p1) > 1900):
             mover(distancia, ang, 1, pi)
             print(ang)
             time.sleep(0.01)
          else:
             parar(pi)
             while(pulso_receptor(p1) < 1600):
                print("Em espera", ang)
                time.sleep(0.1)

except(KeyboardInterrupt):
   parar(pi)

finalizar(pi)
