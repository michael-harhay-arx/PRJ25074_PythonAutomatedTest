import Capability
from datetime import datetime

def NestEngageTest(plc):
  print("\nRunning test...") 

  logName = f"CylinderLog_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

  for i in range(200):
    Capability.simulate_cts_test(1, logName)
    Capability.simulate_cts_test(2, logName)