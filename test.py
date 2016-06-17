import hmm

hmm1 = hmm.HMM(2)
hmm1.set_obervation(["-","+"])
hmm1.set_transition_matrix([[0.8,0.2],[0,1]])
hmm1.set_observation_matrix([[0.894,0.106],[0.375,0.625]])
hmm1.set_pi([0.7488,0.2512])


ob_seq = ['-','-','-','+']
p1 = hmm1.gama(1,0,ob_seq)
p2 = hmm1.xi(1,0,0,ob_seq)
p3 = hmm1.xi(1,0,1,ob_seq)

# following part is em for a00
a00 = 0.6
out = 0
error_tolerence = 0.0001
hmm1.set_transition_matrix([[a00,1-a00],[0,1]])
while True:
	a00 = out
	hmm1.set_transition_matrix([[a00, 1-a00],[0,1]])
	xi_sum = 0
	gama_sum = 0
	for i in range(len(ob_seq)-1):
		xi_sum = xi_sum + hmm1.xi(i,0,0,ob_seq)
		gama_sum = gama_sum + hmm1.gama(i,0,ob_seq)
	out = xi_sum/gama_sum
	if abs(out - a00) < error_tolerence:
		break

print a00
print out