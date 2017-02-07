import time
s = time.time()

from sense_hat import SenseHat
from datetime import datetime

matrix = [[(0,0,0) for x in xrange(8)] for y in xrange(8)]

def main():
	bench("main")
	sense = SenseHat()
	bench("got sense")
	go = True
	while(go):
		date = datetime.now()
		# bench("got date")
		# print(date)
		set_display(sense, date)
		time.sleep(1)
		# go = False

def bench(msg=""):
	global s
	e = time.time()
	print("%.0f %s" % ((e - s) * 1000, msg))
	s = e

def set_display(sense, date):
	# bench("start display")
	# matrix = [[(0,0,0) for x in xrange(8)] for y in xrange(8)]
	# print(matrix)
	# bench("matrix initialized")
	for y in xrange(8):
		for x in xrange(8):
			if y > 4:
				matrix[y][x] = handle_hour(date, x, y)
			elif x > 5:
				matrix[y][x] = handle_second(date, x, y)
			else:
				matrix[y][x] = handle_minute(date, x, y)
	# bench("matrix ready")
	flattened = [rgb for array in matrix for rgb in array]
	# bench("matrix flattened")
	sense.set_pixels(flattened)
	# bench("pixels set")


def handle_hour(date, x, y):
	rgb = (0,0,0)
	if date.hour > distance_hour(x, y):
		rgb = (0, 255, 0)
	return rgb

def distance_hour(x, y):
	dist_x = x
	dist_y = 7 - y
	dist = dist_y * 8 + dist_x
	# print("x:%s y:%s dx:%s dy:%s d:%s"  % (x, y, dist_x, dist_y, dist))
	return dist

def handle_minute(date, x, y):
	luminosity = lambda delta : min(float(delta) / 2, 1)
	rgb = (0,0,0)
	dist = distance_minute(x, y)
	delta = date.minute - dist
	if delta > 0:
		rgb = (0, 0, int(255 * luminosity(delta)))
	#print("x:%s, y:%s, dist:%s, delta:%s, rgb:%s" % (x, y, dist, delta, rgb))
	#print(luminosity(delta))
	return rgb

def distance_minute(x, y):
	dist_x = x
	dist_y = 4 - y
	dist = dist_x * 2 + dist_y * 12
	# print("x:%s y:%s dx:%s dy:%s d:%s"  % (x, y, dist_x, dist_y, dist))
	return dist

def handle_second(date, x, y):
	luminosity = lambda delta : min(float(delta) / 12, 1) / 1.5 + float(1/3)
	rgb = (0,0,0)
	dist = distance_second(x, y)
	delta = float(date.second * 1000000 + date.microsecond) / 1000000 - dist
	if date.minute % 2 == 0:
		if x < 7 and delta > 0:
			rgb = (int(255 * luminosity(delta)), 0, 0)
	else:
		if x == 6:
			rgb = (255, 0, 0)
		elif delta > 0:
			rgb = (int(255 * luminosity(delta)), 0, 0)
	# print("x:%s, y:%s, dist:%s, delta:%s, rgb:%s" % (x, y, dist, delta, rgb))
	return rgb

def distance_second(x, y):
	dist_y = 4 - y
	return dist_y * 12


if __name__ == '__main__':
	main()
