import sys
import importlib
from time import sleep
from pylogix import PLC
from datetime import datetime


# Config (Update before running)
# 1) set IP, 2) import correct files, 3) updates test dictionary to include all tests
plcIP = '192.168.251.1'
import PositionTest, PathTest, NestEngageTest, BarcodeTest, ConveyorTest
testsDict = {1 : "PositionTest",
             2 : "PathTest",
             3 : "NestEngageTest",
             4 : "BarcodeTest",
             5 : "ConveyorTest"}

plc = PLC()
plc.IPAddress = plcIP


# CTS functions
def nest_cylinder_move(nestIndex, extended, logName):
  plc.Write(f'Program:MainProgram.Nest{nestIndex}Cylinder.PB', extended, datatype=193)
  sleep(1)

  # Check that sensors are correctly triggered
  fault = 0
  sensorTop = plc.Read(f'Local:3:I.Pt0{3+2*(nestIndex - 1)}.Data', datatype=193)
  sensorBottom = plc.Read(f'Local:3:I.Pt0{4+2*(nestIndex - 1)}.Data', datatype=193)
  print("sensortop: " + str(sensorTop.Value))
  print("sensorBot: " + str(sensorBottom.Value))

  if extended == 0 and (sensorTop.Value != 1 or sensorBottom.Value != 0):
    fault = 1
  if extended == 1 and (sensorTop.Value != 0 or sensorBottom.Value != 1):
    fault = 1

  if extended == 0:
    direction = "up"
  else:
    direction = "down"

  with open(logName, "a") as file:
    if fault != 0:
      file.write(f"Nest {nestIndex}: Fault occurred moving {direction}.\n")
    else:
      file.write(f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}: Nest {nestIndex}: Movement {direction} successful.\n")

def simulate_cts_test(nestIndex, logName):
  sleep(1.0)
  nest_cylinder_move(nestIndex, 1, logName)
  sleep(2.0)
  nest_cylinder_move(nestIndex, 0, logName)
  sleep(1.0)


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
      barcode = plc.Read('Program:MainProgram.Barcode_Result_Data', datatype=194)
      with open("BarcodeLog.txt", "a") as file:
        file.write("Barcode scanned: " + str(barcode))

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
  initialize_station()

  # Start test
  module = importlib.import_module(testName)
  if hasattr(module, testName):
    func = getattr(module, testName)
    func(plc)
  else:
    print(f"No such function '{testName}' in " + testName + ".py.")
        
  print(testName + " complete.")