import numbers
import math

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
	"""return value: possibility (0~1)"""
	def observation_possibility(self, ob):
		if len(ob) == 0:
			print "error observation sequence empty"
		result = 0
		state_seq = [0]*len(ob)
		for i in range(0, pow(self.Nostate, len(ob))-1):
			# print state_seq
			# print self.state_seq_possibility(state_seq)
			# print self.ob_under_given_true_state_possibility(ob, state_seq)
			result = result + self.state_seq_possibility(state_seq)*self.ob_under_given_true_state_possibility(ob, state_seq)
			increment(state_seq, len(ob)-1, self.Nostate)
		# print state_seq
		# print self.state_seq_possibility(state_seq)
		# print self.ob_under_given_true_state_possibility(ob, state_seq)
		result = result + self.state_seq_possibility(state_seq)*self.ob_under_given_true_state_possibility(ob, state_seq)
		return result

	"""possibility of a observation given a deterimined sequence of inner state"""
	"""P(O|Q,\lambda)"""
	"""argument: 1.ob: a observation sequence vector of arbitrary length 2.seq: a inner state sequence vector with the same length as first vector"""	
	"""return value: possibility (0~1)"""
	def ob_under_given_true_state_possibility(self, ob, seq):
		if len(ob) != len(seq):
			print "The length of observation sequence not equal to inner state sequence"
		else:
			ob_seq = self.__transform_ob_seq(ob)
			result = 1
			for i in range(0, len(ob_seq)):
				result = result*self.observation_matrix[seq[i]][ob_seq[i]]
		return result

	"""possibility of a TRUE state sequence to happen"""
	"""P(Q|\lambda)"""
	"""argument: 1.a TRUE state sequence vector (state denoted by number)"""
	"""return value: possibility (0~1)"""
	def state_seq_possibility(self, ob):
		result = self.pi[ob[0]]
		for i in range(1,len(ob)):
			result = result*self.transition_matrix[ob[i-1]][ob[i]]
		return result


	"""possibility of the partial observation sequence, O1 O2 .. Ot, and the state Si at time t, given the model \lambda"""
	"""\alpha_t(i) = P(O_1 O_2 ... O_t, q_t = S_i|\lamda)"""
	"""argument: 1. t: the time(This is a 0 BASED INDEX. Time starts from 0) 2. i: the state at time t(should also be 0 BASED INDEX) 3.ob: a list of sequence. The list is a string of notation of observation"""
	"""return value: possibility (0~1)"""
	def alpha(self, t, i, ob):
		if i >= self.Nostate:
			print "i should be in the range from 0 to No_of_state-1. Function failed, return 0"
			return 0
		partial_seq = []
		for x in range(t+1):
			partial_seq.append(ob[x])
		p_1 = self.observation_possibility(partial_seq) # p_1 = P(O_1 O_2 .. O_t|\lamda)
 		total = 0
 		for x in range(self.Nostate):
 			total = total + self.observation_matrix[x][self.ob_map[ob[t]]]
		p_2 = self.observation_matrix[i][self.ob_map[ob[t]]]/total # P(q_t = S_i|O_1 O_2 .. O_t, \lamda)
		result = p_1 * p_2
		return result

	"""possibility of partial observation sequence from t+1 to the end, given the state S_i at time t and the model \lamda"""
	"""\beta_t(i) = P(O_t+1 O_t+2 ... O_T|q_t = S_i, \lamda"""
	"""argument: 1. t: the time(This is a 0 BASED INDEX. Time starts from 0) 2. i: the state at time t(should also be 0 BASED INDEX) 3.ob: a list of sequence. The list is a string of notation of observation"""
	"""return value: possibility (0~1)"""
	def beta(self, t, i, ob):
		if i >= self.Nostate:
			print "i should be in the range from 0 to No_of_state-1. Function failed, return 0"
			return 0
		if t == len(ob) - 1: # This is initialization: \beta_T(i) = 1
			return 1
		result = 0
		for j in range(self.Nostate):
			#following is the induction procedure
			result = result + self.transition_matrix[i][j]*self.observation_matrix[j][self.ob_map[ob[t+1]]]*self.beta(t+1,j,ob)
		return result
	"""possibility of being in state S_i at time t, given the observation sequence O and the model \lemda"""
	"""gama_t(i) = P(q_t = S_i|O,\lamda)"""
	"""argument: 1. t: the time(This is a 0 BASED INDEX. Time starts from 0) 2. i: the state at time t(should also be 0 BASED INDEX) 3.ob: a list of sequence. The list is a string of notation of observation"""
	"""return value: possibility (0~1)"""
	def gama(self, t, i, ob):
		if i >= self.Nostate:
			print "i should be in the range from 0 to No_of_state-1. Function failed, return 0"
			return 0
		alpha = self.alpha(t,i,ob)
		beta = self.beta(t,i,ob)
		p = self.observation_possibility(ob)
		result = alpha*beta/p
		return result
	
	"""possibility of being in state S_i at time t, and state S_j at time t+1, given the model and the observation sequence"""
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
 		p = self.observation_possibility(ob)
 		result = alpha*self.transition_matrix[i][j]*self.observation_matrix[j][self.ob_map[ob[t+1]]]*beta/p
 		return result

	# def EM_for_a(self, i, j, seq, error_tolerence):
	# 	if i >= self.Nostate:
	# 		print "i should be in the range from 0 to No_of_state-1. Function failed, return 0"
	# 		return 0
	# 	if j >= self.Nostate:
	# 		print "j should be in the range from 0 to No_of_state-1. Function failed, return 0"
	# 		return 0



