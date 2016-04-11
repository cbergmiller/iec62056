import re
import serial
import logging
import binascii
from contextlib import contextmanager

from .value import Value

_logger = logging.getLogger('iec62056_client')
_logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
_logger.addHandler(ch)


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
		with self.serial_connection():
			self._send_sign_on()
			# while True:
			# 	l = self.ser.readline()
			# 	print(l.decode('ascii'))
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

	def _send_ack_with_options(self, protocol_control_char='1', mode='2'):
		"""Send the 'acknowlege with options' message."""
		_logger.debug('sending acknowledge with options message (baudrate: {})'.format(self.target_baudrate))
		_baudrate = BAUDRATES.get(self.protocol_mode).get(self.target_baudrate)
		cmd = bytes('\x06{}{}{}\r\n'.format(protocol_control_char, _baudrate, mode), 'ascii')
		_logger.debug('command: {}'.format(binascii.hexlify(cmd)))
		self.ser.write(cmd)

	def _read_identification(self):
		_logger.debug('reading identification')
		line1 = self.ser.readline().decode('ascii')
		line2 = self.ser.readline().decode('ascii')
		_logger.debug(line1)
		_logger.debug(line2)
		id_data = re.match('/(\w{3})(\w)\\\\(\w)?(.+)', line2)
		if not id_data:
			raise IOError
		maker_id = id_data.group(1)
		baudrate_id = id_data.group(2)
		mode_id = id_data.group(3)
		meter_id = id_data.group(4)
		_logger.info('maker: {}, baudrate: {}, mode: {}, meter: {}'.format(maker_id, baudrate_id, mode_id, meter_id))

	def _read_data_msg(self):
		"""Read a data message."""
		self.values.clear()
		data_pattern = re.compile('(\w+)-(\w+):(\w+).(\w+).(\w+)*(\w+)?')
		value_pattern = re.compile('\((.*?)\)')
		end = b'!\r\n\x03'
		while True:
			line = self.ser.readline().decode('ascii')
			_logger.debug(line)
			osis_data = data_pattern.match(line)
			value_data = value_pattern.search(line)
			if not value_data:
				_logger.warning('No value match')
				continue
			value_groups = value_data.groups()
			if not value_groups:
				_logger.warning('No value groups')
				continue
			v = value_groups[0].split('*')
			_value = v[0]
			_unit = v[1] if len(v) == 2 else None

			if not osis_data:
				_logger.warning('No osis data')
				continue
			value = Value(
				medium=osis_data.group(1),
				channel=osis_data.group(2),
				measure=osis_data.group(3),
				mode=osis_data.group(4),
				rate=osis_data.group(5),
				previous=osis_data.group(6),
				value=_value,
				unit=_unit
			)
			print(value)
			self.values.append(value)
			_logger.debug(str(value))
			if end in line:
				break
