import Capability
from datetime import datetime

def BarcodeTest(plc):
  print("\nRunning test...") 

  logName = f"BarcodeLog_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

  for i in range(25):
    Capability.robot_move(0)  # LOADING
    Capability.robot_grip()
    Capability.robot_move(1)  # BARCODE
    Capability.sensor_wait(sensorIndex=0, sensorHigh=0, logName=logName)
    Capability.scan_barcode(logName)
    Capability.robot_move(0)  # LOADING
    Capability.sensor_wait(sensorIndex=0, sensorHigh=1, logName=logName)
    Capability.robot_ungrip()

    Capability.robot_move(2)  # NEST1
    Capability.robot_grip()
    Capability.robot_move(1)  # BARCODE
    Capability.sensor_wait(sensorIndex=1, sensorHigh=0, logName=logName)
    Capability.scan_barcode(logName)
    Capability.robot_move(2)  # NEST1
    Capability.sensor_wait(sensorIndex=1, sensorHigh=1, logName=logName)
    Capability.robot_ungrip()

    Capability.robot_move(3)  # NEST2
    Capability.robot_grip()
    Capability.robot_move(1)  # BARCODE
    Capability.sensor_wait(sensorIndex=2, sensorHigh=0, logName=logName)
    Capability.scan_barcode(logName)
    Capability.robot_move(3)  # NEST2
    Capability.sensor_wait(sensorIndex=2, sensorHigh=1, logName=logName)
    Capability.robot_ungrip()
