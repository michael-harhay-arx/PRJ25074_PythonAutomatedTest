import Capability
from time import sleep

def do_action(nest):
  # ungrip DUT if at nest
  if (nest == 0 or nest == 2 or nest == 3):
    Capability.robot_ungrip()
    sleep(0.5)
    Capability.robot_grip()
  else:
    sleep(0.5)

def PositionTest(plc):
  print("\nRunning test...") 

  # grab DUT from loading nest
  Capability.robot_move(0)
  Capability.robot_grip()

  for i in range(25):

    # Iterate through all combinations of movements
    for startNest in range(0, 6):
      Capability.robot_move(startNest)
      do_action(startNest)

      for targetNest in range(startNest + 1, 6):
        # go to target nest
        Capability.robot_move(targetNest)
        do_action(targetNest)

        # go back to start nest
        Capability.robot_move(startNest)
        do_action(startNest)

  Capability.robot_move(5)  # FAIL
  Capability.robot_ungrip()





# OLD --------------------------
    # Capability.robot_move(0)  # LOADING
    # Capability.robot_ungrip()
    # sleep(0.5)
    # Capability.robot_grip()

    # Capability.robot_move(2)  # NEST1
    # Capability.robot_ungrip()
    # sleep(0.5)
    # Capability.robot_grip()

    # Capability.robot_move(0)  # LOADING
    # Capability.robot_ungrip()
    # sleep(0.5)
    # Capability.robot_grip()

    # Capability.robot_move(3)  # NEST2
    # Capability.robot_ungrip()
    # sleep(0.5)
    # Capability.robot_grip()




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
        
