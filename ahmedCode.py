from PyQt6 import QtWidgets, uic, QtCore
import sys
from pylogix import PLC
from serial.tools import list_ports


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
    self.cts_controls_group = self.findChild(QtWidgets.QGroupBox, "CTS_CONTROLS_GROUP")
    self.cts_logger_group = self.findChild(QtWidgets.QGroupBox, "CTS_LOGGER_GROUP")
    self.plc_controls_group = self.findChild(QtWidgets.QGroupBox, "PLC_CONTROLS_GROUP")
    self.robot_controls_group = self.findChild(QtWidgets.QGroupBox, "ROBOT_CONTROLS_GROUP")
    ## Text_Fields
    self.log_name_edit = self.findChild(QtWidgets.QLineEdit, "LOG_NAME_EDIT")
    self.plc_ip_address_edit = self.findChild(QtWidgets.QLineEdit, "PLC_IP_ADDRESS_EDIT")
    ## Labels
    self.cts_test_label = self.findChild(QtWidgets.QLabel,"CTS_TEST_LABEL")
    self.com_port_label = self.findChild(QtWidgets.QLabel,"COM_PORT_LABEL")
    self.log_name_label = self.findChild(QtWidgets.QLabel,"LOG_NAME_LABEL")
    self.plc_ip_address_label = self.findChild(QtWidgets.QLabel,"PLC_IP_ADDRESS_LABEL")
    self.gripper_label = self.findChild(QtWidgets.QLabel,"GRIPPER_LABEL")
    self.position_label = self.findChild(QtWidgets.QLabel,"POSITION_LABEL")
    self.nest1_label = self.findChild(QtWidgets.QLabel,"NEST1_LABEL")
    self.fixture_engage_label = self.findChild(QtWidgets.QLabel,"FIXTURE_ENGAGE_LABEL")
    self.nest2_label = self.findChild(QtWidgets.QLabel,"NEST2_LABEL")
    
    ## Buttons
    self.format_logs_pb = self.findChild(QtWidgets.QPushButton, "FORMAT_LOGS_PB")
    self.start_log_pb = self.findChild(QtWidgets.QPushButton, "STAR_LOG_PB")
    self.plc_connect_pb = self.findChild(QtWidgets.QPushButton, "PLC_CONNECT_PB")
    self.plc_disconnect_pb = self.findChild(QtWidgets.QPushButton, "PLC_DISCONNECT_PB")
    self.robot_grip_pb = self.findChild(QtWidgets.QPushButton, "GRIPPER_GRIP_PB")
    self.robot_ungrip_pb = self.findChild(QtWidgets.QPushButton, "GRIPPER_UNGRIP_PB")
    self.position_next_pb = self.findChild(QtWidgets.QPushButton, "POSITION_NEXT_PB")
    self.position_prev_pb = self.findChild(QtWidgets.QPushButton, "POSITION_PREV_PB")
    self.com_ports_refresh_pb = self.findChild(QtWidgets.QPushButton, "COM_PORTS_REFRESH_PB")
    self.nest1_cts_test_bp = self.findChild(QtWidgets.QPushButton, "NEST1_CTS_TEST_PB")
    self.nest1_cylinder_pb = self.findChild(QtWidgets.QPushButton, "NEST1_CYLINDER_PB")
    self.nest2_cts_test_bp = self.findChild(QtWidgets.QPushButton, "NEST2_CTS_TEST_PB")
    self.nest2_cylinder_pb = self.findChild(QtWidgets.QPushButton, "NEST2_CYLINDER_PB")
    ## Combo_Boxes
    self.com_ports_combo = self.findChild(QtWidgets.QComboBox, "COM_PORTS_COMBO")

  
  def catch_actions(self):
    ## Button Clicks actions
    self.nest1_cts_test_bp.clicked.connect(self.clicked)
    self.nest1_cylinder_pb.clicked.connect(self.nest1_cylinder_clicked)
    self.nest2_cts_test_bp.clicked.connect(self.clicked)
    self.nest2_cylinder_pb.clicked.connect(self.nest2_cylinder_clicked)
    self.format_logs_pb.clicked.connect(self.clicked)
    self.start_log_pb.clicked.connect(self.clicked)
    self.plc_connect_pb.clicked.connect(self.plc_connect)
    self.plc_disconnect_pb.clicked.connect(self.intialize_stuff)
    self.robot_grip_pb.clicked.connect(self.robot_grip)
    self.robot_ungrip_pb.clicked.connect(self.robot_ungrip)
    self.position_next_pb.clicked.connect(self.clicked)
    self.position_prev_pb.clicked.connect(self.clicked)
    self.com_ports_refresh_pb.clicked.connect(self.find_com_ports)
    ## Text Changed catchers
    self.log_name_edit.textChanged.connect(self.clicked)
    self.plc_ip_address_edit.textChanged.connect(self.clicked)

  
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
  
  def robot_grip(self):
    self.plc.Write('Program:MainProgram.RobotGripper.PB', True)
    
  def robot_ungrip(self):
    self.plc.Write('Program:MainProgram.RobotGripper.PB', False)
    
  def intialize_stuff(self):
    self.find_com_ports()
    self.plc = PLC()
    self.cts_controls_group.setEnabled(False)
    self.robot_controls_group.setEnabled(False)
  
  def find_com_ports(self):
    self.com_ports_combo.clear()
    ports = list_ports.comports()
    for port in ports:
      self.com_ports_combo.addItem(port.device)
      
  
if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  main_window = QMainWindow()
  sys.exit(app.exec())