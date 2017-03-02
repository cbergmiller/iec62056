from iec62056.client import Client

from iec62056.client2 import DLMS

client = Client(port='com7', target_baudrate=300)
client.read()
for d in client.data_sets:
    print(d)


# d = DLMS(None, 'COM7')
# d.alive = True
# d._update_values()
