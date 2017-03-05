import hmm
import numpy as np

# initialize a hmm model using the parameter we get from EM alg.
hmm = hmm.HMM(2)
hmm.set_obervation(["-","+"])
hmm.set_transition_matrix([[0.9603,0.0397],[0,1]])
hmm.set_observation_matrix([[0.9862,0.0138],[0.3897,0.6103]])
hmm.set_pi([0.8664,0.1336])

obs = []
for i in range(1375):
	ob = hmm.gen_ob_seq(13)
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

for ob in simulated_data:
	print(ob)

observations = list(simulated_data)

print("Number of all biopsies taken: %d" % sum([len(ob) for ob in observations]))
print("Number of positive biopsy outcome: %d" % sum([ob.count('+') for ob in observations]))
print("Number of negative biopsy outcome: %d" % sum([ob.count('-') for ob in observations]))
print("Average number of biopsies taken by each patient: %.4f" % (float(sum([len(ob) for ob in observations]))/len(observations)))


num_detect_progression = 0
num_continue_after_progression = 0
total_biopsies_after_progression = 0
print("Patients' seq continue biopsy after grade detection:")
for ob in observations:
	try:
		idx = ob.index("+")
		num_detect_progression += 1
		if len(ob) > idx+1:
			num_continue_after_progression += 1
			total_biopsies_after_progression += len(ob) - idx - 1
			print(ob)
	except:
		continue

print("Number of patients with grade progression: " + str(num_detect_progression))
print("Number of patients continue after a grade progression: " + str(num_continue_after_progression))
print("Ratio of patients continue after a grade progression: %.4f" % (float(num_continue_after_progression)/num_detect_progression))
print("Average number of biopsies taken for patients who continue take biopsy after grade progression: %.4f" % (float(total_biopsies_after_progression)/num_continue_after_progression))
print("Drop out rate for patients who got all negtive result in each stage:")
for i in range(12):
	prefix = ["-" for i in range(i+1)]
	total = 0
	drop = 0
	for ob in observations:
		if len(ob) >= len(prefix):
			if(ob[:i+1] == prefix):
				total += 1
				if (len(ob) == len(prefix)):
					drop += 1
	print("Drop out rate after stage %d : %.4f" % ((i+1), (float(drop)/total if total != 0 else 0)))