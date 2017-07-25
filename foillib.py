import os
import numpy as np

def dell(name):
	os.system("rm " + name + " \n")

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
	t = 64
	for i in range(len( comm)):
		quiet_flag=   "plop \n g \n \n"
		comm[i] = quiet_flag + comm[i]
		comm[i] = comm[i] + " \n \n \n quit \n"

#	callstring = "ulimit -t 48 \n"

	commbuffname = []
	for i in range(len(comm)):
		commbuffname.append("commsbuff" + str(i))
		f = open(commbuffname[i], "w")
		f.write(comm[i])
		f.close()
#		callstring = callstring + "./xfoil < " + commbuffname[i] + " > /dev/null 2> xfoilerror.log  & \n "

	thread_script= []
	for thread in range(t):
		thread_script.append("ulimit -t 32 \n")

	for i in range(len(commbuffname)):
		thread = i % t
		thread_script[thread] = thread_script[thread] + "./xfoil <" + commbuffname[i] + " > /dev/null 2> xfoilerror.log \n"

	callstring = ""
	i = 0
	threadfiles = []
	for thread in thread_script:
		threadfiles.append("thread" + str(i) + ".sh")
		f = open("thread" + str(i) + ".sh", "w")
		f.write(thread)
		f.close
		callstring = callstring + "bash thread"+str(i)+".sh & \n"
		i = i + 1

	callstring = callstring + " wait \n wait \n wait \n"
	f = open("callscr.sh", "w")
	f.write(callstring)
	f.close()
	os.system("bash callscr.sh")
	#os.system("./xfoil < commsbuff > xfoil.log 2> xfoilerror.log")
	for file in commbuffname:
		dell(file)
	for file in threadfiles:
		dell(file)
	dell("callscr.sh")
	#os.system("rm commsbuff")

def save_naca(nacanumber, fname):
	com = "naca " + nacanumber + "\n"
#	com = com + "ppar \n n 100 \n \n \n"
	com = com + "save "+ fname +"\n"
	call_xfoil(com)

def write_polars(filenames, polarnames, rey):
	coms = []
	for i in range(len(filenames)):
		coms.append("")
		coms[i] = coms[i] + "load " + str(filenames[i]) +"\n"
		coms[i] = coms[i] + "gdes \n cadd \n \n \n \n \n"
		coms[i] = coms[i] + "panel \n"
	#	coms[i] = coms[i] + "ppar \n n 60 \n \n \n"
		coms[i] = coms[i] + "oper \n"
		coms[i] = coms[i] + "vpar \n xtr 1.0 0.8 \n \n"
		coms[i] = coms[i] + "VISC " + str(rey) + "\n"
#		thr_coms[t] = thr_coms[t] + "init \n"
		coms[i] = coms[i] + "iter 30 \n"
		coms[i] = coms[i] + "pacc \n" + str(polarnames[i]) + " \n \n"
		coms[i] = coms[i] + "cseq 0.0 1.6 0.1 \n"
		coms[i] = coms[i] + "pacc \n visc \n PDEL 1 \n \n \n"

	call_xfoil_mt(coms)

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
	i = 0
	for point in foil:
		if i > 79: # point[1]  < 0:
			low_side=1
		if low_side == 0:
			upper.append(point)
		else:
			lower.append(point)
		lastx = point[0]
		i = i + 1

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
	dell("bf*")
	dell("bp*")
	return polars

def norm_foil(foil):
	newfoil = []
	normy = foil[79][1]
	m = -normy/(1-foil[79][0])
	for point in foil:
		x = point[0]
		y = point[1]
		y = y + (1-x) * m
		newfoil.append([x, y])
	return np.array(newfoil)
