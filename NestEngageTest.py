import Capability

def NestEngageTest(plc):
  print("\nRunning test...") 

  for i in range(100):
    Capability.simulate_cts_test(1)
    Capability.simulate_cts_test(2)
