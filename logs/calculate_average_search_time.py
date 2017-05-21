import csv

def writeLog(title, logs):
    import csv
    with open(title, 'a') as csvfile:
        spamwriter = csv.writer(csvfile, lineterminator='\n')
        spamwriter.writerows(logs)

def readData(title):
	log = 0.0
	with open(title, "rb") as f:
		reader = csv.reader(f)
		data = list(reader)
		log = sum([float(i[0]) for i in data]) / len(data) * 1000
	return log

def do():
	logs = []
	for i in range(10):
		title = "test1_mts" + str(i) + "_speedupcra.csv"
		logs.append([title, readData(title)])
		for lvl in [1,2,3]:
			title = "test1_mts" + str(i) + "_abstraction_level" + str(lvl) + ".csv"
			logs.append([title, readData(title)])
		
	writeLog("test1_result.csv", logs)

def do2():
	logs = [["", "speed-up", "abstraction(1)", "abstraction(2)", "abstraction(3)"]]
	for i in range(10):
		log = ["mts" + str(i)]
		title = "test1_mts" + str(i) + "_speedupcra.csv"
		log.append(readData(title))
		for lvl in [1,2,3]:
			title = "test1_mts" + str(i) + "_abstraction_level" + str(lvl) + ".csv"
			log.append(readData(title))
		logs.append(log)
		
	writeLog("test1_result3.csv", logs)
def test():
	title = "test1_mts0_speedupcra.csv"
	result = 0.0
	with open(title, "rb") as f:
		reader = csv.reader(f)
		data = list(reader)
		# print data[1:4]
		result = sum([float(i[0]) for i in data]) / len(data)
	print result

def readData2(title):
	log = 0.0
	successRate = 0.0
	dataList = []
	with open(title, "rb") as f:		
		reader = csv.reader(f)
		data = list(reader)
		for i in data:
			if i[0] != "NAN":
				dataList.append(float(i[0]))
		#print len(dataList), "/", len(data)
		successRate = float(len(dataList)) / float(len(data))
		print successRate
	return successRate, dataList

def test2():
	"""
	calculate success rate and distribution
	"""
	rates = [["map", "speedpucra", "abstraction(1)", "abstraction(2)", "abstraction(3)"]]
	rate = None
	for i in range(10):
		rate = ["mts" + str(i)]
		datas = []
		title = "test2_mts" + str(i) + "_speedupcra.csv"
		result, data = readData2(title)
		rate.append(result)
		data.insert(0, "speedupcra")
		datas.append(data)

		for lvl in [1, 2, 3]:
			title = "test2_mts" + str(i) + "_abstraction_level" + str(lvl) + ".csv"
			result, data = readData2(title)
			rate.append(result)
			data.insert(0, "abstraction_level" + str(lvl))
			datas.append(data)
		#writeLog("test2_mts" + str(i) + ".csv", datas)
		rates.append(rate)
		print rates
	# writeLog
	writeLog("test2_rate.csv", rates)
#do2()
test2()