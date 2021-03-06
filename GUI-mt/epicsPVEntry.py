"""
   This module provides a class library for a GUI entry field widget bound to an Epics PV. The PV is monitored
   and the field is updated when the PV changes

Author:         John Skinner
Created:        Nov, 2 2009
Modifications:
"""

import epicsPV
from mtTkinter import *
import Pmw
from beamline_support import *
import time

class epicsPVEntry:
   """
   This module provides a class library for a GUI entry field widget bound to an Epics PV. The PV is monitored
   and the field is updated when the PV changes

   """
   is_drawn = 0
   
   def __init__(self, pvname,parent,input_width,type_string,precision = 2):
      """

      Inputs:
         pvname:
            The name of the epics process variable.
         parent:
            The container to place the entry widget.
         input_width:
         type_string:
           'real' or 'int' or 'none'


      Example:
         omega_move = epicsPVEntry("x12c_comm:omega",diffstat_moveframe,10,'real')
         omega_move.getEntry().pack(side=LEFT)


      """
      self.pv_statestrings = [] #for enums, b/c this CaChannel ignores type conversions on callback returns
      self.precision = precision
      self.entry_var = StringVar()            
      self.entry_pv = pvCreate(pvname,self._conCB)
      time.sleep(0.05)
      if (ca.dbf_text(self.entry_pv.field_type()) == "DBF_ENUM"):
        self.entry_pv.getControl()
        self.pv_statestrings = getattr(self.entry_pv.callBack,'pv_statestrings')
        self.entry_var.set(pvGet(self.entry_pv))
      else:
        self._set_entry_var_with_precision(pvGet(self.entry_pv))
      if (type_string == "none"):
        self.entry = Pmw.EntryField(parent,value=str(pvGet(self.entry_pv)))
      else:
        self.entry = Pmw.EntryField(parent,value=str(pvGet(self.entry_pv)),validate = {'validator':type_string})
      self.entry.component('entry').configure(width=input_width,textvariable=self.entry_var)
      add_callback(self.entry_pv,self._entry_pv_movingCb,"")
      
   def _conCB(self,epics_args, user_args):
     if (epics_args[1] == 6):
       if (epicsPVEntry.is_drawn):
         self.entry.component('entry').configure(background="#729fff")
     elif (epics_args[1] == 7):
       self.entry_var.set("----")
       self.entry.component('entry').configure(background="white")



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
         

   def _entry_pv_movingCb(self,epics_args, user_args):
#      print "in callback " + str(epics_args['pv_value'])
      if not (epicsPVEntry.is_drawn):
        return
      if (ca.dbf_text(epics_args['type']) == "DBF_CHAR"):
        self.entry_var.set(waveform_to_string(epics_args['pv_value']))
      elif (ca.dbf_text(epics_args['type']) == "DBF_ENUM"):
        if (self.pv_statestrings):
          self.entry_var.set(self.pv_statestrings[epics_args['pv_value']])
        else:
          self.entry_var.set(epics_args['pv_value'])
      else:
        self._set_entry_var_with_precision(epics_args['pv_value'])
#        self.entry_var.set("%.4f" % (epics_args['pv_value']))

        
   def pack(self,side=LEFT,padx=0,pady=0): #pass the params in
      self.entry.pack(side=side,padx=padx,pady=pady)

   def getEntry(self):
      return self.entry

   def getField(self):
      return self.entry_var.get()
   
   def setField(self,value):
      self.entry_var.set(value)
   
   def setColor(self,color_string):
      self.entry.component('entry').configure(background=color_string)

  
