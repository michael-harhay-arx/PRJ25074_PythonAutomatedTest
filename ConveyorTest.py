import Capability
from time import sleep

def PositionTest(plc):
  print("\nRunning test...") 

  for i in range(100):
    input("Press Enter to run pass sequence...")
    Capability.robot_move(0)  # LOADING
    Capability.robot_grip()
    Capability.robot_move(4)  # PASS
    Capability.robot_ungrip()
    sleep(0.5)