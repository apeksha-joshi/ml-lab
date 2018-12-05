import csv 
import math

def mean(num):
	return sum(num)/float(len(num))
	
def stdev(num):
	avg=mean(num)
	var=sum([pow((x-avg),2) for x in num])/float(len(num)-1)
	return math.sqrt(var)

def summarize(dataset):
	summarise=[(mean(att),stdev(att)) for att in zip(*dataset)]
	del summarise[-1]
	return summarise

def calprob(summary,item):
	prob=1
	for i in range(len(summary)):
		x=item[i]
		mean,stdev=summary[i]
		exp=math.exp(-math.pow((x-mean),2)/(2*math.pow(stdev,2)))
		final=exp/(math.sqrt(2*math.pi))*stdev
		prob*=final
		return prob

with open('ConceptLearning.csv') as csvfile:
	data=[line for line in csv.reader(csvfile)]
	
for i in range(len(data)):
	data[i]=[float(x) for x in data[i]]
	
split=int(0.9*len(data))
test=[]
train=[]
train=data[:split]
test=data[split:]
print('\nTraining data:\n')
for i in range(len(train)):
	print(train[i],'\n')
print('\nTesting data:\n')
for i in range(len(test)):
	print(test[i],'\n')
yes=[]
no=[]
for i in range(len(train)):
	if data[i][-1]==5.0:
		no.append(data[i])
	else:
		yes.append(data[i])
yes=summarize(yes)
no=summarize(no)

prediction=[]
for item in test:
	yesprob=calprob(yes,item)
	noprob=calprob(no,item)
	prediction.append(10.0 if(yesprob>noprob) else 5.0)
	
correct=0
for i in range(len(test)):
	if test[i][-1]==prediction[i]:
		correct+=1

for i in range(len(test)):
	print(test[i][-1])
	
for i in range(len(prediction)):
	print(prediction[i])
	
print('\nAccuracy={0}%'.format(float(correct/len(test)*100)))
