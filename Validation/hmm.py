import numbers
import math
import numpy as np

def increment(array, dig_pos, max):
	if array[dig_pos] < (max -1):
		array[dig_pos] = array[dig_pos] + 1
	else:
		array[dig_pos] = 0
		increment(array, dig_pos-1, max)
	

class HMM(object):
	"""docstring for HMM"""
	"""initialization of a HMM object, give argument of No. state"""

	def __init__(self, Nostate):
		if Nostate > 0 and isinstance (Nostate,(int,long)):
			self.Nostate = Nostate
		else:
			print "Should give a integer larger than 0"
		self.pi = []
		self.observation = []
		self.ob_map = {} # ob_map is a map from the string notation of observation to the No. of observation, For example if we got 2 types of observation ["-","+"], ob_map["-"] = 0, ob_map["+"] = 1
		self.transition_matrix = []
		self.observation_matrix = []
		self.alpha_dict = {}
		self.beta_dict = {}

	def set_obervation(self, obs):
		self.observation = obs
		count = 0
		for ob_type in obs:
			self.ob_map[ob_type] = count
			count = count + 1

	def set_transition_matrix(self,tm):
		self.transition_matrix = tm

	def set_observation_matrix(self,om):
		self.observation_matrix = om

	def set_pi(self, pi):
		self.pi = pi

	def clear_alpha_dict(self):
		self.alpha_dict = {}

	def clear_beta_dict(self):
		self.beta_dict = {}

	def print_hmm(self):
		print "Number of state:"
		print self.Nostate
		print "Type of observations:"
		print self.observation
		print "Transitionmatrix:"
		for line in self.transition_matrix:
			print line
		print "Observation matrix:"
		for line in self.observation_matrix:
			print line
		print "Initial state:"
		print self.pi


	def give_state(self, year):
		current_state = self.pi
		for i in range(0,year):
			next_state = []
			for j in range(0, self.Nostate):
				count = 0
				for k in range (0, self.Nostate):
					count = count + current_state[k]*self.transition_matrix[k][j]  
				next_state.append(round(count,4))
			current_state = next_state
		return next_state

	"""accept a real observation sequence and return a number based observation seq"""
	"""private_method"""
	def __transform_ob_seq(self, ob):
		return_seq = []
		for ob_type in ob:
			return_seq.append(self.ob_map[ob_type])
		return return_seq

	"""observation sequence without a given inner state"""
	"""P(O|\lambda)"""
	"""argument: 1.a observation sequence vector of arbitrary length"""
	"""return value: probability (0~1)"""
	def observation_probability(self, ob):
		# old brute force method

		# if len(ob) == 0:
		# 	print "error observation sequence empty"
		# result = 0
		# state_seq = [0]*len(ob)
		# for i in range(0, pow(self.Nostate, len(ob))-1):
		# 	# print state_seq
		# 	# print self.state_seq_probability(state_seq)
		# 	# print self.ob_under_given_true_state_probability(ob, state_seq)
		# 	result = result + self.state_seq_probability(state_seq)*self.ob_under_given_true_state_probability(ob, state_seq)
		# 	increment(state_seq, len(ob)-1, self.Nostate)
		# # print state_seq
		# # print self.state_seq_probability(state_seq)
		# # print self.ob_under_given_true_state_probability(ob, state_seq)
		# result = result + self.state_seq_probability(state_seq)*self.ob_under_given_true_state_probability(ob, state_seq)
		# return result


		# new alpha pass method
		result = 0
		for i in range(self.Nostate):
			result += self.alpha(len(ob)-1,i,ob)
		return result

	"""probability of a observation given a deterimined sequence of inner state"""
	"""P(O|Q,\lambda)"""
	"""argument: 1.ob: a observation sequence vector of arbitrary length 2.seq: a inner state sequence vector with the same length as first vector"""	
	"""return value: probability (0~1)"""
	def ob_under_given_true_state_probability(self, ob, seq):
		if len(ob) != len(seq):
			print "The length of observation sequence not equal to inner state sequence"
		else:
			ob_seq = self.__transform_ob_seq(ob)
			result = 1
			for i in range(0, len(ob_seq)):
				result = result*self.observation_matrix[seq[i]][ob_seq[i]]
		return result

	"""probability of a TRUE state sequence to happen"""
	"""P(Q|\lambda)"""
	"""argument: 1.a TRUE state sequence vector (state denoted by number)"""
	"""return value: probability (0~1)"""
	def state_seq_probability(self, true_state_seq):
		result = self.pi[true_state_seq[0]]
		for i in range(1,len(true_state_seq)):
			result = result*self.transition_matrix[true_state_seq[i-1]][true_state_seq[i]]
		return result


	"""probability of the partial observation sequence, O1 O2 .. Ot, and the state Si at time t, given the model \lambda"""
	"""\alpha_t(i) = P(O_1 O_2 ... O_t, q_t = S_i|\lamda)"""
	"""argument: 1. t: the time(This is a 0 BASED INDEX. Time starts from 0) 2. i: the state at time t(should also be 0 BASED INDEX) 3.ob: a list of sequence. The list is a string of notation of observation"""
	"""return value: probability (0~1)"""
	def alpha(self, t, i, ob):
		if i >= self.Nostate:
			print "i should be in the range from 0 to No_of_state-1. Function failed, return 0"
			return 0
		# partial_seq = []
		# for x in range(t+1):
		# 	partial_seq.append(ob[x])
		# p_1 = self.observation_probability(partial_seq) # p_1 = P(O_1 O_2 .. O_t|\lamda)
 	# 	total = 0
 	# 	for x in range(self.Nostate):
 	# 		total = total + self.observation_matrix[x][self.ob_map[ob[t]]]
		# p_2 = self.observation_matrix[i][self.ob_map[ob[t]]]/total # p_2 = P(q_t = S_i|O_1 O_2 .. O_t, \lamda)
		# result = p_1 * p_2 # P(O_1 O_2 ... O_t, q_t = S_i|\lamda) = P(O_1 O_2 .. O_t|\lamda) * P(q_t = S_i|O_1 O_2 .. O_t, \lamda)
		if (str(ob[:t+1]),i) in self.alpha_dict:
			return self.alpha_dict[(str(ob[:t+1]),i)]
		result = 0
		if t == 0:
			self.alpha_dict[((str(ob[:t+1]),i))] = self.pi[i]*self.observation_matrix[i][self.ob_map[ob[0]]]
			return self.alpha_dict[((str(ob[:t+1]),i))]
		else:
			Sum = 0
			for j in range(self.Nostate):
				Sum = Sum + self.alpha(t-1,j,ob)*self.transition_matrix[j][i]
			result = Sum*self.observation_matrix[i][self.ob_map[ob[t]]]
			self.alpha_dict[((str(ob[:t+1]),i))] = result
		return result

	"""probability of partial observation sequence from t+1 to the end, given the state S_i at time t and the model \lamda"""
	"""\beta_t(i) = P(O_t+1 O_t+2 ... O_T|q_t = S_i, \lamda"""
	"""argument: 1. t: the time(This is a 0 BASED INDEX. Time starts from 0) 2. i: the state at time t(should also be 0 BASED INDEX) 3.ob: a list of sequence. The list is a string of notation of observation"""
	"""return value: probability (0~1)"""
	def beta(self, t, i, ob):
		if i >= self.Nostate:
			print "i should be in the range from 0 to No_of_state-1. Function failed, return 0"
			return 0
		if (str(ob[t+1:]),i) in self.beta_dict:
			return self.beta_dict[(str(ob[t+1:]),i)]

		if t == len(ob) - 1: # This is initialization: \beta_T(i) = 1
			self.beta_dict[(str(ob[t+1:]),i)] = 1
			return 1
		result = 0
		for j in range(self.Nostate):
			#following is the induction procedure
			# if t == len(ob) - 1:
			# 	result = result + self.transition_matrix[i][j]*1*self.beta(t+1,j,ob) # b_j(O_{T+1}) = 1
			# else:
			result = result + self.transition_matrix[i][j]*self.observation_matrix[j][self.ob_map[ob[t+1]]]*self.beta(t+1,j,ob)
			self.beta_dict[(str(ob[t+1:]),i)] = result
		return result
	"""probability of being in state S_i at time t, given the observation sequence O and the model \lemda"""
	"""gamma_t(i) = P(q_t = S_i|O,\lamda)"""
	"""argument: 1. t: the time(This is a 0 BASED INDEX. Time starts from 0) 2. i: the state at time t(should also be 0 BASED INDEX) 3.ob: a list of sequence. The list is a string of notation of observation"""
	"""return value: probability (0~1)"""
	def gamma(self, t, i, ob):
		if i >= self.Nostate:
			print "i should be in the range from 0 to No_of_state-1. Function failed, return 0"
			return 0
		alpha = self.alpha(t,i,ob)
		beta = self.beta(t,i,ob)
		p = self.observation_probability(ob)
		result = alpha*beta/p
		return result
	
	"""probability of being in state S_i at time t, and state S_j at time t+1, given the model and the observation sequence"""
	"""xi_t(i,j) = P(q_t = S_i, q_t+1 = S_j|O,\lamda)"""
	"""argument: 1. t: the time(This is a 0 BASED INDEX. Time starts from 0) 2,3. i,j: the state at time t and t+1(should also be 0 BASED INDEX) 4.ob: a list of sequence. The list is a string of notation of observation"""
	def xi(self, t, i, j, ob):
		if i >= self.Nostate:
			print "i should be in the range from 0 to No_of_state-1. Function failed, return 0"
			return 0
		if j >= self.Nostate:
			print "j should be in the range from 0 to No_of_state-1. Function failed, return 0"
			return 0
 		alpha = self.alpha(t,i,ob)
 		beta = self.beta(t+1,j,ob)
 		p = self.observation_probability(ob)
 		result = alpha*self.transition_matrix[i][j]*self.observation_matrix[j][self.ob_map[ob[t+1]]]*beta/p
 		return result

	# def EM_for_a(self, i, j, seq, error_tolerence):
	# 	if i >= self.Nostate:
	# 		print "i should be in the range from 0 to No_of_state-1. Function failed, return 0"
	# 		return 0
	# 	if j >= self.Nostate:
	# 		print "j should be in the range from 0 to No_of_state-1. Function failed, return 0"
	# 		return 0

	"""Generate the distribution of true state after time t.(t = 0 will return \pi)"""
	"""argument: 1. t: time (integer greater than or equal to zero)"""
	def gen_true_state_prob_vector(self, t):
		start_vector = np.matrix(self.pi)
		transition_matrix = np.matrix(self.transition_matrix)
		result = start_vector
		for i in range(t):
			result *= transition_matrix
		return result.tolist()[0]

	"""Generate the distribution of observation after time t.(t = 0 will return \pi*observation_matrix)"""
	"""argument: 1. t: time (integer greater than or equal to zero)"""
	def gen_ob_prob_vector(self, t):
		start_vector = np.matrix(self.pi)
		transition_matrix = np.matrix(self.transition_matrix)
		observation_matrix = np.matrix(self.observation_matrix)
		result = start_vector
		for i in range(t):
			result *= transition_matrix
		result *= observation_matrix
		return result.tolist()[0]

	"""Generate a sequence of true state with lenth t"""
	"""argument: 1. t: length of the sequence(t greater than or equal to 0)"""
	def gen_true_state_seq(self,t):
		if t == 0:
			return []
		result = []
		start = np.random.choice(self.Nostate, p = self.pi)
		result.append(start)
		current = start
		for i in range(t-1):
			current = np.random.choice(self.Nostate, p = self.transition_matrix[current])
			result.append(current)
		return result

	"""Generate a sequence of observations with length t"""
	"""argument: 
	1. t: length of the sequence(t greater than or equal to 0) 
	2.(optional) true_state_seq: a seqence of true state sequence, if given, the length of this sequence should be same as t, the function would generate an observation sequence with provided hidden state sequence. If not given, the function would return a random observations sequence based on the probability distribution"""
	def gen_ob_seq(self, t, true_state_seq = None):
		if t == 0:
			return []
		if true_state_seq == None:
			true_state_seq = self.gen_true_state_seq(t)
		else:
			if self.state_seq_probability(true_state_seq) == 0:
				raise Exception("Given true state seq in gen_ob_seq is not possible to happen under given model parameters.")
			elif len(true_state_seq) != t:
				raise Exception("The length of given true_state_seq doesn't match t.")
		result = []
		for i in range(t):
			current = true_state_seq[i]
			result.append(self.observation[np.random.choice(len(self.observation), p = self.observation_matrix[current])])
		return result