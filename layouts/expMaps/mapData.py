

def getData(mapFile):
	tileNum = 0
	width = 0
	height = 0
	with open(mapFile) as f:
		for line in f:
			if width == 0:
				width = len(line)
			for char in line:
				if char != "%":
					tileNum += 1
			height += 1



	return width, height, tileNum

def main():
	result = []
	for i in range(10):
		mapFile = "mts" + str(i) + ".lay"
		a, b, c = getData(mapFile)
		result.append([mapFile, a, b, c])
	import csv
	with open("sizeData.csv", "a") as csvfile:
		spamwriter = csv.writer(csvfile, lineterminator='\n')
		spamwriter.writerows(result)
main()
