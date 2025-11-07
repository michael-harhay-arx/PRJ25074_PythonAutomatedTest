import Capability

def BarcodeTest(plc):
  print("\nRunning test...") 

  while True:
    Capability.robot_move(0)  # LOADING
    Capability.robot_grip()
    Capability.robot_move(1)  # BARCODE
    Capability.scan_barcode()
    Capability.robot_move(0)  # LOADING
    Capability.robot_ungrip()

    Capability.robot_move(2)  # NEST1
    Capability.robot_grip()
    Capability.robot_move(1)  # BARCODE
    Capability.scan_barcode()
    Capability.robot_move(2)  # NEST1
    Capability.robot_ungrip()

    Capability.robot_move(3)  # NEST2
    Capability.robot_grip()
    Capability.robot_move(1)  # BARCODE
    Capability.scan_barcode()
    Capability.robot_move(3)  # NEST2
    Capability.robot_ungrip()
