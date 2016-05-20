__author__ = 'Sundu'
import itertools


class rule_generation:
	x = []
	y = []
	xy = []
	x_y = []

	x_sup = 0.0
	xy_sup = 0.0
	conf = 0.0


def getAllPermutations(elements):
	if len(elements) <= 1:
		yield elements
	else:
		for permutation in getAllPermutations(elements[1:]):
			for i in range(len(elements)):
				yield permutation[:i] + elements[0:1] + permutation[i:]


#############Start#########################################################

print ("#######################################Implementation of Apriori Algorithm##############################")
print("Select dataset to test on:")
print("1 - Apple Store")
print("2 - Cycle Store")
print("3 - IKEA")
print("4 - Pet Shop")
print("5 - Music Store")

ch = input("Enter your choice(1-5)")

if ch == 1:
	input_file = "apple_store"
else:
	if ch == 2:
		input_file = "cycle_store"
	else:
		if ch == 3:
			input_file = "ikea"
		else:
			if ch == 4:
				input_file = "pet_shop"
			else:
				input_file = "music_store"



################# Reading Data  #####################################################

with open(input_file) as f:
	data = f.read()

dataset = []
dataset1 = []
for line in data.split("\n"):

	if line:

		dataset = []
		a = line.split()
		for i in range(len(a)):
			dataset.append(a[i])

	dataset1.append(dataset)

print ("dataset1 : ", dataset1)
##########User Data##############################################################

min_sup = float(input("Enter Minimum Support :"))
min_conf = float(input("Enter Minimum Confidence"))

###################### Creating a unique list of data items #######################
items = []

for i in range(0, len(dataset1)):
	# print len(dataset1[i])-1
	for j in range(1, len(dataset1[i])):
		if not items:
			items.append(dataset1[i][j])
		if dataset1[i][j] not in items:
			items.append(dataset1[i][j])
items.sort()
print("Unique items in the dataset are :", items)
print (" ")



########################### Support for 1-items , iteration 1#################

support1 = []
length = float(len(dataset1))
C1 = {}
F1 = {}

for k in items:

	count = 0
	for i in range(0, len(dataset1)):
		for j in range(1, len(dataset1[i])):
			if k == dataset1[i][j]:

				count += 1
				if k in C1:
					C1[k] += 1
				else:
					C1[k] = 1
	support1.append(float(count) / float(len(dataset1)) * 100.0)

for key in C1:
	if ((float(C1[key]) / (float)(len(dataset1))) * 100) >= min_sup:
		F1[key] = (float(C1[key]) / (float)(len(dataset1))) * 100
print("Freqent item set of 1-item and its support are:")
print(F1)

###################################iteratition 2###############################################


supp = {}
combs = []
comb2 = []
items2 = []

for i in range(1, len(F1) + 1):
	els = [list(x) for x in itertools.combinations(F1, i)]
	combs.extend(els)

###########finding the frequent set of combination set#############
support2 = []
grp = []

C2 = {}
F2 = {}

count = 0
for i in range(0, len(dataset1)):

	for temp in range(0, len(combs)):

		temp2 = combs[temp]

		if set(combs[temp]).issubset(set(dataset1[i])):
			count += 1

			if temp in C2:
				C2[temp] += 1
			else:
				C2[temp] = 1

grp2 = []

for key in C2:
	if ((float(C2[key]) / (float)(len(dataset1))) * 100) >= min_sup:
		F2[key] = (float(C2[key]) / (float)(len(dataset1))) * 100

permutationsResult = []  ################ Prints all the combinations of items possible ################

for j in F2:
	permutationsResult.append(getAllPermutations(combs[j]))
for permutation in permutationsResult:
	for x in permutation:
		comb2.append(x)

strB = ""
dict = {}
C3 = []
count = 0
for i in range(0, len(dataset1)):
	for temp in range(0, len(comb2)):
		temp2 = comb2[temp]
		if set(comb2[temp]).issubset(set(dataset1[i])):
			count += 1
			if tuple(temp2) in dict:
				dict[tuple(temp2)] += 1
			else:
				dict[tuple(temp2)] = 1

for h in dict:
	dict[h] = (float(dict[h]) / length) * 100

key_dict = []
for k in dict:
	key_dict.append(k)

arules = []
rules = []
for element in comb2:
	if len(element) > 1:
		r = rule_generation()
		left = 1
		while left < len(element):
			# print element,"ELEM"

			r.x = []
			r.xy = []
			for j in range(1, len(element) + 1):

				if j <= left:
					r.x.append(element[j - 1])
					r.xy.append(element[j - 1])
					strB = strB + element[j - 1] + " "
				else:
					if j - 1 == left:
						strB = strB + "---->"
					r.y.append(element[j - 1])
					r.xy.append(element[j - 1])
					strB = strB + element[j - 1] + " "
			for each_list in comb2:
				if set(r.xy).issubset(set(each_list)):
					for x in key_dict:
						if list(x) == r.xy:
							y = x
							break
					for x in key_dict:
						if list(x) == r.x:
							z = x
							break

					if dict[y] >= min_sup:
						xys = dict[y]

					if dict[z] >= min_sup:
						xs = dict[z]
					conf = (xys / xs) * 100.0
					if conf >= min_conf:
						r.x_sup = xs
						r.xy_sup = xys
						arules.append("\t" + strB + "|" + str(r.x_sup) + "|" + str(r.xy_sup) + "|" + str(conf) + "|")

			rule = []
			strB = ""
			left = left + 1

print("\tRULE|SUPPORT(X)|SUPPORT(XY)|CONFIDENCE|")
print(" ")
for e in list(set(arules)):
	print(e)
