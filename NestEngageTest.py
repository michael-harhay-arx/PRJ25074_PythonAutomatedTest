import Capability

def NestEngageTest(plc):
  print("\nRunning test...") 

  for i in range(100):
    Capability.simulate_cts1_test()
    Capability.simulate_cts2_test()
