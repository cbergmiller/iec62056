

MEDIUM = {
	'0': 'abstract',
	'1': 'electricity',
	'4': 'heating costs',
	'5': 'cold',
	'6': 'heat',
	'7': 'gas',
	'8': 'water',
	'9': 'hot water',
}

MEASURE_ELECTRICITY = {
	'0': 'general function',
	'1': 'sum active power +',
	'2': 'sum active power -',
	'3': 'sum reactive power +',
	'4': 'sum reactive power -',
	'5': 'sum reactive power Q I',
	'6': 'sum reactive power Q II',
	'7': 'sum reactive power Q III',
	'8': 'sum reactive power Q IV',
	'9': 'sum apparent power +',
	'10': 'sum apparent power -',
	'13': 'power factor',
	'14': 'frequency',
	'21': 'L1 active power +',
	'22': 'L1 active power -',
	'23': 'L1 reactive power +',
	'24': 'L1 reactive power -',
	'25': 'L1 reactive power Q I',
	'26': 'L1 reactive power Q II',
	'27': 'L1 reactive power Q III',
	'28': 'L1 reactive power Q IV',
	'29': 'L1 apparent power +',
	'30': 'L1 apparent power -',
	'31': 'L1 current',
	'32': 'L1 voltage',
	'33': 'L1 power factor',
	'41': 'L2 active power +',
	'42': 'L2 active power -',
	'43': 'L2 reactive power +',
	'44': 'L2 reactive power -',
	'45': 'L2 reactive power Q I',
	'46': 'L2 reactive power Q II',
	'47': 'L2 reactive power Q III',
	'48': 'L2 reactive power Q IV',
	'49': 'L2 apparent power +',
	'50': 'L2 apparent power -',
	'51': 'L2 current',
	'52': 'L2 voltage',
	'53': 'L2 power factor',
	'61': 'L3 active power +',
	'62': 'L3 active power -',
	'63': 'L3 reactive power +',
	'64': 'L3 reactive power -',
	'65': 'L3 reactive power Q I',
	'66': 'L3 reactive power Q II',
	'67': 'L3 reactive power Q III',
	'68': 'L3 reactive power Q IV',
	'69': 'L3 apparent power +',
	'70': 'L3 apparent power -',
	'71': 'L3 current',
	'72': 'L3 voltage',
	'73': 'L3 power factor',
	'94': 'country code',
	'C': 'service',
	'F': 'error message',
	'L': 'list',
	'P': 'Datenprofile, Lastgang P.01/ P.02, Betriebslogbuch P.98/ P.99',
}

MEASURE_THERMAL = {
	'1': 'power',
	'2': 'energy',
}

MODE_ELECTRICITY = {
	'1': 'cumulative minimum',
	'2': 'cumulative maximum',
	'3': 'minimum 1',
	'4': 'average',
	'5': 'previous average',
	'6': 'maximum 1',
	'7': 'instantaneous value',
	'8': 'meter reading',
	'9': '',
}


class Value(object):
	"""
	Value represents a measured valus.
	Values are identified with the Object Identification System (OBIS).
	"""
	def __init__(self, medium='1', channel='1', measure='0', mode='0', rate='0', previous=None, unit=None, value=None):
		self.medium = medium
		self.channel = channel
		self.measure = measure
		self.mode = mode
		self.rate = rate
		self.previous = previous
		self.unit = unit
		self.value = value

