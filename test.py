import hmm
from io import StringIO
import numpy as np
import math
import sys

hmm1 = hmm.HMM(2)
hmm1.set_obervation(["-","+"])
hmm1.set_transition_matrix([[0.8,0.2],[0,1]])
hmm1.set_observation_matrix([[1.00,0.00],[0.375,0.625]])
hmm1.set_pi([0.7488,0.2512])

#........The following part is the code for reading data form file "data"


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
# print observations
observations = [elem for elem in observations if len(elem)>1]
# for ob in observations:
# 	print str(ob)+','

# print len(observations)



# a = 0.85
# while True:
# 	b = 0.9
# 	while True:
# 		pi = 0.65
# 		while True:
# 			sys.stdout.write("Starting: a = " + str(a) + " b = " + str(b) + " pi = " + str(pi) + "\n")
# 			sys.stdout.flush()

# 			pi = pi + 0.05
# 			if pi == 0.85:
# 				break
# 		b = b + 0.05
# 		if b == 1.05:
# 			break
# 	a = a + 0.05
# 	if a == 1.05:
# 		break

# following part is em for a00(based on the ob sequences in the list observations)
# a00 = 0.6
# out = 0.6
# error_tolerence = 0.000001
# hmm1.set_transition_matrix([[a00,1-a00],[0,1]])
# while True:
# 	a00 = out
# 	hmm1.set_transition_matrix([[a00, 1-a00],[0,1]])
# 	divisor = 0
# 	dividend = 0
# 	for ob in observations:
# 		xi_sum = 0
# 		gama_sum = 0
# 		for t in range(len(ob)-1):
# 			xi_sum = xi_sum + hmm1.xi(t,0,0,ob)
# 			gama_sum = gama_sum + hmm1.gama(t,0,ob)
# 		dividend = dividend + xi_sum
# 		divisor = divisor + gama_sum
# 	out = dividend/divisor
# 	print out
# 	if abs(out - a00) < error_tolerence:
# 		break

# print a00
# print out



# This is the grid search on maximizing the product of P for each sequence
# Max_p_log = -1000000000000000000000000000000000000
# Max = 0
# for i in range(1,101):
# 	a = float(i)/100
# 	log = 0
# 	for ob in observations:
# 		hmm1.set_transition_matrix([[a,1-a],[0,1]])
# 		log = log + math.log(hmm1.observation_possibility(ob))
# 	print log	
# 	if log > Max_p_log:
# 		Max = a
# 		Max_p_log = log
# print Max




# following part is em for a00(based on the ob sequences in the list observations)
error_tolerence = 0.001

a00 = 0.9
out = a00
hmm1.set_transition_matrix([[a00,1-a00],[0,1]])

b00 = 0.8
out1 = b00
hmm1.set_observation_matrix([[b00, 1-b00], [0.375,0.625]])

# out2 = b11
# pi0 = 0.7488
# out3 = pi0
# hmm1.set_pi([pi0,1-pi0])


while True:
	a00 = out
	b00 = out1
	# b11 = out2
	# pi0 = out3
	
	divisor_a00 = 0
	divisor_b00 = 0
	divisor_b11 = 0
	dividend_a00 = 0
	dividend_b11 = 0
	dividend_b00 = 0
	# out3 = 0 # out3 is for estimate of pi_0
	hmm1.set_observation_matrix([[b00, 1-b00], [0.375,0.625]])
	hmm1.set_transition_matrix([[a00, 1-a00],[0,1]])
	# hmm1.set_pi([pi0, 1-pi0])
	for ob in observations:
		xi_sum = 0
		gama_sum = 0
		gama_sum1 = 0 # fenmu b00
		gamma_sum_p1 = 0 # fenzi b00
		# gama_sum2 = 0 # fenmu b11
		# gamma_sum_p2 = 0 # fenzi b11
		for t in range(len(ob)-1):
			# this is for a00
			xi_sum = xi_sum + hmm1.xi(t,0,0,ob)
			gama_sum = gama_sum + hmm1.gama(t,0,ob)
			
			# this is for b00
			gama_sum1 = gama_sum1 + hmm1.gama(t,0,ob)
			if ob[t] == "-":
				gamma_sum_p1 = gamma_sum_p1 + hmm1.gama(t,0,ob)

			# #this is for b11
			# gama_sum2 = gama_sum2 + hmm1.gama(t,1,ob)
			# if ob[t] == '+':
			# 	gamma_sum_p2 = gamma_sum_p2 + hmm1.gama(t,1,ob)	

		t = len(ob) - 1
		gama_sum1 = gama_sum1 + hmm1.gama(t,0,ob)
		if ob[t] == "-":
			gamma_sum_p1 = gamma_sum_p1 + hmm1.gama(t,0,ob)



		divisor_a00 = divisor_a00 + gama_sum
		divisor_b00 = divisor_b00 + gama_sum1
		# divisor_b11 = divisor_b11+ gama_sum2
		dividend_a00 = dividend_a00 + xi_sum
		dividend_b00 = dividend_b00 + gamma_sum_p1
		# dividend_b11 = dividend_b11 + gamma_sum_p2
		
		# out3 = out3 + hmm1.gama(0,0,ob)

	out = dividend_a00 / divisor_a00
	out1 = dividend_b00 / divisor_b00
	# out2 = dividend_b11 / divisor_b11
	# out3 = out3/len(observations)
	
	log = 0
	for ob in observations:
		log = log + math.log(hmm1.observation_possibility(ob))
	print log
	# sys.stdout.write('.')
	# sys.stdout.flush()

	if (abs(out - a00) < error_tolerence) and (abs(out1 - b00) < error_tolerence):
		break


# sys.stdout.write('\n')
# sys.stdout.flush()
print "result"
print "a"
print a00
print out
print "b00"
print b00
print out1
# print "pi0"
# print pi0
# print out3

log = 0
for ob in observations:
	log = log + math.log(hmm1.observation_possibility(ob))
print "Total posibility:"
print log
