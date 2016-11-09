file = open('Time_and_result.txt','r')

txt = []

for line in file: # This for loop splite each line in the data file to 3 numbers and saved in the list "txt"
	txt.append(line.split())

observations = []
time = []
pt_observation = []
pt_time = []


for i in range (0,5691): # 5692 is the total number of records
	if i == 0:
		if float(txt[i][3]) <= 6:
			pt_observation.append("6")
		else:
			if float(txt[i][3]) == 7:
				pt_observation.append("3+4")
			else: 
				if float(txt[i][3]) == 7.5:
					pt_observation.append("4+3")
				else:
					if float(txt[i][3]) > 7.5:
						pt_observation.append("8")
		pt_time.append((txt[i][1],txt[i][2]))
	else: 
		if txt[i][0] == txt[i-1][0]:
			if float(txt[i][3]) <= 6:
				pt_observation.append("6")
			else:
				if float(txt[i][3]) == 7:
					pt_observation.append("3+4")
				else:
					if float(txt[i][3]) == 7.5:
						pt_observation.append("4+3")
					else:
						if float(txt[i][3]) > 7.5:
							pt_observation.append("8")
			pt_time.append((txt[i][1],txt[i][2]))
			if i == 5690:
				observations.append(pt_observation)
				time.append(pt_time)

		else:
			observations.append(pt_observation)
			time.append(pt_time)
			pt_time = []
			pt_observation = []
			if float(txt[i][3]) <= 6:
				pt_observation.append("6")
			else:
				if float(txt[i][3]) == 7:
					pt_observation.append("3+4")
				else:
					if float(txt[i][3]) == 7.5:
						pt_observation.append("4+3")
					else:
						if float(txt[i][3]) > 7.5:
							pt_observation.append("8")
			pt_time.append((txt[i][1],txt[i][2]))
			
			
# print len(observations)
# print len(time)

relative_time = []
for ti in time:
	start = ti[0]
	pt_relative_time = []
	for t in ti:
		pt_relative_time.append((int(t[1])-int(start[1]))*12+(int(t[0])-int(start[0])))
	relative_time.append(pt_relative_time)

# for i in range(len(time)):
# 	print observations[i]
# 	print relative_time[i]

a = []
for ob in observations:
	output = 0
	for ele in ob:
		if ele == '8':
			output = 1
	if output == 1:
		print(ob)
		a.append(ob)
print len(a)

# # This is a filter that only filter out those seqences with only one record
# observations = [elem for elem in observations if len(elem)>1]

# for ob in observations:
# 	ob.remove(ob[0])
# 	print ob

# print len(observations)
