import hmm
from io import StringIO
import numpy as np

hmm1 = hmm.HMM(2)
hmm1.set_obervation(["-","+"])
hmm1.set_transition_matrix([[0.8,0.2],[0,1]])
hmm1.set_observation_matrix([[0.90,0.10],[0.375,0.625]])
hmm1.set_pi([0.7488,0.2512])

txt = []
file = open('data')
for line in file:
	txt.append(line.split())




observations = []
pt_observation = []
for i in range (0,5692):
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

ps_array = []
print observations
observations = [elem for elem in observations if len(elem)>1]
for ob in observations:
	print str(ob)+','

print len(observations)

observations = [['-', '-', '+'],
['-', '-'],
['-', '-', '-'],
['-', '-'],
['-', '-'],
['-', '-', '-'],
['-', '+'],
['-', '+'],
['-', '-', '-'],
['-', '-', '-', '-'],
['-', '-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-', '-', '-'],
['-', '-'],
['-', '-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '+', '+'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['+', '-'],
['-', '-'],
['-', '-', '-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-', '-'],
['-', '-', '+'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-', '-', '-'],
['-', '-', '-', '-'],
['-', '-'],
['-', '-'],
['-', '+'],
['-', '+'],
['-', '+'],
['-', '+'],
['-', '-'],
['-', '-'],
['-', '+'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-', '-'],
['-', '-', '-'],
['-', '+'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-', '-'],
['-', '-'],
['-', '-'],
['-', '+'],
['-', '+'],
['-', '-', '-'],
['-', '-'],
['-', '-'],
['-', '+'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '+'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '+'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-'],
['-', '-']
]
# following part is em for a00
a00 = 0.6
out = 0.6
error_tolerence = 0.000001
hmm1.set_transition_matrix([[a00,1-a00],[0,1]])
while True:
	a00 = out
	hmm1.set_transition_matrix([[a00, 1-a00],[0,1]])
	divisor = 0
	dividend = 0
	for ob in observations:
		xi_sum = 0
		gama_sum = 0
		for t in range(len(ob)-1):
			xi_sum = xi_sum + hmm1.xi(t,0,0,ob)
			gama_sum = gama_sum + hmm1.gama(t,0,ob)
		dividend = dividend + xi_sum
		divisor = divisor + gama_sum
	out = dividend/divisor
	print out
	if abs(out - a00) < error_tolerence:
		break

print a00
print out