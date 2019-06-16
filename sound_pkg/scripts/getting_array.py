import usb.core
import usb.util
import time
import sys
from pocketsphinx import LiveSpeech
import struct

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
text1 = 'start'
speech = LiveSpeech(lm=False, keyphrase='how about you', kws_threshold=1e-40)
PARAMETERS = {
	'DOAANGLE': (21, 0, 'int', 359, 0, 'ro', 'DOA angle. Current value. Orientation depends on build configuration.'),
	'SPEECHDETECTED': (19, 22, 'int', 1, 0, 'ro', 'Speech detection status.', '0 = false (no speech detected)',
					   '1 = true (speech detected)')
}

TIMEOUT = 100000


def get_array():
	if dev:

		while True:
			try:
				if read('SPEECHDETECTED') == 1:
					for kw in speech:
						temp = direction()
						if kw != " ":
							print("get " + str(kw) + " from " + str(temp))
			except KeyboardInterrupt:
				break


def poskesuphi():
	for kw in speech:
		return kw


def read(name):
	try:
		data = PARAMETERS[name]
	except KeyError:
		return

	id = data[0]

	cmd = 0x80 | data[1]
	if data[2] == 'int':
		cmd |= 0x40

	length = 8

	response = dev.ctrl_transfer(
		usb.util.CTRL_IN | usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE,
		0, cmd, id, length, TIMEOUT)

	response = struct.unpack(b'ii', response.tostring())

	if data[2] == 'int':
		result = response[0]
	else:
		result = response[0] * (2. ** response[1])

	return result


def direction():
	return read('DOAANGLE')


if __name__ == "__main__":
	get_array()
