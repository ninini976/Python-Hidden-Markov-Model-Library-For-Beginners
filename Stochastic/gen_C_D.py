import hmm

# initialize a hmm model using the parameter we get from EM alg.
hmm = hmm.HMM(2)
hmm.set_obervation(["-","+"])
hmm.set_transition_matrix([[0.9603,0.0397],[0,1]])
hmm.set_observation_matrix([[0.9862,0.0138],[0.3897,0.6103]])
hmm.set_pi([0.8664,0.1336])

for i in range(20):
	tss = hmm.gen_true_state_seq(10)
	print(tss)
	print(hmm.gen_ob_seq(10, true_state_seq = tss))