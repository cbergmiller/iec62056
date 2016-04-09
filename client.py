import re
import serial
import logging
from contextlib import contextmanager

from .value import Value

_logger = logging.getLogger('iec62056_client')
_logger.setLevel(logging.DEBUG)

BAUDRATES = {
	'B': {
		600: 'A',
		1200: 'B',
		2400: 'C',
		4800: 'D',
		9600: 'E',
		19200: 'F',
	},
	'C': {
		300: '0',
		600: '1',
		1200: '2',
		2400: '3',
		4800: '4',
		9600: '5',
		19200: '6',
	}
}


class Client(object):
	"""
	IEC 62056-21 client
	"""
	def __init__(self, port=None, target_baudrate=9600, protocol_mode='C'):
		self.port = port
		self.ser = None
		self.protocol_mode = protocol_mode
		self.target_baudrate = target_baudrate
		self.values = []

	def read(self):
		"""
		Read the metering data.
		"""
		with self.serial_connection:
			self._send_sign_on()
			self._read_identification()
			self._send_ack_with_options()
			if self.ser.baudrate != self.target_baudrate:
				self.ser.baudrate = self.target_baudrate
			self._read_data_msg()

	@contextmanager
	def serial_connection(self):
		"""Open the serial connection to the meter."""
		self.ser = serial.Serial(
			self.port,
			baudrate=300,
			bytesize=serial.SEVENBITS,
			stopbits=serial.STOPBITS_ONE,
			parity=serial.PARITY_EVEN,
			timeout=1,
		)
		try:
			yield None
		finally:
			self.ser.close()

	def _send_sign_on(self, device_addr=None):
		"""Send the sign on message."""
		if not device_addr:
			cmd = b'/?!\r\n'
			_logger.debug('sending sign on message')
		else:
			cmd = bytes('/?{}!\r\n'.format(device_addr), 'ascii')
			_logger.debug('sending sign on message for device address {}'.format(device_addr))
		self.ser.write(cmd)

	def _send_ack_with_options(self, protocol_control_char='0', mode='0'):
		"""Send the 'acknowlege with options' message."""
		_logger.debug('sending acknowledge with options message (baudrate: {})'.format(self.target_baudrate))
		_baudrate = BAUDRATES.get(self.protocol_mode).get(self.target_baudrate)
		cmd = bytes('\x06{}{}{}\r\n'.format(protocol_control_char, _baudrate, mode), 'ascii')
		self.ser.write(cmd)

	def _read_identification(self):
		_logger.debug('reading identification')
		line = self.ser.readline()
		id_data = re.match('/(\w{3})(\w)(\\\w)?(\w+)', line)
		if not id_data:
			raise IOError
		maker_id = id_data.group(1)
		baudrate_id = id_data.group(2)
		mode_id = id_data.group(3)
		meter_id = id_data.group(4)

	def _read_data_msg(self):
		"""Read a data message."""
		self.values.clear()
		dataset = re.compile('(\w+)-(\w+):(\w+).(\w+).(\w+)*(\w+)?')
		end = '!\r\n\x03'
		while True:
			line = self.ser.readline()
			osis_data = dataset.match(line)
			if not osis_data:
				continue
			value = Value(
				medium=osis_data.group(1),
				channel=osis_data.group(2),
				measure=osis_data.group(3),
				mode=osis_data.group(4),
				rate=osis_data.group(5),
				previous=osis_data.group(6),
				value=None,
				unit=None
			)
			self.values.append(value)
			if end in line:
				break
