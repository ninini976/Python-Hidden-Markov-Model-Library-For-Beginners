import hmm
from io import StringIO
import numpy as np
import math
import sys

hmm1 = hmm.HMM(2)
hmm1.set_obervation(["-","+"])
hmm1.set_transition_matrix([[0.9,0.1],[0,1]])
hmm1.set_observation_matrix([[0.8,0.2],[0.3,0.7]])
hmm1.set_pi([0.85,0.15])

#........The following part is the code for reading data form file "data"

txt = []
file = open('data')


for line in file: # This for loop splite each line in the data file to 3 numbers and saved in the list "txt"
	txt.append(line.split())

observations = []
pt_observation = []
for i in range (0,5692): # 5692 is the total number of records
	if i < 5691 and int(txt[i+1][0]) == 1:
		if int(txt[i][2]) <= 6:
			pt_observation.append("-")
		else:
			pt_observation.append("+")
		observations.append(pt_observation)
		pt_observation = []
	else: 
		if i < 5691 and int(txt[i+1][0]) != 1:
			if int(txt[i][2]) <= 6:
				pt_observation.append("-")
			else:
				pt_observation.append("+")
		else:
			if int(txt[i][2]) <= 6:
				pt_observation.append("-")
			else:
				pt_observation.append("+")
			observations.append(pt_observation)


# This is a filter that only filter out those seqences with only one record
observations = [elem for elem in observations if len(elem)>1]

# In each sequence, remove the diagnosis stage data and print
for ob in observations:
	ob.remove(ob[0])
	#print ob

# Print the number of observation seqences in total
#print len(observations)

print("Number of all biopsies taken: %d" % sum([len(ob) for ob in observations]))
print("Average number of biopsies taken by each patient: %.4f" % (float(sum([len(ob) for ob in observations]))/len(observations)))


num_detect_progression = 0
num_continue_after_progression = 0
total_biopsies_after_progression = 0
print("Patients' seq continue biopsy after grade detection:")
for ob in observations:
	try:
		idx = ob.index("+")
		num_detect_progression += 1
		if len(ob) > idx+1:
			num_continue_after_progression += 1
			total_biopsies_after_progression += len(ob) - idx - 1
			print(ob)
	except:
		continue

print("Number of patients with grade progression: " + str(num_detect_progression))
print("Number of patients continue after a grade progression: " + str(num_continue_after_progression))
print("Ratio of patients continue after a grade progression: %.4f" % (float(num_continue_after_progression)/num_detect_progression))
print("Average number of biopsies taken for patients who continue take biopsy after grade progression: %.4f" % (float(total_biopsies_after_progression)/num_continue_after_progression))
print("Drop out rate for patients who got all negtive result in each stage:")
for i in range(12):
	prefix = ["-" for i in range(i+1)]
	total = 0
	drop = 0
	for ob in observations:
		if len(ob) >= len(prefix):
			if(ob[:i+1] == prefix):
				total += 1
				if (len(ob) == len(prefix)):
					drop += 1
	print("Drop out rate after stage %d : %.4f" % ((i+1), (float(drop)/total)))