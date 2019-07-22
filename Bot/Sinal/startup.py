#!/usr/bin/env python

# read_PWM.py
# 2015-12-08
# Public Domain

import time
import pigpio # http://abyz.co.uk/rpi/pigpio/python.html

## The PWM cycles per second ##
FREQ=63 
###############################

## Pin with the PWM signal generated ##
PWM1=21 
PWM2=22
PWM3=23

GPIO=[PWM1, PWM2, PWM3]
#######################################

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


class reader:
   """
   A class to read PWM pulses and calculate their frequency
   and duty cycle.  The frequency is how often the pulse
   happens per second.  The duty cycle is the percentage of
   pulse high time per cycle.
   """
   def __init__(self, pi, gpio, weighting=0.0):
      """
      Instantiate with the Pi and gpio of the PWM signal
      to monitor.

      Optionally a weighting may be specified.  This is a number
      between 0 and 1 and indicates how much the old reading
      affects the new reading.  It defaults to 0 which means
      the old reading has no effect.  This may be used to
      smooth the data.
      """
      self.pi = pi
      self.gpio = gpio

      if weighting < 0.0:
         weighting = 0.0
      elif weighting > 0.99:
         weighting = 0.99

      self._new = 1.0 - weighting # Weighting for new reading.
      self._old = weighting       # Weighting for old reading.

      self._high_tick = None
      self._period = None
      self._high = None

      pi.set_mode(gpio, pigpio.INPUT)

      self._cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cbf)

   def _cbf(self, gpio, level, tick):

      if level == 1:

         if self._high_tick is not None:
            t = pigpio.tickDiff(self._high_tick, tick)

            if self._period is not None:
               self._period = (self._old * self._period) + (self._new * t)
            else:
               self._period = t

         self._high_tick = tick

      elif level == 0:

         if self._high_tick is not None:
            t = pigpio.tickDiff(self._high_tick, tick)

            if self._high is not None:
               self._high = (self._old * self._high) + (self._new * t)
            else:
               self._high = t

   def frequency(self):
      """
      Returns the PWM frequency.
      """
      if self._period is not None:
         return 1000000.0 / self._period
      else:
         return 0.0

   def pulse_width(self):
      """
      Returns the PWM pulse width in microseconds.
      """
      if self._high is not None:
         return self._high
      else:
         return 0.0

   def duty_cycle(self):
      """
      Returns the PWM duty cycle percentage.
      """
      if self._high is not None:
         return 100.0 * self._high / self._period
      else:
         return 0.0

   def cancel(self):
      """
      Cancels the reader and releases resources.
      """
      self._cb.cancel()

if __name__ == "__main__":

   import time
   import pigpio
   import read_PWM

   ## input pins ##
   PWM_GPIO1 = 4
   PWM_GPIO2 = 5
   ################
   RUN_TIME = 60.0
   SAMPLE_TIME = 1.0

   pi = pigpio.pi()

   for g in GPIO:
   	pi.set_mode(g, pigpio.OUTPUT)

   p1 = read_PWM.reader(pi, PWM_GPIO1)
   p2 = read_PWM.reader(pi, PWM_GPIO2)

   start = time.time()

   pi.set_mode(25, pigpio.OUTPUT)

   while (time.time() - start) < RUN_TIME:

      time.sleep(SAMPLE_TIME)

      ## signal information from input pins ##
      ## first pin (4) ## 
      f1 = p1.frequency()
      pw1 = p1.pulse_width()
      dc1 = p1.duty_cycle()
      
      while (pw1 == 0):
	      pi.write(25, 1)
	      time.sleep(0.5)
	      pi.write(25, 0)
	      time.sleep(0.5)
	      pw1 = p1.pulse_width()
	  
	      
      pi.write(25, 1)
      ## second pin (5) ## 
      #f2 = p2.frequency()
      #pw2 = p2.pulse_width()
      #dc2 = p2.duty_cycle()
      ###################
      #################################################
      ## setting signal information for the output pins ##
      ## first pin (21) ##  
      set_dc(0, pw1)
      ## first pin (22) ##  
      #set_dc(1, pw2)
      ####################
      ####################################################
      print("f1={:.1f} pw1={} dc1={:.2f}".format(f1, int(pw1+0.5), dc1))
      print("##########################################################")
      #print("f2={:.1f} pw2={} dc2={:.2f}".format(f2, int(pw2+0.5), dc2))
      #print("##########################################################")

   pi.wave_tx_stop()

   p.cancel()

   pi.stop()
