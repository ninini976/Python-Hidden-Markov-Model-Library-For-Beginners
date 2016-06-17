import hmm

hmm1 = hmm.HMM(2)
hmm1.set_obervation(["-","+"])
hmm1.set_transition_matrix([[0.8,0.2],[0,1]])
hmm1.set_observation_matrix([[0.894,0.106],[0.375,0.625]])
hmm1.set_pi([0.7488,0.2512])


ob_seq = ['-','-','-','+']
p = hmm1.xi(2,0,1,ob_seq)
print p
