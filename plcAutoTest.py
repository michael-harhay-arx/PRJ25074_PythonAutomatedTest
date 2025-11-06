import sys
from pylogix import PLC
from time import sleep
import time

plc = PLC()

def nest1_cylinder_move(self):
  current = plc.Read('Program:MainProgram.Nest1Cylinder.PB')
  self.plc.Write('Program:MainProgram.Nest1Cylinder.PB', not current.Value)

def nest2_cylinder_move(self):
  current = plc.Read('Program:MainProgram.Nest2Cylinder.PB')
  self.plc.Write('Program:MainProgram.Nest2Cylinder.PB', not current.Value)
  
def plc_connect(self):
  self.plc.IPAddress = self.plc_ip_address_edit.text()
  self.cts_controls_group.setEnabled(True)
  self.robot_controls_group.setEnabled(True)
  
def move_to_position(self, position, timeout=10.0):
  self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', position, datatype=199)
  
  start_time = time.time()
  while time.time() - start_time < timeout:
    inPos = self.plc.Read('Program:MainProgram.RobotOutputs.ob_InPos', datatype=193)
    if inPos.Value == 1:
        return True
    sleep(0.1)  # non-blocking

  return False # returns false if timeout occurs
  
def robot_ungrip(self):
  self.plc.Write('Program:MainProgram.RobotGripper.PB', False)
  sleep(0.2)

def robot_grip(self):
  self.plc.Write('Program:MainProgram.RobotGripper.PB', True)
  sleep(0.2)

def robot_move(self, target):
  self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', target, dataype=199)

def update_status(self, status):
  self.status_label.setText(status)

def simulate_cts_test(self):
  sleep(1.0)
  self.nest1_cylinder_clicked()
  sleep(3.0)
  self.nest1_cylinder_clicked()
  sleep(1.0)

def start_test(self):

  # Init
  print("Status: Initializing")
  self.plc.Write('Program:MainProgram.RobotInputs.ib_Reset', 1, datatype=193)
  sleep(1.0)
  self.plc.Write('Program:MainProgram.RobotInputs.ib_Reset', 0, datatype=193)
  self.robot_ungrip()
  self.move_to_position(0)
  
  # Barcode -> fail
  self.update_status("BARCODE -> FAIL") 
  self.plc.Write('Program:MainProgram.RobotInputs.ib_Start', 1, datatype=193)
  self.robot_grip()
  self.move_to_position(1)  # BARCODE

  self.move_to_position(5)  # FAIL
  self.robot_ungrip()
  self.move_to_position(0)  # LOADING


  # Nest 1 -> fail
  # self.update_status("NEST1 -> FAIL") 
  # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 0, datatype=199) # LOADING
  # self.plc.Write('Program:MainProgram.RobotInputs.ib_Start', 1, datatype=193)
  # self.robot_grip()
  # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 1, datatype=199) # BARCODE
  # sleep(2.0)

  # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 2, datatype=199) # NEST1
  # self.robot_ungrip()
  # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 1, datatype=199) # BARCODE
  # simulate_cts_test()
  # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 2, datatype=199) # NEST1
  # self.robot_grip()

  # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 5, datatype=199) # FAIL
  # self.robot_ungrip()
  # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 0, datatype=199) # LOADING


  # # Nest 1 -> pass
  # self.update_status("NEST1 -> PASS") 
  # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 0, datatype=199) # LOADING
  # self.plc.Write('Program:MainProgram.RobotInputs.ib_Start', 1, datatype=193)
  # self.robot_grip()
  # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 1, datatype=199) # BARCODE
  # sleep(2.0)

  # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 2, datatype=199) # NEST1
  # self.robot_ungrip()
  # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 1, datatype=199) # BARCODE
  # simulate_cts_test()
  # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 2, datatype=199) # NEST1
  # self.robot_grip()

  # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 4, datatype=199) # PASS
  # self.robot_ungrip()
  # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 0, datatype=199) # LOADING


  
if __name__ == '__main__':
  plc = PLC()
  start_test()
        
