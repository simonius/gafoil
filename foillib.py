import os
import numpy as np

def dell(name):
	os.system("rm " + name)

def load_naca(num):
	save_naca(num, "foilbuf")
	naca = read_foil("foilbuf")
	dell("foilbuf")
	return naca

def call_xfoil(comm_str):
	quiet_flag= "" # "plop \n g \n \n"
	comm_str = quiet_flag + comm_str + "\n \n \n \n \n q \n q \nq \n"
	#print(comm_str)
	os.system("echo \" " + comm_str + " \" | xfoil >xfoil.log 2> xfoilerror.log")
	#dell("xfoil_comms")
	#print("xfoil ended")

def call_xfoil_big(comm):
	comm = comm + " \n \n \n q"
	f = open("commsbuff", "w")
	f.write(comm)
	f.close()
	os.system("xfoil < commsbuff > xfoil.log 2> xfoilerror.log")
	os.system("rm commsbuff")

def save_naca(nacanumber, fname):
	com = "naca " + nacanumber + "\n"
	com = com + "save "+ fname +"\n"
	call_xfoil(com)

def write_polars(filenames, polarnames, rey):
	com =""
	for i in range(len(filenames)):
		com = com + "load " + str(filenames[i]) +"\n"
		com = com + "gdes \n cadd \n \n \n \n \n"
		com = com + "panel \n"
		com = com + "oper \n"
		com = com + "VISC " + str(rey) + "\n"
	#	com = com + "init \n"
		com = com + "cli 0.5 \n"
		com = com + "pacc \n" + str(polarnames[i]) + " \n \n"
		com = com + "cseq 0.4 0.8 0.2 \n"
		com = com + "pacc \n visc \n PDEL 1 \n \n \n"
	call_xfoil_big(com)

def read_foil(filename):
	points = []
	file = open(filename, "r")
	lines = list(file)
	for line in lines[1:]:
		splits = str.split(line)
		points.append([float(splits[0]), float(splits[1])])
	return np.array(points)

def write_foil(filename, foil):
	f = open(filename, "w")
	f.write("genetic foil \n")
	for point in foil:
		f.write(str(point[0]) + " " + str(point[1])+"\n")

def get_upper_lower(foil):
	upper = []
	lower = []
	low_side = 0
	lastx = 1.0
	for point in foil:
		if point[1]  < 0:
			low_side=1
		if low_side == 0:
			upper.append(point)
		else:
			lower.append(point)
		lastx = point[0]

	return np.array(upper), np.array(lower)

def read_polar(filename):
	points = []
	f = open(filename, "r")
	lines = list(f)
	for line in lines[12:]:
		splits = str.split(line)
		point= []
		for s in splits:
			point.append(float(s))
		points.append(point)
	return points

def get_polar(foil, rey):
	write_foil("bufffoil", foil)
	write_polar1("bufffoil", "bpolar", rey)
	polar = read_polar("bpolar")
	dell("bufffoil")
	dell("bpolar")
	return polar


def get_polars(foils, rey):
	i = 0
	polars = []
	filenames = []
	polarfilenames = []
	for foil in foils:
		filename = "bf" + str(i)
		polarfilename = "bp"+str(i)
		filenames.append(filename)
		polarfilenames.append(polarfilename)
		write_foil(filename, foil)
		i = i + 1
	subdivsf = []
	subdivsp = []
	parts = len(filenames) / 100
	for i in range(parts):
		subdivsf.append(filenames[100*i: 100*(i+1)])
		subdivsp.append(polarfilenames[100*i: 100*(i+1)])
	for i in range(parts):
		write_polars(subdivsf[i], subdivsp[i], rey)

	for polar in polarfilenames:
		polars.append(read_polar(polar))
	for i in range(len(filenames)):
		dell(filenames[i])
		dell(polarfilenames[i])
	return polars
