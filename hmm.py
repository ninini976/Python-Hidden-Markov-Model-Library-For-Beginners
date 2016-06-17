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
		self.ob_map = {}
		self.transition_matrix = []
		self.observation_matrix = []

	def set_obervation(self, ob):
		self.observation = ob
		count = 0
		for ob_type in ob:
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
	def __transform_ob_seq(self, ob):
		return_ob = []
		for ob_type in ob:
			return_ob.append(self.ob_map[ob_type])
		return return_ob

	"""observation sequence without a given inner state"""
	"""P(O|\lambda)"""
	"""argument: 1.a observation sequence vector of arbitrary length"""
	"""return value: possibility (0~1)"""
	def observation_possibility(self, ob):
		result = 0
		state_seq = [0]*len(ob)
		for i in range(0, pow(self.Nostate, len(ob))-1):
			# print state_seq
			# print self.state_seq_possibility(state_seq)
			# print self.ob_seq_possibility(ob, state_seq)
			result = result + self.state_seq_possibility(state_seq)*self.ob_seq_possibility(ob, state_seq)
			increment(state_seq, len(ob)-1, self.Nostate)
		# print state_seq
		# print self.state_seq_possibility(state_seq)
		# print self.ob_seq_possibility(ob, state_seq)
		result = result + self.state_seq_possibility(state_seq)*self.ob_seq_possibility(ob, state_seq)
		return result

	"""possibility of a observation given a deterimined sequence of inner state"""
	"""P(O|Q,\lambda)"""
	"""argument: 1.a observation sequence vector of arbitrary length 2.a inner state sequence vector with the same length as first vector"""	
	"""return value: possibility (0~1)"""
	def ob_seq_possibility(self, ob, seq):
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
	def state_seq_possibility(self, seq):
		result = self.pi[seq[0]]
		for i in range(1,len(seq)):
			result = result*self.transition_matrix[seq[i-1]][seq[i]]
		return result


	"""possibility of the partial observation sequence, O1 O2 .. Ot, and the state Si at time t, given the model \lambda"""
	"""\alpha_t(i)"""
	"""argument: 1. t: the time 2. i: the state at time t 3.seq: a list of sequence"""
	def alpha(self, t, i, seq):
		partial_seq = []
		for i in range(t):
			partial_seq.append(seq[i])
		p = self.observation_possibility(partial_seq)
		print p

