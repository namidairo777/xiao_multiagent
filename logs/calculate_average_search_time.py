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
		print data[1:4]
		result = sum([float(i[0]) for i in data]) / len(data)
	print result

do2()