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

# print all observations and number of it 
for ob in observations:
	print ob
print len(observations)

# print the log scaled probability of all seqences' product under correct A,B and pi
log = 0
for ob in observations:		
	log = log + math.log(hmm1.observation_probability(ob))
print log

# following part is EM algorithm for a00(based on the ob sequences in the list observations)
error_tolerence = 0.00001

# set the starting value
a00 = 0.01
out_a00 = a00
hmm1.set_transition_matrix([[a00,1-a00],[0,1]])

b11 = 0.70 # b11 use the correct value and won't change in this file
out_b11 = b11
hmm1.set_observation_matrix([[0.8, 0.2], [1-b11,b11]])

while True: # This is a loop of EM algorithm
	a00 = out_a00
	
	denominator_a00 = 0
	numerator_a00 = 0
	
	
	hmm1.set_transition_matrix([[a00, 1-a00],[0,1]]) # transition matrix is updated each iteration
	# print log scaled porbability for each iteration
	log = 0
	for ob in observations:
		log = log + math.log(hmm1.observation_probability(ob))
	print log


	for ob in observations:
		xi_sum = 0 # element that will sum up to the numerator of a00
		gamma_sum = 0 # element that will sum up to the denominator of a00
		for t in range(len(ob)-1):
			# this is for a00
			xi_sum = xi_sum + hmm1.xi(t,0,0,ob)
			gamma_sum = gamma_sum + hmm1.gamma(t,0,ob)
			
		denominator_a00 = denominator_a00 + gamma_sum
		numerator_a00 = numerator_a00 + xi_sum
		
		
	out_a00 = numerator_a00 / denominator_a00
	print out_a00
	
	# hmm1.print_hmm()
	
	if (abs(out_a00 - a00) < error_tolerence): # and (abs(out_b11 - b11) < error_tolerence):
		break


print "result"
print "a"
print a00
print out_a00
print "b11"
print b11
print out_b11
# print "pi0"
# print pi0
# print out3

log = 0
for ob in observations:
	log = log + math.log(hmm1.observation_probability(ob))
print "Total posibility:"
print log
