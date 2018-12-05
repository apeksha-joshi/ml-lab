import csv
hypo=['$','$','$','$','$','$']
with open('Training_examples.csv') as csvfile:
	readcsv=csv.reader(csvfile,delimiter=',')
	
	data=[]
	print('\nExamples are: \n')
	for row in readcsv:
		print(row)
		if row[len(row)-1].upper()=='Y':
			data.append(row)
print('\npositive examples\n')
for row in data:
	print(row)
	
tlen=len(data)
d=len(data[0])-1
l=[]
print('\nSteps:\n')
print(hypo)
for i in range(d):
	l.append(data[0][i])
hypo=l
print(hypo)
for i in range(tlen):
	for k in range(d):
		if hypo[k]!=data[i][k]:
			hypo[k]='?'
	print(hypo)

