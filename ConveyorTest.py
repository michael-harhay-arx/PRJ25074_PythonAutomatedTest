import Capability
from time import sleep
from datetime import datetime

def ConveyorTest(plc):
  print("\nRunning test...") 

  logName = f"ConveyorLog_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

  for i in range(100):
    input("Load DUT, then press Enter to run pass sequence...")
    Capability.robot_move(0)  # LOADING
    Capability.robot_grip()
    Capability.robot_move(4)  # PASS
    Capability.robot_ungrip()

    Capability.conveyor_logic(logName)

    sleep(0.5)