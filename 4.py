import random
from math import exp
from random import seed

def init_net(n_inputs,n_hidden,n_outputs):
	network=list()
	hidden_layer=[{'weight':[random.uniform(-0.5,0.5) for i in range(n_inputs+1)]} for i in range(n_hidden)]
	network.append(hidden_layer)
	output_layer=[{'weight':[random.uniform(-0.5,0.5) for i in range(n_hidden+1)]} for i in range(n_outputs)]
	network.append(output_layer)
	print(network)
	print('\nInitialised network\n')
	i=1
	for layer in network:
		j=1
		for sub in layer:
			print('\nLayer[{0}] Node[{1}]: '.format(i,j),sub)
			j=j+1
		i=i+1
	return network

def activate(weights,inputs):
	activation=weights[-1]
	for i in range(len(weights)-1):
		activation+=(weights[i]*inputs[i])
	return activation

def transform_act(act):
	return 1.0/(1.0+exp(-act))

def forward_pass(network,row):
	inputs=row
	for layer in network:
		new_inp=[]
		for neuron in layer:
			activation=activate(neuron['weight'],inputs)
			neuron['output']=transform_act(activation)
			new_inp.append(neuron['output'])
		inputs=new_inp
	return inputs

def transform_output(output):
	return output*(1.0-output)

def backward_pass(network,expected):
	for i in reversed(range(len(network))):
		layer=network[i]
		errors=list()
		if i != (len(network)-1):
			for j in range(len(layer)):
				error=0.0
				for neuron in network[i+1]:
					error+=neuron['weight'][j]*neuron['delta']
				errors.append(error)
		else:
			for j in range(len(layer)):
				neuron=layer[j]
				errors.append(expected[j]-neuron['output'])
		for j in range(len(layer)):
			neuron=layer[j]
			neuron['delta']=errors[j]*transform_output(neuron['output'])

def update_weight(network,row,eta):
	for i in range(len(network)):
		inputs=row[:-1]
		if i!=0:
			inputs=[neuron['output'] for neuron in network[i-1]]
		for neuron in network[i]:
			for j in range(len(inputs)):
				neuron['weight'][j]+=eta*inputs[j]*neuron['delta']
			neuron['weight'][j]+=eta*neuron['delta']

def train_net(dataset,n_outputs,eta,n,network):
	for i in range(n):
		sum_error=0
		for row in dataset:
			output=forward_pass(network,row)
			expected=[0 for i in range(n_outputs)]
			expected[row[-1]]=1
			sum_error+= sum((expected[j]-output[j])**2 for j in range(len(expected)))
			backward_pass(network,expected)
			update_weight(network,row,eta)
		print('\nn={0}  learning_rate={1}  error={2}\n'.format(i,eta,sum_error))
			

seed()
dataset=[[0,0,0],[0,1,1],[1,0,1],[1,1,1]]
n_inputs=len(dataset[0])-1
print('\nNo of inputs: ',n_inputs)
n_outputs=len(set(row[-1] for row in dataset))
print('\nOutputs: ',n_outputs)

network=init_net(n_inputs,2,n_outputs)

train_net(dataset,n_outputs,0.5,20,network)

print('\nFinal network\n')
i=1
for layer in network:
	j=1
	for sub in layer:
		print('\nLayer[{0}] Node[{1}]: '.format(i,j),sub)
		j=j+1
	i=i+1

