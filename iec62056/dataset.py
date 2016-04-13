

MEDIUM = {
	'0': 'Abstract',
	'1': 'Electricity',
	'4': 'Heat cost',
	'5': 'Cooling',
	'6': 'Heat',
	'7': 'Gas',
	'8': 'Cold water',
	'9': 'Hot water',
}

MEASURE_ELECTRICITY = {
	'0': 'General purpose',
	'1': 'Sum active power +',
	'2': 'Sum active power -',
	'3': 'Sum reactive power +',
	'4': 'Sum reactive power -',
	'5': 'Sum reactive power Q I',
	'6': 'Sum reactive power Q II',
	'7': 'Sum reactive power Q III',
	'8': 'Sum reactive power Q IV',
	'9': 'Sum apparent power +',
	'10': 'Sum apparent power -',
	'13': 'Power factor',
	'14': 'Frequency',
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
	'81': 'Angles',
	'82': 'Unitless quantity',
	'91': 'Neutral current',
	'92': 'Neutral voltage',
	'94': 'Country specific identifier',
	'96': 'Service entry',
	'97': 'Error message',
	'98': 'List',
	'C': 'Service',
	'F': 'Error message',
	'L': 'List',
	'P': 'Datenprofile, Lastgang P.01/ P.02, Betriebslogbuch P.98/ P.99',
}

MEASURE_THERMAL = {
	'1': 'power',
	'2': 'energy',
}

MODE_ELECTRICITY = {
	'0': 'Billing period average',
	'1': 'Cumulative minimum 1',
	'2': 'Cumulative maximum 1',
	'3': 'Minimum 1',
	'4': 'Current average 1',
	'5': 'Last average 1',
	'6': 'Maximum 1',
	'7': 'Instantaneous value',
	'8': 'Time integral 1',
	'9': 'Time integral 2',
	'10': 'Time integral 3',
	'11': 'Cumulative minimum 2',
	'12': 'Cumulative maximum 2',
	'13': 'Minimum 2',
	'14': 'Current average 2',
	'15': 'Last average 2',
	'16': 'Maximum 2',

	'21': 'Cumulative minimum 3',
	'22': 'Cumulative maximum 3',
	'23': 'Minimum 3',
	'24': 'Current average 3',
	'25': 'Last average 3',
	'26': 'Maximum 3',

	'27': 'Current average 5',
	'28': 'Current average 6',
	'29': 'Time integral 5',
	'30': 'Time integral 6',

	'31': 'Under limit threshold',
	'32': 'Under limit occurrence counter',
	'33': 'Under limit duration',
	'34': 'Under limit magnitude',
	'35': 'Over limit threshold',
	'36': 'Over limit occurrence counter',
	'37': 'Over limit duration',
	'38': 'Over limit magnitude',
	'39': 'Missing threshold',
	'40': 'Missing occurrence counter',
	'41': 'Missing duration',
	'42': 'Missing magnitude',

	'55': 'Test average',
	'58': 'Time integral 4',
}


class DataSet(object):
	"""
	DataSet represents a DLMS/COSEM Data-Set using
	the Object Identification System (OBIS).
	"""
	def __init__(self, medium='1', channel='1', measure='0', mode='0', rate='0', billing_period=None):
		self.medium = medium
		self.channel = channel
		self.measure = measure
		self.mode = mode
		self.rate = rate
		self.billing_period = billing_period
		self.values = []

	def __str__(self):
		return u'{} - {} - {}{}: {}'.format(
			self.medium_display,
			self.measure_display,
			self.mode_display,
			' - {}'.format(self.billing_period_display) if self.billing_period else '',
			', '.join([str(v) for v in self.values])
		)

	def add_value(self, value, unit):
		self.values.append(Value(value, unit))

	@property
	def medium_display(self):
		return MEDIUM.get(self.medium, 'unknown')

	@property
	def measure_display(self):
		if self.medium == '1':
			measures = MEASURE_ELECTRICITY
		else:
			return 'unknown'
		return measures.get(self.measure, 'unknown')

	@property
	def mode_display(self):
		if self.medium == '1':
			modes = MODE_ELECTRICITY
		else:
			return 'unknown'
		return modes.get(self.mode, 'unknown')

	@property
	def billing_period_display(self):
		return 'period {}'.format(self.billing_period)


class Value(object):
	"""
	Value represents a value for a Data-Set.
	"""
	def __init__(self, value, unit):
		self.value = value
		self.unit = unit

	def __str__(self):
		if self.unit:
			return '{} {}'.format(self.value, self.unit)
		return str(self.value)
