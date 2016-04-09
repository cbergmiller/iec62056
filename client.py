import serial


class Client(object):
	"""
	IEC 62056-21 client
	"""
	def __init__(self, port=None):
		self.port = port
		self.ser = None

	def _open(self):
		"""
		Open the connection to the meter.
		"""
		self.ser = serial.Serial(
			self.port,
			baudrate=300,
			bytesize=serial.SEVENBITS,
			stopbits=serial.STOPBITS_ONE,
			parity=serial.PARITY_EVEN,
			timeout=1,
		)

	def _send_sign_on(self, device_name=None):
		if not device_name:
			cmd = b'/?!\r\n'
		else:
			cmd = bytes('/?{}!\r\n'.format(device_name), 'ascii')
		self.ser.write(cmd)

	def _send_ack(self):
		protocol = None
		baudrate = None
		mode = None
		cmd = bytes('\x06{}{}{}\r\n'.format(protocol, baudrate, mode), 'ascii')
		self.ser.write(cmd)
