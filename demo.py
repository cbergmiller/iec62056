from iec62056.client import Client
from iec62056.value import Value

from iec62056.client2 import DLMS


client = Client(port='com7', target_baudrate=2400)
client.read()

# d = DLMS(None, 'COM7')
# d.alive = True
# d._update_values()
