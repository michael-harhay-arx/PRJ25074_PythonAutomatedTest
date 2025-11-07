import Capability

def PathTest(plc):
  print("\nRunning test...") 

  # LOADING
  Capability.robot_move(0)  # LOADING
  Capability.robot_move(1)  # BARCODE

  # BARCODE
  Capability.robot_move(1)  # BARCODE
  Capability.robot_move(0)  # LOADING
  
  Capability.robot_move(1)  # BARCODE
  Capability.robot_move(2)  # NEST1

  Capability.robot_move(1)  # BARCODE
  Capability.robot_move(3)  # NEST2

  Capability.robot_move(1)  # BARCODE
  Capability.robot_move(5)  # FAIL

  # NEST 1
  Capability.robot_move(2)  # NEST1
  Capability.robot_move(5)  # FAIL

  Capability.robot_move(2)  # NEST1
  Capability.robot_move(4)  # PASS

  Capability.robot_move(2)  # NEST1
  Capability.robot_move(1)  # BARCODE

  Capability.robot_move(2)  # NEST1
  Capability.robot_move(0)  # LOADING

  Capability.robot_move(2)  # NEST1
  Capability.robot_move(3)  # NEST2

  # NEST 2
  Capability.robot_move(3)  # NEST2
  Capability.robot_move(5)  # FAIL

  Capability.robot_move(3)  # NEST2
  Capability.robot_move(4)  # PASS

  Capability.robot_move(3)  # NEST2
  Capability.robot_move(1)  # BARCODE

  Capability.robot_move(3)  # NEST2
  Capability.robot_move(0)  # LOADING

  Capability.robot_move(3)  # NEST2
  Capability.robot_move(2)  # NEST1

  # FAIL
  Capability.robot_move(5)  # FAIL
  Capability.robot_move(0)  # LOADING

  Capability.robot_move(5)  # FAIL
  Capability.robot_move(1)  # BARCODE

  Capability.robot_move(5)  # FAIL
  Capability.robot_move(2)  # NEST1

  Capability.robot_move(5)  # FAIL
  Capability.robot_move(3)  # NEST2

  # PASS
  Capability.robot_move(4)  # PASS
  Capability.robot_move(0)  # LOADING

  Capability.robot_move(4)  # PASS
  Capability.robot_move(1)  # BARCODE

  Capability.robot_move(4)  # PASS
  Capability.robot_move(2)  # NEST1

  Capability.robot_move(4)  # PASS
  Capability.robot_move(3)  # NEST2
