import sys
import importlib
from time import sleep
from pylogix import PLC


# Config (Update before running)
# 1) set IP, 2) import correct files, 3) updates test dictionary to include all tests
plcIP = '192.168.251.1'
import BarcodeTest, NestEngageTest, PathTest, PositionTest
testsDict = {1 : "PositionTest",
             2 : "PathTest",
             3 : "NestEngageTest",
             4 : "BarcodeTest"}

plc = PLC()
plc.IPAddress = plcIP

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
  sleep(1.0)

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


# Barcode functions
def scan_barcode():
  plc.Write('Program:MainProgram.Barcode_TriggerInput', 1, datatype=193)

  while True:
    scannerDone = plc.Read('Program:MainProgram.Barcode_Read_Complete', datatype=193)

    if scannerDone:
      break
    
  plc.Write('Program:MainProgram.Barcode_TriggerInput', 0, datatype=193)
  plc.Write('Program:MainProgram.Barcode_Read_Complete_Clear', 1, datatype=193)
  sleep(0.5)
  plc.Write('Program:MainProgram.Barcode_Read_Complete_Clear', 0, datatype=193)


# Initialization function
def initialize_station():
  print("Initializing...")

  plc.Write('Program:MainProgram.RobotInputs.ib_Reset', 1, datatype=193)   # Reset flag
  sleep(1.0)
  plc.Write('Program:MainProgram.RobotInputs.ib_Reset', 0, datatype=193)

  plc.Write('Program:MainProgram.RobotInputs.ib_Resume', 1, datatype=193)  # Resume flag
  sleep(1.0)
  plc.Write('Program:MainProgram.RobotInputs.ib_Resume', 0, datatype=193)

  robot_ungrip()
  plc.Write('Program:MainProgram.RobotInputs.ib_Start', 1, datatype=193)   # Start flag
  robot_move(0)


# Main
if __name__ == '__main__':
  print("-------------------- PRJ25074 Capability Tester --------------------\n\nPlease select a test to run:")

  # Build test selection prompt
  testPrompt = ""
  numTests = len(testsDict)

  if (numTests > 0):
    for i in range (1, numTests + 1):
      testPrompt += str(i) + ") " + testsDict[i] + "\t\t"
    
    testPrompt += "[type "
    for i in range (1, numTests + 1):
      testPrompt += str(i) + "/"
    testPrompt = testPrompt[:-1]
    testPrompt += "]: "

  else:
    print("No tests loaded. Exiting...")
    sleep(2)
    sys.exit()

  # Get desired test
  testNum = input(testPrompt)
  testNum = int(testNum)
  testName = testsDict[testNum]
  print("\nNow running: " + testName)

  # Initialize PLC
  #plc = PLC()
  #plc.IPAddress = plcIP
  initialize_station()

  # Start test
  module = importlib.import_module(testName)
  if hasattr(module, testName):
    func = getattr(module, testName)
    func(plc)
  else:
    print(f"No such function '{testName}' in " + testName + ".py.")
        
  print(testName + " complete.")