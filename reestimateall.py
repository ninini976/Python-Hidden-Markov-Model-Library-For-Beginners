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

# The following part read simulated data from a file "obs1"
file = open("obs1")

observations = []

for line in file:
	observations.append(line.split())
for ob in observations:
	print ob
print len(observations)


log = 0
for ob in observations:		
	log = log + math.log(hmm1.observation_probability(ob))
print log

# following part is EM algorithm for a00(based on the ob sequences in the list observations)
error_tolerence = 0.000001

# set the starting value
a00 = 0.99
out_a00 = a00
hmm1.set_transition_matrix([[a00,1-a00],[0,1]])


b00 = 0.70
out_b00 = b00

b11 = 0.99
out_b11 = b11

hmm1.set_observation_matrix([[b00, 1- b00], [1-b11,b11]])

pi0 = 0.99
out_pi = pi0
hmm1.set_pi([pi0,1-pi0])

print "Starting point:"
hmm1.print_hmm()

while True: # This is a loop of EM algorithm
	a00 = out_a00
	b00 = out_b00
	b11 = out_b11
	pi0 = out_pi
	
	denominator_a00 = 0
	denominator_b00 = 0
	denominator_b11 = 0
	numerator_a00 = 0
	numerator_b00 = 0
	numerator_b11 = 0
	out_pi = 0 # out3 is for estimate of pi_0
	
	hmm1.set_observation_matrix([[b00, 1-b00], [1-b11,b11]]) # observation matrix is updated each iteration
	hmm1.set_transition_matrix([[a00, 1-a00],[0,1]]) # transition matrix is updated each iteration
	hmm1.set_pi([pi0, 1-pi0]) # pi is updated each iteration
	log = 0
	for ob in observations:
		log = log + math.log(hmm1.observation_probability(ob))
	print log
	

	for ob in observations:
		xi_sum = 0 # element that will sum up to the numerator of a00
		gamma_sum = 0 # element that will sum up to the denominator of a00
		gamma_sum1 = 0 # element that will sum up to the numerator of b00
		gamma_sum_p1 = 0 # element that will sum up to the denominator ot b00
		gamma_sum2 = 0 # element that will sum up to the numerator of b11
		gamma_sum_p2 = 0 # element that will sum up to the denominator ot b11
		for t in range(len(ob)-1):
			# this is for a00
			xi_sum = xi_sum + hmm1.xi(t,0,0,ob)
			gamma_sum = gamma_sum + hmm1.gamma(t,0,ob)
		for t in range(len(ob)):	
			# this is for b00
			gamma_sum1 = gamma_sum1 + hmm1.gamma(t,0,ob)
			if ob[t] == "-":
				gamma_sum_p1 = gamma_sum_p1 + hmm1.gamma(t,0,ob)

			# this is for b11
			gamma_sum2 = gamma_sum2 + hmm1.gamma(t,1,ob)
			if ob[t] == '+':
				gamma_sum_p2 = gamma_sum_p2 + hmm1.gamma(t,1,ob)	

		

		denominator_a00 = denominator_a00 + gamma_sum
		denominator_b00 = denominator_b00 + gamma_sum1
		denominator_b11 = denominator_b11+ gamma_sum2
		numerator_a00 = numerator_a00 + xi_sum
		numerator_b00 = numerator_b00 + gamma_sum_p1
		numerator_b11 = numerator_b11 + gamma_sum_p2
		
		out_pi = out_pi + hmm1.gamma(0,0,ob)

	out_a00 = numerator_a00 / denominator_a00
	out_b00 = numerator_b00 / denominator_b00
	out_b11 = numerator_b11 / denominator_b11
	out_pi = out_pi/len(observations)
	print out_a00
	print out_b00
	print out_b11
	print out_pi
	
	# hmm1.print_hmm()
	

	if (abs(out_b11 - b11) < error_tolerence) and (abs(out_b11 - b11) < error_tolerence) and (abs(out_pi - pi0) < error_tolerence) and (abs(out_b00 - b00) < error_tolerence):
		break


print "result"
print "a"
print a00
print out_a00
print "b_00"
print b00
print out_b00
print "b11"
print b11
print out_b11
print "pi0"
print pi0
print out_pi

log = 0
for ob in observations:
	log = log + math.log(hmm1.observation_probability(ob))
print "Total posibility:"
print log
