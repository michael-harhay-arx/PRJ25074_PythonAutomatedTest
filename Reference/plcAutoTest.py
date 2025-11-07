from pylogix import PLC
from time import sleep


# CTS functions
def nest1_cylinder_move():
  current = plc.Read('Program:MainProgram.Nest1Cylinder.PB')
  plc.Write('Program:MainProgram.Nest1Cylinder.PB', not current.Value)

def nest2_cylinder_move():
  current = plc.Read('Program:MainProgram.Nest2Cylinder.PB')
  plc.Write('Program:MainProgram.Nest2Cylinder.PB', not current.Value)

def simulate_cts1_test():
  sleep(1.5)
  nest1_cylinder_move()
  sleep(3.0)
  nest1_cylinder_move()
  sleep(1.5)

def simulate_cts2_test():
  sleep(1.5)
  nest2_cylinder_move()
  sleep(3.0)
  nest2_cylinder_move()
  sleep(1.5)


# Robot functions
def robot_ungrip():
  plc.Write('Program:MainProgram.RobotGripper.PB', False)
  sleep(0.2)

def robot_grip():
  plc.Write('Program:MainProgram.RobotGripper.PB', True)
  sleep(0.2)

def robot_move(target):
  plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', target, datatype=199)
  
  sleep(0.3)

  while True:
    inPos = plc.Read('Program:MainProgram.RobotOutputs.ob_InPos', datatype=193)
    if inPos.Value == 1:
      break
    sleep(0.1)

  sleep(0.3)


# Main test function
def start_test():

  # Init
  print("\nStatus: Initializing")
  plc.Write('Program:MainProgram.RobotInputs.ib_Reset', 1, datatype=193)
  sleep(1.0)
  plc.Write('Program:MainProgram.RobotInputs.ib_Reset', 0, datatype=193)
  robot_ungrip()
  plc.Write('Program:MainProgram.RobotInputs.ib_Start', 1, datatype=193)
  robot_move(0)

  # BARCODE -> FAIL
  print("\nSequence: BARCODE -> FAIL") 
  plc.Write('Program:MainProgram.RobotInputs.ib_Start', 1, datatype=193)
  robot_grip()
  robot_move(1)  # BARCODE

  robot_move(5)  # FAIL
  robot_ungrip()
  robot_move(0)  # LOADING

  # NEST1 -> FAIL
  print("\nSequence: NEST1 -> FAIL") 
  robot_move(0)
  robot_grip()
  robot_move(1)  # BARCODE

  robot_move(2)  # NEST1
  robot_ungrip()
  robot_move(1)  # BARCODE
  simulate_cts1_test()
  robot_move(2)  # NEST1
  robot_grip()

  robot_move(5)  # FAIL
  robot_ungrip()
  robot_move(0)  # LOADING

  # NEST1 -> PASS
  print("\nSequence: NEST1 -> PASS") 
  robot_move(0)
  robot_grip()
  robot_move(1)  # BARCODE

  robot_move(2)  # NEST1
  robot_ungrip()
  robot_move(1)  # BARCODE
  simulate_cts1_test()
  robot_move(2)  # NEST1
  robot_grip()

  robot_move(4)  # PASS ----> FIX
  robot_ungrip()
  robot_move(0)  # LOADING

  # NEST2 -> FAIL
  print("\nSequence: NEST2 -> FAIL") 
  robot_move(0)
  robot_grip()
  robot_move(1)  # BARCODE

  robot_move(3)  # NEST2
  robot_ungrip()
  robot_move(1)  # BARCODE
  simulate_cts2_test()
  robot_move(3)  # NEST2
  robot_grip()

  robot_move(5)  # FAIL
  robot_ungrip()
  robot_move(0)  # LOADING

  # NEST2 -> PASS
  print("\nSequence: NEST2 -> PASS") 
  robot_move(0)
  robot_grip()
  robot_move(1)  # BARCODE

  robot_move(3)  # NEST2
  robot_ungrip()
  robot_move(1)  # BARCODE
  simulate_cts2_test()
  robot_move(3)  # NEST2
  robot_grip()

  robot_move(4)  # PASS
  robot_ungrip()
  robot_move(0)  # LOADING

  # FAIL -> NESTS
  print("\nSequence: FAIL -> NESTS")
  robot_move(5)  # FAIL
  robot_move(2)  # NEST1
  robot_move(5)  # FAIL
  robot_move(3)  # NEST2

  # PASS -> NESTS
  print("\nSequence: FAIL -> NESTS")
  robot_move(4)  # PASS
  robot_move(2)  # NEST1
  robot_move(4)  # PASS
  robot_move(3)  # NEST2

  # NESTS -> LOADING
  print("\nSequence: NESTS -> LOADING")
  robot_move(3)  # NEST2
  robot_move(4)  # LOADING
  robot_move(2)  # NEST1
  robot_move(4)  # LOADING

  # NESTS -> NESTS
  print("\nSequence: NESTS -> NESTS")
  robot_move(3)  # NEST2
  robot_move(2)  # NEST1
  robot_move(3)  # NEST2
  robot_move(0)  # LOADING


  
if __name__ == '__main__':
  print("\nInitializing PLC...")
  plc = PLC()
  plc.IPAddress = '192.168.250.1'

  print("\nRunning test sequences...")
  start_test()
        
