from copyreg import clear_extension_cache
import sys
import importlib
from time import sleep
from pylogix import PLC
from datetime import datetime


# Config (Update before running)
# 1) set IP, 2) import correct files, 3) updates test dictionary to include all tests
plcIP = '192.168.251.1'
import PositionTest, PathTest, NestEngageTest, BarcodeTest, ConveyorTest, Initialize
testsDict = {1 : "PositionTest",
             2 : "PathTest",
             3 : "NestEngageTest",
             4 : "BarcodeTest",
             5 : "ConveyorTest",
             6 : "Initialize"}

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

  with open(logName, "a") as file:
    if extended == 0 and (sensorTop.Value != 1 or sensorBottom.Value != 0):
      fault = 1
      file.write(f"Fault occurred!\nsensorTop should be 1, is: {sensorTop.Value}\nsensorBottom should be 0, is: {sensorBottom.Value}\n")
      print(f"Fault occurred!\nsensorTop should be 1, is: {sensorTop.Value}\nsensorBottom should be 0, is: {sensorBottom.Value}\n")
    if extended == 1 and (sensorTop.Value != 0 or sensorBottom.Value != 1):
      fault = 1
      file.write(f"Fault occurred!\nsensorTop should be 0, is: {sensorTop.Value}\nsensorBottom should be 1, is: {sensorBottom.Value}\n")
      print(f"Fault occurred!\nsensorTop should be 0, is: {sensorTop.Value}\nsensorBottom should be 1, is: {sensorBottom.Value}\n")

  if extended == 0:
    direction = "up"
  else:
    direction = "down"

  with open(logName, "a") as file:
    if fault != 0:
      file.write(f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}: Nest {nestIndex}: Fault occurred moving {direction}.\n")
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
  plc.Write('Program:MainProgram.Robot.REQ', target, datatype=194)
  sleep(0.3)

  while True:
    inPos = plc.Read('Program:MainProgram.RobotInputs.ib_InPos', datatype=193)
    if inPos.Value == 1:
      break
    sleep(0.1)

  sleep(0.3)


# Barcode functions
def scan_barcode(logName):
  sleep(1)
  plc.Write('Program:MainProgram.Barcode_TriggerInput', 1, datatype=193)

  while True:
    scannerDone = plc.Read('Program:MainProgram.Barcode_Read_Complete', datatype=193)

    if scannerDone.Value == 1:
      barcode = plc.Read('Program:MainProgram.Barcode_Result_Data', datatype=194)
      with open(logName, "a") as file:
        barcode_bytes = barcode.Value
        barcode_str = ''.join(chr(b) for b in barcode_bytes if b > 0 and b < 127)
        file.write(f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}: Barcode scanned: {barcode_str}\n")

      break
    
  plc.Write('Program:MainProgram.Barcode_TriggerInput', 0, datatype=193)
  plc.Write('Program:MainProgram.Barcode_Read_Complete_Clear', 1, datatype=193)
  sleep(0.5)
  plc.Write('Program:MainProgram.Barcode_Read_Complete_Clear', 0, datatype=193)


# Sensor functions
def sensor_wait(sensorIndex, sensorHigh, logName):
  sleep(1)
  sensorStatus = plc.Read(f'I_OP220_N3_DUT_PRE_NEST_{sensorIndex}', datatype=193)

  if sensorHigh == 0:
    word = "low"
  else:
    word = "high"

  with open(logName, "a")as file:
    file.write(f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}: Waiting for sensor status to change to {word}... ")
    while sensorHigh != sensorStatus.Value:
      continue
    file.write("Sensor status changed.\n")


# Conveyor function
def conveyor_logic(logName):

  with open(logName, "a") as file:
    # Wait for DUT to be dropped
    conveyorLoaded = plc.Read('I_OP220_N3_CONVEYOR_LOAD', datatype=193)
    while conveyorLoaded.Value != 1:
      print(str(conveyorLoaded.Value))
      conveyorLoaded = plc.Read('I_OP220_N3_CONVEYOR_LOAD', datatype=193)
      sleep(0.1)

    file.write(f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}: DUT dropped on conveyor.\n")

    # Check for conveyor full
    conveyorFull = plc.Read('I_OP220_N3_CONVEYOR_UNLOAD', datatype=193)
    while conveyorFull.Value == 1:
      file.write(f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}: Conveyor full. Operator unloading DUTs...\n")
      input("Conveyor full, please unload and press Enter to continue...")
      conveyorFull = plc.Read('I_OP220_N3_CONVEYOR_UNLOAD', datatype=193)

    file.write(f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}: Conveyor not full, moving belt to next index...\n")

    # Move conveyor until next cleat position reached
    plc.Write('O_OP220_N5_CONV_FWD', 1, datatype=193)
    sleep(0.5)

    cleatInPosition = plc.Read('I_OP220_N3_CONVEYOR_CLEAT', datatype=193)
    while cleatInPosition.Value != 1:
      sleep(0.1)
      cleatInPosition = plc.Read('I_OP220_N3_CONVEYOR_CLEAT', datatype=193)

    plc.Write('O_OP220_N5_CONV_FWD', 0, datatype=193)

    file.write(f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}: Next belt index reached. Waiting for next DUT...\n")


# Initialization function
def initialize_station():
  print("Initializing...")

  plc.Write('Program:MainProgram.RobotOutputs.ob_Reset', 1, datatype=193)   # Reset flag
  sleep(1.0)
  plc.Write('Program:MainProgram.RobotOutputs.ob_Reset', 0, datatype=193)

  plc.Write('Program:MainProgram.RobotOutputs.ob_Resume', 1, datatype=193)  # Resume flag
  sleep(1.0)
  plc.Write('Program:MainProgram.RobotOutputs.ob_Resume', 0, datatype=193)

  plc.Write(f'Program:MainProgram.Nest1Cylinder.PB', 0, datatype=193)
  plc.Write(f'Program:MainProgram.Nest2Cylinder.PB', 0, datatype=193)
  sleep(1)

  robot_ungrip()
  plc.Write('Program:MainProgram.RobotOutputs.ob_Start', 1, datatype=193)   # Start flag
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