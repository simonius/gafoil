import os
import numpy as np
import foillib as fl
import foilreprod as fr

gen = 0

def getfirst(item):
	return item[0]

def generation_step(parents):
	children = fr.produce_children(parents)
	children = children + parents
	score = score_foils(children)
	lib = []
	for i in range(len(score)):
		lib.append([score[i], children[i]])
	lib.sort(key=getfirst)
	score.sort()
	new_parents =[]
	for obj in lib[-30:]:
		new_parents.append(obj[1])
	return new_parents, score[-1]



def test():
	foils = naca_parents()
	new = optimize(foils, 10)

def optimize(start, n):
	par = start
	best = []
	for i in range(n):
		par, sc = generation_step(par)
		print("Best score: " + str(sc))
		best.append(sc)
	print(best)

def naca_parents():
	foils = []
	for i in range(4):
		for k in range(4):
			for j in range(3):
				foils.append(fl.load_naca(str(k*2)+str(i*2)+str(10+j*3)))
	return foils

def score_foils(foils):
	polars = fl.get_polars(foils, 1000000)
	score = []
#	print(polars)
	for polar in polars:
		if (len(polar)>2):
			op = polar[1]
			score.append(op[1]/op[2])
		else:
			score.append(0)
	return score

test()
