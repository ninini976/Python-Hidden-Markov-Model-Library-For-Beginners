import hmm
from io import StringIO
import numpy as np

def check_all_neg(array):
	for record in array:
		if record != "-":
			return 0
	return 1


	

hmm1 = hmm.HMM(2)
hmm1.set_obervation(["-","+"])
hmm1.set_transition_matrix([[0.8,0.2],[0,1]])
hmm1.set_observation_matrix([[0.894,0.106],[0.375,0.625]])
hmm1.set_pi([0.7488,0.2512])

ps_array = []
ob = ['-','-']
best_pstable = 0
max = 0
for i in range(0,101):
	pstable = float(i)/100
	hmm1.set_transition_matrix([[pstable,1-pstable],[0,1]])
	p = 0
	for j in range(10-len(ob)+1):
		appendob = []
		for x in range(j):
			appendob.append("-")
		appendob.append("+")
		copy = list(ob)
		for element in appendob:
			copy.append(element)
		print copy
		print hmm1.observation_possibility(copy)
		p = p + hmm1.observation_possibility(copy)
	print p
	if p > max:
		max = p
		best_pstable = pstable
	ps_array.append(best_pstable)
	print best_pstable


txt = np.loadtxt('data')
observations = []
pt_observation = []
for i in range (0,5692):
	if i < 5691 and txt[i+1][0] == 1:
		if txt[i][2] <= 6:
			pt_observation.append("-")
		else:
			pt_observation.append("+")
		observations.append(pt_observation)
		pt_observation = []
	else: 
		if i < 5691 and txt[i+1][0] != 1:
			if txt[i][2] <= 6:
				pt_observation.append("-")
			else:
				pt_observation.append("+")
		else:
			if txt[i][2] <= 6:
				pt_observation.append("-")
			else:
				pt_observation.append("+")
			observations.append(pt_observation)

ps_array = []

print len(observations)

for ob in observations:
	if len(ob) == 1:
		continue
	print ob
	if check_all_neg(ob):
		# print "The pstable that can best fit this observation: 1.0"
		if len(ob) > 9:
			ps_array.append(1)
			print 1.0
		else:
			process_neg(ob)
		continue 
	max = 0
	best_pstable = 0
	for i in range(0,101):
		pstable = float(i)/100
		hmm1.set_transition_matrix([[pstable,1-pstable],[0,1]])
		p = hmm1.observation_possibility(ob)
		if p > max:
			max = p
			best_pstable = pstable
 	ps_array.append(best_pstable)
 	print best_pstable

