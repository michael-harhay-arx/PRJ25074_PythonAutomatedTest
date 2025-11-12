import Capability
from time import sleep

def PositionTest(plc):
  print("\nRunning test...") 

  for i in range(80):
    Capability.robot_move(0)  # LOADING
    Capability.robot_ungrip()
    sleep(0.5)
    Capability.robot_grip()

    Capability.robot_move(2)  # NEST1
    Capability.robot_ungrip()
    sleep(0.5)
    Capability.robot_grip()

    Capability.robot_move(0)  # LOADING
    Capability.robot_ungrip()
    sleep(0.5)
    Capability.robot_grip()

    Capability.robot_move(3)  # NEST2
    Capability.robot_ungrip()
    sleep(0.5)
    Capability.robot_grip()

  Capability.robot_move(5)  # FAIL
  Capability.robot_ungrip()



  # FULL TEST----------------------------------->
  # input("Press Enter to run position validation (fail chute)...")

  # Capability.robot_move(0)  # LOADING
  # Capability.robot_grip()
  # Capability.robot_move(1)  # BARCODE
  
  # Capability.robot_move(2)  # NEST1
  # Capability.robot_ungrip()
  # sleep(0.5)
  # Capability.robot_grip()
  
  # Capability.robot_move(3)  # NEST2
  # Capability.robot_ungrip()
  # sleep(0.5)
  # Capability.robot_grip()

  # Capability.robot_move(5)  # FAIL
  # Capability.robot_ungrip()


  # input("Press Enter to run position validation (conveyor)...")

  # Capability.robot_move(0)  # LOADING
  # Capability.robot_grip()
  # Capability.robot_move(1)  # BARCODE
  
  # Capability.robot_move(2)  # NEST1
  # Capability.robot_ungrip()
  # sleep(0.5)
  # Capability.robot_grip()
  
  # Capability.robot_move(3)  # NEST2
  # Capability.robot_ungrip()
  # sleep(0.5)
  # Capability.robot_grip()

  # Capability.robot_move(4)  # PASS
  # Capability.robot_ungrip()
        
