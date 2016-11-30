import hmm
from io import StringIO
import numpy as np
import math
import sys

# Initiate an hmm with 3 states
hmm1 = hmm.HMM(3)
hmm1.set_obervation(["6","3+4", "8"])
hmm1.set_transition_matrix([[0.92,0.07,0.01],[0,0.7,0.3],[0,0,1]])
hmm1.set_observation_matrix([[0.9,0.08,0.02],[0.1,0.7,0.2],[0.1,0.3,0.6]])
hmm1.set_pi([0.85,0.1,0.05])


# Read data from file 'Time_and_result.txt'
file = open('Time_and_result.txt','r')

txt = []

for line in file: # This for loop splite each line in the data file to 4 numbers and saved in the list "txt"
	txt.append(line.split())

observations = []
time = []
pt_observation = []
pt_time = []


for i in range (0,5691): # 5692 is the total number of records
	if i == 0:
		if float(txt[i][3]) <= 6:
			pt_observation.append("6")
		else:
			if float(txt[i][3]) == 7:
				pt_observation.append("3+4")
			else: 
				if float(txt[i][3]) == 7.5:
					pt_observation.append("4+3")
				else:
					if float(txt[i][3]) > 7.5:
						pt_observation.append("8")
		pt_time.append((txt[i][1],txt[i][2]))
	else: 
		if txt[i][0] == txt[i-1][0]:
			if float(txt[i][3]) <= 6:
				pt_observation.append("6")
			else:
				if float(txt[i][3]) == 7:
					pt_observation.append("3+4")
				else:
					if float(txt[i][3]) == 7.5:
						pt_observation.append("4+3")
					else:
						if float(txt[i][3]) > 7.5:
							pt_observation.append("8")
			pt_time.append((txt[i][1],txt[i][2]))
			if i == 5690:
				observations.append(pt_observation)
				time.append(pt_time)

		else:
			observations.append(pt_observation)
			time.append(pt_time)
			pt_time = []
			pt_observation = []
			if float(txt[i][3]) <= 6:
				pt_observation.append("6")
			else:
				if float(txt[i][3]) == 7:
					pt_observation.append("3+4")
				else:
					if float(txt[i][3]) == 7.5:
						pt_observation.append("4+3")
					else:
						if float(txt[i][3]) > 7.5:
							pt_observation.append("8")
			pt_time.append((txt[i][1],txt[i][2]))
			

relative_time = []
for ti in time:
	start = ti[0]
	pt_relative_time = []
	for t in ti:
		pt_relative_time.append((int(t[1])-int(start[1]))*12+(int(t[0])-int(start[0])))
	relative_time.append(pt_relative_time)

for ob in observations:
	for i in range(len(ob)):
		if ob[i] == '4+3':
			ob[i] = '8'

# This is a filter that only filter out those seqences with only one record
observations = [elem for elem in observations if len(elem)>1]

# In each sequence, remove the diagnosis stage data and print
for ob in observations:
	ob.remove(ob[0])
	print ob

# Print the number of observation seqences in total
print len(observations)

# print len(observations)
# for ob in observations:
# 	print ob


# stopping criteria the change in log scaled likelihood is with in 10^(-4)
error_tolerence = 0.00001


# set the starting value
a00 = 0.92
a01 = 0.07
a11 = 0.70
out_a00 = a00
out_a01 = a01
out_a11 = a11
hmm1.set_transition_matrix([[a00,a01,1-a00-a01],[0,a11,1-a11],[0,0,1]])


b00 = 0.9
b01 = 0.08
b10 = 0.1
b11 = 0.7
b20 = 0.1
b21 = 0.3
out_b00 = b00
out_b01 = b01
out_b10 = b10
out_b11 = b11
out_b20 = b20
out_b21 = b21
hmm1.set_observation_matrix([[b00, b01, 1-b00-b01], [b10, b11, 1-b10-b11], [b20, b21, 1-b20-b21]])

pi0 = 0.85
pi1 = 0.1
out_pi0 = pi0
out_pi1 = pi1
hmm1.set_pi([pi0,pi1, 1-pi0-pi1])

print "start computing initial guess log probablity:"

last_log = 0
for i in range(len(observations)):
	ob = observations[i]
	print "computing initial guess log probablity " + str(i)		
	last_log = last_log + math.log(hmm1.observation_probability(ob))
print last_log


print "Starting point:"
hmm1.print_hmm()

new_log = last_log

round_num = 0
while True: # This is a loop of EM algorithm
	hmm1.clear_alpha_dict()
	hmm1.clear_beta_dict()
	round_num = round_num + 1
	#update parameters in each iteration
	a00 = out_a00
	a01 = out_a01
	a11 = out_a11
	b00 = out_b00
	b01 = out_b01
	b10 = out_b10
	b11 = out_b11
	b20 = out_b20
	b21 = out_b21
	pi0 = out_pi0
	pi1 = out_pi1

	denominator_a00 = 0
	denominator_a01 = 0
	denominator_a11 = 0
	denominator_b00 = 0
	denominator_b01 = 0
	denominator_b10 = 0
	denominator_b11 = 0
	denominator_b20 = 0
	denominator_b21 = 0
	numerator_a00 = 0
	numerator_a01 = 0
	numerator_a11 = 0
	numerator_b00 = 0
	numerator_b01 = 0
	numerator_b10 = 0
	numerator_b11 = 0
	numerator_b20 = 0
	numerator_b21 = 0
	out_pi0 = 0 
	out_pi1 = 0

	# pi, A, B get updated in each iteration
	hmm1.set_transition_matrix([[a00,a01,1-a00-a01],[0,a11,1-a11],[0,0,1]])
	hmm1.set_observation_matrix([[b00, b01, 1-b00-b01], [b10, b11, 1-b10-b11], [b20, b21, 1-b20-b21]])
	hmm1.set_pi([pi0,pi1, 1-pi0-pi1])

	# we check that the log probability increase in each iteration
	last_log = new_log
	new_log = 0
	for ob in observations:
		new_log = new_log + math.log(hmm1.observation_probability(ob))
	print new_log
	if new_log < last_log:
		print "log probability decreases"
		print "WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
		break
	else:
		print "log probability increases"

	


	for i in range(len(observations)):
		
		ob = observations[i]
		# print "reestimate process " + str(i)
		# element that will sum to denominator or numerator for each observation sequence
		sub_denominator_a00 = 0
		sub_denominator_a01 = 0
		sub_denominator_a11 = 0
		sub_denominator_b00 = 0
		sub_denominator_b01 = 0
		sub_denominator_b10 = 0
		sub_denominator_b11 = 0
		sub_denominator_b20 = 0
		sub_denominator_b21 = 0
		sub_numerator_a00 = 0
		sub_numerator_a01 = 0
		sub_numerator_a11 = 0
		sub_numerator_b00 = 0
		sub_numerator_b01 = 0
		sub_numerator_b10 = 0
		sub_numerator_b11 = 0
		sub_numerator_b20 = 0
		sub_numerator_b21 = 0


		for t in range(len(ob)-1):
			# this is for a00
			sub_numerator_a00 += hmm1.xi(t,0,0,ob)
			sub_denominator_a00 += hmm1.gamma(t,0,ob)

			# this is for a01
			sub_numerator_a01 += hmm1.xi(t,0,1,ob)
			sub_denominator_a01 += hmm1.gamma(t,0,ob)

			# this is for a11
			sub_numerator_a11 += hmm1.xi(t,1,1,ob)
			sub_denominator_a11 += hmm1.gamma(t,1,ob)			

		for t in range(len(ob)):	
			# this is for b00
			sub_denominator_b00 += hmm1.gamma(t,0,ob)
			if ob[t] == "6":
				sub_numerator_b00 += hmm1.gamma(t,0,ob)

			# this is for b01
			sub_denominator_b01 += hmm1.gamma(t,0,ob)
			if ob[t] == "3+4":
				sub_numerator_b01 += hmm1.gamma(t,0,ob)

			# this is for b10
			sub_denominator_b10 += hmm1.gamma(t,1,ob)
			if ob[t] == "6":
				sub_numerator_b10 += hmm1.gamma(t,1,ob)

			# this is for b11
			sub_denominator_b11 += hmm1.gamma(t,1,ob)
			if ob[t] == "3+4":
				sub_numerator_b11 += hmm1.gamma(t,1,ob)

			# this is for b20
			sub_denominator_b20 += hmm1.gamma(t,2,ob)
			if ob[t] == "6":
				sub_numerator_b20 += hmm1.gamma(t,2,ob)
 			
			# this is for b21
			sub_denominator_b21 += hmm1.gamma(t,2,ob)
			if ob[t] == "3+4":
				sub_numerator_b21 += hmm1.gamma(t,2,ob)

		
		denominator_a00 += sub_denominator_a00
		denominator_a01 += sub_denominator_a01
		denominator_a11 += sub_denominator_a11
		denominator_b00 += sub_denominator_b00
		denominator_b01 += sub_denominator_b01
		denominator_b10 += sub_denominator_b10
		denominator_b11 += sub_denominator_b11
		denominator_b20 += sub_denominator_b20
		denominator_b21 += sub_denominator_b21
		numerator_a00 += sub_numerator_a00
		numerator_a01 += sub_numerator_a01
		numerator_a11 += sub_numerator_a11
		numerator_b00 += sub_numerator_b00
		numerator_b01 += sub_numerator_b01
		numerator_b10 += sub_numerator_b10
		numerator_b11 += sub_numerator_b11
		numerator_b20 += sub_numerator_b20
		numerator_b21 += sub_numerator_b21
		
		out_pi0 += hmm1.gamma(0,0,ob)
		out_pi1 += hmm1.gamma(0,1,ob)

	out_a00 = numerator_a00 / denominator_a00
	out_a01 = numerator_a01 / denominator_a01
	out_a11 = numerator_a11 / denominator_a11
	out_b00 = numerator_b00 / denominator_b00
	out_b01 = numerator_b01 / denominator_b01
	out_b10 = numerator_b10 / denominator_b10
	out_b11 = numerator_b11 / denominator_b11
	out_b20 = numerator_b20 / denominator_b20
	out_b21 = numerator_b21 / denominator_b21

	out_pi0 = out_pi0/len(observations)
	out_pi1 = out_pi1/len(observations)
	
	hmm1.print_hmm()
	

	if (abs(new_log - last_log) < error_tolerence) and round_num > 1:
		break


print "result:"

hmm1.print_hmm()

# print "a"
# print a00
# print out_a00
# print "b_00"
# print b00
# print out_b00
# print "b11"
# print b11
# print out_b11
# print "pi0"
# print pi0
# print out_pi0

# log = 0
# for ob in observations:
# 	log = log + math.log(hmm1.observation_probability(ob))
# print "Total posibility:"
# print log
