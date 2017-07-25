import os
import numpy as np
import foillib as fl
import foilreprod as fr

gen = 0

def getfirst(item):
	return item[0]

def generation_step(parents):
	global gen
	gen = gen + 1
	print("Gen: " + str(gen))
	children = fr.produce_children(parents)
	children = children + parents
	print("Benching " + str(len(children)) + " Foils !")
	new_par, lib = get_parents(children)
	i = 0
	for obj in lib:
		print("Best foil in obj:" + str(i) + " Score: " + str((obj[0])[1]))
		i = i +1
	return new_par



def test():
	foils = naca_parents()
	new = optimize(foils, 15)
	polars = fl.get_polars(new, 1000000)
	score = main_obj(polars)
	score2 = sec_obj(polars)
	index_min = np.argmin(score)
	index_min2 = np.argmin(score2)
	fl.write_foil("outfoil1.dat", new[index_min])
	fl.write_foil("outfoil2.dat", new[index_min2])

def optimize(start, n):
	par = start
	best = []
	for i in range(n):
		par = generation_step(par)
	return par

def naca_parents():
	foils = []
	for i in range(4):
		for k in range(4):
			for j in range(3):
				foils.append(fl.load_naca(str(k*2)+str(i*2)+str(10+j*4)))
	return foils

def main_obj(polars):
	score = []
	for polar in polars:
		if (len(polar)>14):
			sc = 1
			i = 0
			for op in polar[0:14]:
				mult = 1
				if (op[6] < 0.3 or op[5] < 0.3 or op[4]<-0.15):
					mult = 10
				i = i + 1
				sc = sc *op[2]*mult #op[1]/op[2]
			score.append(sc**(1/float(i)))
		else:
			score.append(10)
	return score

def sec_obj(polars, lowtr = 0.3):
	score = []
	for polar in polars:
		if(len(polar)>14):
			min = 0
			for op in polar[0:14]:
				if(check_op(op, lowtr = lowtr)):
					min = 10
				if(op[2] > min):
					min = op[2]
			score.append(min)
		else:
			score.append(10)
	return score

def getsecond(item):
	return item[1]

def check_op(op, lowtr = 0.3):
	if (op[6] < lowtr or op[5] < 0.3 or op[4]<-0.15 or op[2] < 0.0005):
		return 0.0
	else:
		return 1.0


def get_parents(foils):
	polars = fl.get_polars(foils, 1000000)
	libs = []
	for k in range(14):
		lib = []
		for i in range(len(polars)):
			polar = polars[i]
			if (len(polar) > k):
				op = polar[k]
				if check_op(op) == 1:
					lib.append([i, op[2]])
				else:
					lib.append([i, 10])
			else:
				lib.append([i, 10])
		lib.sort(key=getsecond)
		libs.append(lib)
	lib = []
	msc = main_obj(polars)
	i = 0
	for ob in msc:
		lib.append([i, ob])
		i = i + 1
	lib.sort(key=getsecond)
	libs.append(lib)

	lib = []
	ssc = sec_obj(polars)
	i = 0
	for ob in ssc:
		lib.append([i,ob])
		i = i + 1
	lib.sort(key=getsecond)
	libs.append(lib)

	lib = []
	tsc = sec_obj(polars, lowtr = 0.8)
	i = 0
	for ob in tsc:
		lib.append([i, ob])
		i = i + 1
	lib.sort(key=getsecond)
	libs.append(lib)

	parentslist = []
	for lib in libs:
		i = 0
		j = 0
		while(i< 3 and j < len(lib)):
			if ((lib[j])[0] in parentslist):
				j = j + 1
			else:
				parentslist.append((lib[j])[0])
				i = i + 1
				j = j + 1
	parents = []
	for parent in parentslist:
		parents.append(foils[parent])
	return parents, libs


test()
