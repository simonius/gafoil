import numpy as np
import foillib as fl

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
	return children
