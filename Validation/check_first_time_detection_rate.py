import hmm

# initialize a hmm model using the parameter we get from EM alg.
hmm = hmm.HMM(2)
hmm.set_obervation(["-","+"])
hmm.set_transition_matrix([[0.9603,0.0397],[0,1]])
hmm.set_observation_matrix([[0.9862,0.0138],[0.3897,0.6103]])
hmm.set_pi([0.8664,0.1336])

num_progression = 0
num_first_detect = 0

for i in range(1000):
	tss = hmm.gen_true_state_seq(10)
	print(tss)
	try:
		idx = tss.index(1)
	except:
		idx = -1
	obs = hmm.gen_ob_seq(10, true_state_seq = tss)
	print(obs)
	if idx != -1:
		if obs[idx] == '+':
			num_first_detect += 1
			num_progression += 1
		else:
			num_progression += 1

print("Number of patients with progression and detected at the first biopsy taken after progression: " + str(num_first_detect))
print("Number of patients with progression: " + str(num_progression))
print("First time detection rate:" + str(float(num_first_detect)/num_progression))