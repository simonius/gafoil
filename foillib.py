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
	quiet_flag=   "plop \n g \n \n"
	comm_str = quiet_flag + comm_str + "\n \n \n \n \n quit \n"
	#print(comm_str)
	os.system("echo \" " + comm_str + " \" | ./xfoil >xfoil.log 2> xfoilerror.log")
	#dell("xfoil_comms")
	#print("xfoil ended")

def call_xfoil_mt(comm):
	for i in range(len( comm)):
		quiet_flag=   "plop \n g \n \n"
		comm[i] = quiet_flag + comm[i]
		comm[i] = comm[i] + " \n \n \n quit \n"
	callstring = " "
	commbuffname = []
	for i in range(len(comm)):
		commbuffname.append("commsbuff" + str(i))
		f = open(commbuffname[i], "w")
		f.write(comm[i])
		f.close()
		callstring = callstring + "./xfoil < " + commbuffname[i] + " > xfoil.log 2> xfoilerror.log  & \n "
	callstring = callstring + " wait \n wait \n wait \n"
	#print(callstring)
	os.system(callstring)
	#os.system("./xfoil < commsbuff > xfoil.log 2> xfoilerror.log")
	for file in commbuffname:
		dell(file)
	#os.system("rm commsbuff")

def save_naca(nacanumber, fname):
	com = "naca " + nacanumber + "\n"
	com = com + "save "+ fname +"\n"
	call_xfoil(com)

def write_polars(filenames, polarnames, rey):
	threads = 16
	thr_coms = []
	for t in range(threads):
		thr_coms.append("")
	for i in range(len(filenames)):
		t = i % threads
		thr_coms[t] = thr_coms[t] + "load " + str(filenames[i]) +"\n"
		thr_coms[t] = thr_coms[t] + "gdes \n cadd \n \n \n \n \n"
		thr_coms[t] = thr_coms[t] + "panel \n"
		thr_coms[t] = thr_coms[t] + "oper \n"
		thr_coms[t] = thr_coms[t] + "VISC " + str(rey) + "\n"
	#	com = com + "init \n"
	#	com = com + "cli 0.5 \n"
		thr_coms[t] = thr_coms[t] + "pacc \n" + str(polarnames[i]) + " \n \n"
		thr_coms[t] = thr_coms[t] + "cseq 0.4 0.8 0.2 \n"
		thr_coms[t] = thr_coms[t] + "pacc \n visc \n PDEL 1 \n \n \n"
	call_xfoil_mt(thr_coms)

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

	write_polars(filenames, polarfilenames, rey)

	for polar in polarfilenames:
		polars.append(read_polar(polar))
	for i in range(len(filenames)):
		dell(filenames[i])
		dell(polarfilenames[i])
	return polars
