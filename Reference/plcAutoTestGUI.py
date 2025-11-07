from PyQt6 import QtWidgets, uic 
import sys
from pylogix import PLC
from PyQt6.QtWidgets import QApplication
from time import sleep
from PyQt6.QtCore import QTimer, QCoreApplication
import time
import asyncio
from qasync import QEventLoop, asyncSlot

class QMainWindow(QtWidgets.QMainWindow):
  
  def __init__(self):
    
    super(QMainWindow, self).__init__()
    uic.load_ui.loadUi("CTS_Logger_Gui.ui", self)
    
    self.show()
    
    self.assign_objects()
    self.catch_actions()
    self.intialize_stuff()
    
    
  def assign_objects(self):
    ## Group_Boxes
    self.plc_controls_group = self.findChild(QtWidgets.QGroupBox, "PLC_CONTROLS_GROUP")
    self.test_controls_group = self.findChild(QtWidgets.QGroupBox, "TEST_CONTROLS_GROUP")
    self.robot_controls_group = self.findChild(QtWidgets.QGroupBox, "ROBOT_CONTROLS_GROUP")
    self.cts_controls_group = self.findChild(QtWidgets.QGroupBox, "CTS_CONTROLS_GROUP")

    ## Text_Fields
    self.plc_ip_address_edit = self.findChild(QtWidgets.QLineEdit, "PLC_IP_ADDRESS_EDIT")
    
    ## Labels
    self.cts_test_label = self.findChild(QtWidgets.QLabel,"CTS_TEST_LABEL")
    self.status_label = self.findChild(QtWidgets.QLabel,"STATUS_LABEL")
    self.plc_ip_address_label = self.findChild(QtWidgets.QLabel,"PLC_IP_ADDRESS_LABEL")
    self.gripper_label = self.findChild(QtWidgets.QLabel,"GRIPPER_LABEL")
    self.position_label = self.findChild(QtWidgets.QLabel,"POSITION_LABEL")
    self.nest1_label = self.findChild(QtWidgets.QLabel,"NEST1_LABEL")
    self.fixture_engage_label = self.findChild(QtWidgets.QLabel,"FIXTURE_ENGAGE_LABEL")
    self.nest2_label = self.findChild(QtWidgets.QLabel,"NEST2_LABEL")
    
    ## Buttons
    self.start_test_pb = self.findChild(QtWidgets.QPushButton, "START_TEST_PB")
    self.plc_connect_pb = self.findChild(QtWidgets.QPushButton, "PLC_CONNECT_PB")
    self.plc_disconnect_pb = self.findChild(QtWidgets.QPushButton, "PLC_DISCONNECT_PB")
    self.robot_grip_pb = self.findChild(QtWidgets.QPushButton, "GRIPPER_GRIP_PB")
    self.robot_ungrip_pb = self.findChild(QtWidgets.QPushButton, "GRIPPER_UNGRIP_PB")
    self.position_next_pb = self.findChild(QtWidgets.QPushButton, "POSITION_NEXT_PB")
    self.position_prev_pb = self.findChild(QtWidgets.QPushButton, "POSITION_PREV_PB")
    self.nest1_cts_test_bp = self.findChild(QtWidgets.QPushButton, "NEST1_CTS_TEST_PB")
    self.nest1_cylinder_pb = self.findChild(QtWidgets.QPushButton, "NEST1_CYLINDER_PB")
    self.nest2_cts_test_bp = self.findChild(QtWidgets.QPushButton, "NEST2_CTS_TEST_PB")
    self.nest2_cylinder_pb = self.findChild(QtWidgets.QPushButton, "NEST2_CYLINDER_PB")

  
  def catch_actions(self):
    ## Button Clicks actions
    self.nest1_cts_test_bp.clicked.connect(self.clicked)
    self.nest1_cylinder_pb.clicked.connect(self.nest1_cylinder_clicked)
    self.nest2_cts_test_bp.clicked.connect(self.clicked)
    self.nest2_cylinder_pb.clicked.connect(self.nest2_cylinder_clicked)
    self.start_test_pb.clicked.connect(self.start_test_clicked)
    self.plc_connect_pb.clicked.connect(self.plc_connect)
    self.plc_disconnect_pb.clicked.connect(self.intialize_stuff)
    self.robot_grip_pb.clicked.connect(self.robot_grip)
    self.robot_ungrip_pb.clicked.connect(self.robot_ungrip)
    self.position_next_pb.clicked.connect(self.clicked)
    self.position_prev_pb.clicked.connect(self.clicked)
    
    ## Text Changed catchers
    self.plc_ip_address_edit.textChanged.connect(self.clicked)


  def intialize_stuff(self):
    self.plc = PLC()
    self.cts_controls_group.setEnabled(False)
    self.robot_controls_group.setEnabled(False)

  def clicked(self):
    pass

  def nest1_cylinder_clicked(self):
    current = self.plc.Read('Program:MainProgram.Nest1Cylinder.PB')
    self.plc.Write('Program:MainProgram.Nest1Cylinder.PB', not current.Value)
  
  def nest2_cylinder_clicked(self):
    current = self.plc.Read('Program:MainProgram.Nest2Cylinder.PB')
    self.plc.Write('Program:MainProgram.Nest2Cylinder.PB', not current.Value)
    
  def plc_connect(self):
    self.plc.IPAddress = self.plc_ip_address_edit.text()
    self.cts_controls_group.setEnabled(True)
    self.robot_controls_group.setEnabled(True)
    
  async def move_to_position(self, position, timeout=10.0):
    self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', position, datatype=199)
    
    start_time = time.time()
    while time.time() - start_time < timeout:
      inPos = self.plc.Read('Program:MainProgram.RobotOutputs.ob_InPos', datatype=193)
      if inPos.Value == 1:
          return True
      await asyncio.sleep(0.1)  # non-blocking

    return False # returns false if timeout occurs
    
  async def robot_ungrip(self):
    self.plc.Write('Program:MainProgram.RobotGripper.PB', False)
    sleep(0.2)

  async def robot_grip(self):
    self.plc.Write('Program:MainProgram.RobotGripper.PB', True)
    sleep(0.2)

  def robot_move(self, target):
    self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', target, dataype=199)

  def update_status(self, status):
    self.status_label.setText(status)

  def simulate_cts_test(self):
    sleep(1.0)
    self.nest1_cylinder_clicked()
    sleep(3.0)
    self.nest1_cylinder_clicked()
    sleep(1.0)

  @asyncSlot()
  async def start_test_clicked(self):

    # Init
    self.update_status("Status: Initializing")
    self.plc.Write('Program:MainProgram.RobotInputs.ib_Reset', 1, datatype=193)
    await asyncio.sleep(1.0)
    self.plc.Write('Program:MainProgram.RobotInputs.ib_Reset', 0, datatype=193)
    await self.robot_ungrip()
    await self.move_to_position(0)
    
    # Barcode -> fail
    self.update_status("BARCODE -> FAIL") 
    self.plc.Write('Program:MainProgram.RobotInputs.ib_Start', 1, datatype=193)
    await self.robot_grip()
    await self.move_to_position(1)  # BARCODE

    await self.move_to_position(5)  # FAIL
    await self.robot_ungrip()
    await self.move_to_position(0)  # LOADING


    # Nest 1 -> fail
    # self.update_status("NEST1 -> FAIL") 
    # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 0, datatype=199) # LOADING
    # self.plc.Write('Program:MainProgram.RobotInputs.ib_Start', 1, datatype=193)
    # self.robot_grip()
    # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 1, datatype=199) # BARCODE
    # sleep(2.0)

    # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 2, datatype=199) # NEST1
    # self.robot_ungrip()
    # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 1, datatype=199) # BARCODE
    # simulate_cts_test()
    # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 2, datatype=199) # NEST1
    # self.robot_grip()

    # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 5, datatype=199) # FAIL
    # self.robot_ungrip()
    # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 0, datatype=199) # LOADING


    # # Nest 1 -> pass
    # self.update_status("NEST1 -> PASS") 
    # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 0, datatype=199) # LOADING
    # self.plc.Write('Program:MainProgram.RobotInputs.ib_Start', 1, datatype=193)
    # self.robot_grip()
    # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 1, datatype=199) # BARCODE
    # sleep(2.0)

    # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 2, datatype=199) # NEST1
    # self.robot_ungrip()
    # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 1, datatype=199) # BARCODE
    # simulate_cts_test()
    # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 2, datatype=199) # NEST1
    # self.robot_grip()

    # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 4, datatype=199) # PASS
    # self.robot_ungrip()
    # self.plc.Write('Program:MainProgram.RobotInputs.iW_TargetPosition', 0, datatype=199) # LOADING


    # Nest 2 -> fail


    # Nest 2 -> pass

  
      
  
if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)

  loop = QEventLoop(app)
  asyncio.set_event_loop(loop)

  main_window = QMainWindow()
  
  with loop:
    loop.run_forever()
        
