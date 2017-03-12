import hmm
import numpy as np
import random
import math

def reestimate(hmm1, observations):
	# following part is EM algorithm for a00(based on the ob sequences in the list observations)
	# stopping criteria the change in log scaled likelihood is with in 10^(-4)
	error_tolerence = 0.000001
	# set the starting value
	a00 = 0.95
	out_a00 = a00
	hmm1.set_transition_matrix([[a00,1-a00],[0,1]])
	b00 = 0.894
	out_b00 = b00
	b11 = 0.625
	out_b11 = b11
	hmm1.set_observation_matrix([[b00, 1- b00], [1-b11,b11]])
	pi0 = 0.7488
	out_pi = pi0
	hmm1.set_pi([pi0,1-pi0])
	# clear dic after change the model parameter
	hmm1.clear_alpha_dict()
	hmm1.clear_beta_dict()
	# calculate original log probability
	last_log = 0
	for ob in observations:		
		last_log = last_log + math.log(hmm1.observation_probability(ob))
	# print(last_log)
	# print starting point
	# print("Starting point:")
	# hmm1.print_hmm()
	new_log = last_log
	# print("new round")
	# print(last_log)
	# hmm1.print_hmm()
	round_num = 0
	while True: # This is a loop of EM algorithm
		hmm1.clear_alpha_dict()
		hmm1.clear_beta_dict()
		
		round_num = round_num + 1
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
		
		last_log = new_log

		new_log = 0
		for ob in observations:
			new_log = new_log + math.log(hmm1.observation_probability(ob))
		# print(new_log)
		# hmm1.print_hmm()
		if new_log < last_log:
			print ("log probability decreases")
			raise ValueError("log probability decreases")	
		# else:
		# 	print ("log probability increases")

		


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
		# print out_a00
		# print out_b00
		# print out_b11
		# print out_pi
		
		# hmm1.print_hmm()
		

		if (abs(new_log - last_log) < error_tolerence) and round_num > 1:
			break


	# hmm1.print_hmm()

	log = 0
	for ob in observations:
		log = log + math.log(hmm1.observation_probability(ob))
	# print("Total posibility:")
	# print(log)

	print("%d\t %.4f\t %.4f\t %.4f\t %.4f\t %.6f" % (len(observations), hmm1.transition_matrix[0][0], hmm1.observation_matrix[0][0], hmm1.observation_matrix[1][1], hmm1.pi[0], log))

# initialize a hmm model using the parameter we get from EM alg.
def generate_simulation_data():
	hmm1 = hmm.HMM(2)
	hmm1.set_obervation(["-","+"])
	hmm1.set_transition_matrix([[0.9603,0.0397],[0,1]])
	hmm1.set_observation_matrix([[0.9862,0.0138],[0.3897,0.6103]])
	hmm1.set_pi([0.8664,0.1336])

	obs = []
	for i in range(1375):
		ob = hmm1.gen_ob_seq(13)
		obs.append(ob)

	drop = [0.2598,0.2450,0.2732,0.2898,0.3415,0.3068,0.3805,0.2687,0.2609,0.5484,0.7692,0.5000,1]

	simulated_data = []
	new_obs = list(obs)
	# i = 1, ... , 12
	for i in range(13):
		old_obs = list(new_obs)
		new_obs = []
		for ob in old_obs:
			if ob[i] == "+":
				if np.random.uniform() < 0.943:
					simulated_data.append(ob[:i+1])
				elif np.random.uniform() < 0.55:
					simulated_data.append(ob[:i+2])
				else:
					simulated_data.append(ob[:i+3])
			if ob[:i+1] == ['-' for i in range(i+1)]:
				if np.random.uniform() < drop[i]:
					simulated_data.append(['-' for i in range(i+1)])
				else:
					new_obs.append(ob)

	# for ob in simulated_data:
	# 	print(ob)

	observations = list(simulated_data)
	return observations,hmm1
# print("Number of all biopsies taken: %d" % sum([len(ob) for ob in observations]))
# print("Number of positive biopsy outcome: %d" % sum([ob.count('+') for ob in observations]))
# print("Number of negative biopsy outcome: %d" % sum([ob.count('-') for ob in observations]))
# print("Average number of biopsies taken by each patient: %.4f" % (float(sum([len(ob) for ob in observations]))/len(observations)))


# num_detect_progression = 0
# num_continue_after_progression = 0
# total_biopsies_after_progression = 0
# print("Patients' seq continue biopsy after grade detection:")
# for ob in observations:
# 	try:
# 		idx = ob.index("+")
# 		num_detect_progression += 1
# 		if len(ob) > idx+1:
# 			num_continue_after_progression += 1
# 			total_biopsies_after_progression += len(ob) - idx - 1
# 			print(ob)
# 	except:
# 		continue

# print("Number of patients with grade progression: " + str(num_detect_progression))
# print("Number of patients continue after a grade progression: " + str(num_continue_after_progression))
# print("Ratio of patients continue after a grade progression: %.4f" % (float(num_continue_after_progression)/num_detect_progression))
# print("Average number of biopsies taken for patients who continue take biopsy after grade progression: %.4f" % (float(total_biopsies_after_progression)/num_continue_after_progression))
# print("Drop out rate for patients who got all negtive result in each stage:")
# for i in range(12):
# 	prefix = ["-" for i in range(i+1)]
# 	total = 0
# 	drop = 0
# 	for ob in observations:
# 		if len(ob) >= len(prefix):
# 			if(ob[:i+1] == prefix):
# 				total += 1
# 				if (len(ob) == len(prefix)):
# 					drop += 1
# 	print("Drop out rate after stage %d : %.4f" % ((i+1), (float(drop)/total if total != 0 else 0)))

print("size\t a00\t b00\t b11\t pi0\t log_possibility")
# sample_size = [100,200,500,1000]

# for size in sample_size:
# 	for i in range(5):
# 		# randomly sample 100 samples from 1375 sequences
# 		rand_smpl = random.sample(observations,size)
# 		reestimate(hmm, rand_smpl)
for i in range(50):
	observations,model = generate_simulation_data()
	reestimate(model, observations)