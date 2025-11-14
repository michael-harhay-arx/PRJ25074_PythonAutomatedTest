import Capability
from time import sleep

def PositionTest(plc):
  print("\nRunning test...") 

  # grab DUT from loading nest
  Capability.robot_move(0)
  Capability.robot_grip()

  for i in range(25):

    # Iterate through all combinations of movements
    for startNest in range(0, 5):
      for targetNest in range(0, 5):
          
          if startNest == targetNest:
            continue

          else:
            # go back to start nest
            Capability.robot_move(startNest)

            # ungrip DUT if at nest
            if (startNest == 0 or startNest == 2 or startNest == 3):
              Capability.robot_ungrip()
              sleep(0.5)
              Capability.robot_grip()
            else:
              sleep(0.5)

            # go to target nest
            Capability.robot_move(targetNest)

            # ungrip DUT if at nest
            if (targetNest == 0 or targetNest == 2 or targetNest == 3):
              Capability.robot_ungrip()
              sleep(0.5)
              Capability.robot_grip()
            else:
              sleep(0.5)

            # go back to start nest
            Capability.robot_move(startNest)

  
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
        
