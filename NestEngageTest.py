import Capability

def NestEngagetest(plc):
  print("\nRunning test...") 

  while True:
    Capability.simulate_cts1_test()
    Capability.simulate_cts2_test()
