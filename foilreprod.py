import numpy as np
import foillib as fl
from random import random

def mean_rep(foil1, foil2):
	child = 0.5*(foil1 + foil2)
	return child

def foilconcat(foil1, foil2):
	newfoil = []
	for point in foil1:
		newfoil.append(point)
	for point in foil2:
		newfoil.append(point)
	return np.array(newfoil)

def mix_sides(foil1, foil2):
	upper1, lower1 = fl.get_upper_lower(foil1)
	upper2, lower2 = fl.get_upper_lower(foil2)
	child1 = foilconcat(upper1,lower2)
	child2 = foilconcat(upper2,lower1)
	return child1, child2

def produce_children(foils):
	children = []
	for i in range(len(foils)):
		for foil in foils[i+1:]:
			children.append(mean_rep(foils[i], foil))
			ch1, ch2 = mix_sides(foils[i], foil)
			if len(ch1) == 160:
				children.append(ch1)
			if len(ch2) == 160:
				children.append(ch2)
	mods = []
	for foil in children:
		mods.append(linear_mod(foil))
	children = children + mods
	ret = []
	for foil in children:
		ret.append(check_foil(foil))
	return ret


def linear_mod(foil):
	newfoil = []
	a = random()-0.5
	b = random()-0.5
	a = a*1.0
	b = b*1.0
	b = b + 1
	for point in foil:
		mult = (point[0]-0.5) * a + b
		if (mult < 0.2 or mult > 2):
			print("linearmod error")
		newpoint = [0, 0]
		newpoint[0] = point[0]
		newpoint[1] = point[1]*mult
		newfoil.append(newpoint)
	return np.array(newfoil)

def check_foil(foil):
	sup = 0.00001
	inf = 0.00001
	for point in foil:
		if (sup < point[1]):
			sup = point[1]
		if (inf > point[1]):
			inf = point[1]
	max = abs(sup) + abs (inf)
	if max < 0.13:
		mult = 0.13/max
		for point in foil:
			point[1] = point[1] * mult
	return foil
