"""
   This module provides a class library for a GUI label field widget bound to an Epics motor record instance. The RBV is monitored
   and the field is updated and lit up green when the motor is moving.


Author:         John Skinner
Created:        Nov, 2 2009
Modifications:
"""

import epicsPV
from mtTkinter import *
import Pmw
import time
from beamline_support import *

class epicsMotorLabel:
   """
   This module provides a class library for a GUI label field widget bound to an Epics motor record instance. The RBV is monitored
   and the field is updated and lit up green when the motor is moving.

   """
   is_drawn = 0
   
   def __init__(self, pvname,parent,input_width,precision = 2):
      """

      Inputs:
         pvname:
            The name of the epics process variable.
         parent:
            The container to place the entry widget.
         input_width:
         precision:

      Example:
        tableHrz = epicsMotorLabel("x12c:table_z",table_x_frame,11)
        tableHrz.pack(side=LEFT)

      """
      self.precision = precision      
      self.entry_var = StringVar()
      self.entry_pv = pvCreate(pvname+".RBV",self._conCB)
      time.sleep(0.05)
      self._set_entry_var_with_precision(pvGet(self.entry_pv))      
      self.entry = Label(parent,textvariable=self.entry_var,width=input_width)
      add_callback(self.entry_pv,self._entry_pv_movingCb,self.entry_var)
      self.entry_dmov_pv = pvCreate(pvname+".DMOV")
      add_callback(self.entry_dmov_pv,self._entry_pv_dmovCb,[])
      


   def _conCB(self,epics_args, user_args):
     if (epics_args[1] == 6):
       if (epicsMotorLabel.is_drawn):
         self.entry.configure(background="#729fff")
     elif (epics_args[1] == 7):
       self.entry_var.set("----")
       self.entry.configure(background="white")



   def _entry_pv_movingCb(self,epics_args, user_args):
#      print "in callback " + str(epics_args['pv_value'])
      if not (epicsMotorLabel.is_drawn):
        return
      self._set_entry_var_with_precision(epics_args['pv_value'])         


   def _entry_pv_dmovCb(self,epics_args, user_args):
#      print "in callback " + str(epics_args['pv_value'])
      if not (epicsMotorLabel.is_drawn):
        return
      if (epics_args['pv_value'] == 1):
        self.entry.configure(background="#729fff")
      else:
        self.entry.configure(background="green")         

 
   def _set_entry_var_with_precision(self,inval):
      try:
        val = float(inval)
        if (self.precision == 0):
           self.entry_var.set("%.0f" % val)
        elif (self.precision == 1):
           self.entry_var.set("%.1f" % val)
        elif (self.precision == 2):
           self.entry_var.set("%.2f" % val)
        elif (self.precision == 3):
           self.entry_var.set("%.3f" % val)
        elif (self.precision == 4):
           self.entry_var.set("%.4f" % val)
        else:
           self.entry_var.set("%.5f" % val)
      except TypeError:
         print "type error"
         self.entry_var.set(waveform_to_string(val))
         

   def pack(self,side=LEFT,padx=0,pady=0): #pass the params in
      self.entry.pack(side=side,padx=padx,pady=pady)

   def getField():
      return self.entry_var.get()
   
   def putField(value):
      self.entry_var.put(value)
   
   def setColor(color_string):
      self.entry.configure(background=color_string)

   
