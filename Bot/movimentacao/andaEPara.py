import time
import pigpio
import RPi.GPIO as IO

from leitura_pwm import reader

# wave_PWM.py
# 2016-03-19
# Public Domain

"""
This script shows how to use waves to generate PWM with a
set frequency on any spare GPIO.

Note that only one wave can be transmitted at a time.  So if
waves are being used to generate PWM they can't also be used
at the same time for another purpose.

The frequency is defined by the number of cycles per second.

A wave is generated of length 1000000/frequency microseconds.
The GPIO are switched on and off within the wave to set the
duty cycle for each GPIO.  The wave is repeatedly transmitted.

Waves have a resolution of one microsecond.

You will only get the requested frequency if it divides
exactly into 1000000.

For example, suppose you want a frequency of 7896 cycles per
second.  The wave length will be 1000000/7896 or 126 (for an
actual frequency of 7936.5) and there will be 126 steps
between off and fully on.

One function is provided:

set_dc(channel, dc)

channel: is 0 for the first GPIO, 1 for the second, etc.
     dc: is the duty cycle which must lie between 0 and the
         number of steps.
"""

FREQ=4000 # The PWM cycles per second.

PWM1=22 #porta motores
PWM2=23 #porta servo
PWM_READ=4 #porta receptor

#limites servo
MIN_WIDTH=1200
MAX_WIDTH=1800

GPIO=[PWM1]

_channels = len(GPIO)

_dc=[0]*_channels

_micros=1000000/FREQ

old_wid = None

def set_dc(channel, dc):

   global old_wid

   if dc < 0:
      dc = 0
   elif dc > _micros:
      dc = _micros

   _dc[channel] = dc

   for c in range(_channels):
      d = _dc[c]
      g = GPIO[c]
      if d == 0:
         pi.wave_add_generic([pigpio.pulse(0, 1<<g, _micros)])
      elif d == _micros:
         pi.wave_add_generic([pigpio.pulse(1<<g, 0, _micros)])
      else:
         pi.wave_add_generic(
            [pigpio.pulse(1<<g, 0, d), pigpio.pulse(0, 1<<g, _micros-d)])

   new_wid = pi.wave_create()

   if old_wid is not None:

      pi.wave_send_using_mode(new_wid, pigpio.WAVE_MODE_REPEAT_SYNC)

      # Spin until the new wave has started.
      while pi.wave_tx_at() != new_wid:
         pass

      # It is then safe to delete the old wave.
      pi.wave_delete(old_wid)

   else:

      pi.wave_send_repeat(new_wid)

   old_wid = new_wid



pi = pigpio.pi()
IO.setwarnings(False)
IO.setmode (IO.BCM)

IO.setup(21,IO.IN)
ultimo_estado = None
distancia = 0
barreiras = 9
diametro_roda = 12.4
direcao = 1 #frente=1, re=-1

if not pi.connected:
   exit(0)

p1 = reader(pi, PWM_READ)

# Need to explicity set wave GPIO to output mode.

for g in GPIO:
   pi.set_mode(g, pigpio.OUTPUT)

try:
   pi.set_servo_pulsewidth(PWM2, MIN_WIDTH)
   while p1.pulse_width() < 2000:
       print("aguardando")
       time.sleep(0.1)
   if p1.pulse_width() > 1800:
      while(distancia < 50):
         if p1.pulse_width() > 1800:
            set_dc(0, 100)
            if IO.input(21)!=ultimo_estado:
               ultimo_estado = IO.input(21)
               if IO.input(21) == 1:
                  time.sleep(0.001)
                  if IO.input(21) == 1:
                     distancia+=diametro_roda*direcao/barreiras
                     print("distancia=",distancia)
         else:
            set_dc(0, 0)
            time.sleep(0.1)
   set_dc(0, 0)
   pi.set_servo_pulsewidth(PWM2, (MIN_WIDTH+MAX_WIDTH)/2)
   """
   pi.set_servo_pulsewidth(PWM2, MIN_WIDTH)
   while(distancia<2000):
      if p1.pulse_width > 1500:
	 set_dc(0,250)
         if IO.input(21)!=ultimo_estado:
            ultimo_estado = IO.input(21)
            time.sleep(0.001)
            if IO.input(21) == 1:
               time.sleep(0.001)
               if IO.input(21) == 1:
                  distancia+=diametro_roda*direcao/barreiras
                  print("distancia=",distancia)
      else:
         set_dc(0,0)

   #para motores e centraliza servo
   pi.set_servo_pulsewidth(PWM2, (MIN_WIDTH+MAX_WIDTH)/2)
   set_dc(0,0)
   """
except(KeyboardInterrupt):
   pi.set_servo_pulsewidth(PWM2, (MIN_WIDTH+MAX_WIDTH)/2)
   set_dc(0,0)
   pi.wave_tx_stop()

   if old_wid is not None:
      pi.wave_delete(old_wid)

   pi.stop()

pi.wave_tx_stop()

if old_wid is not None:
   pi.wave_delete(old_wid)

pi.stop()
