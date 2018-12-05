import csv

def g_0(n):
	return ('?', )*n

def s_0(n):
	return ('$', )*n

def more_general(h,x):
	more_general_parts=[]
	for x,y in zip(h,x):
		mg=x=='?' or (x!='$' and (x==y or y=='$'))
		more_general_parts.append(mg)
	return all(more_general_parts)

def fulfills(x,h):
	more_general(h,x)

def min_generalise(x,h):
	h_new=list(h)
	for i in range(len(h)):
		if not fulfills(x[i:i+1],h[i:i+1]):
			h_new[i]='?' if h[i]!='$' else x[i]
	return [tuple(h_new)]

def min_specialise(x,h,domains):
	result=[]
	for i in range(len(h)):
		if h[i]=='?':
			for val in domains[i]:
				if x[i]!=val:
					h_new=h[:i] + (val, )+h[i+1:]
					result.append(h_new)
	return result

def generalise_S(x,G,S):
	S_prev=list(S)
	for s in S_prev:
		if not fulfills(x,s):
			S.remove(s)
			Splus=min_generalise(x,s)
			S.update([h for h in Splus if any([more_general(g,h) for g in G])])
			S.difference_update([h for h in S if any([more_general(h,h1) for h1 in S if h!=h1])])
	return S

def specialise_G(x,domains,G,S):
	G_prev=list(G)
	for g in G_prev:
		if fulfills(x,g):
			G.remove(g)
			Gplus=min_specialise(x,g,domains)
			G.update([h for h in Gplus if any([more_general(h,s) for s in S])])
			G.difference_update([h for h in G if any([more_general(h1,h) for h1 in G if h!=h1])])
	return G

with open('Training_examples.csv') as csvfile:
	examples=[tuple(line) for line in csv.reader(csvfile)]

def get_domains(examples):
	d=[set() for i in range(len(examples[0]))]
	for x in examples:
		for i,xi in enumerate(x):
			d[i].add(xi)
	return [list(sorted(x)) for x in d]

def candidate(examples):
	domains=get_domains(examples)[:-1]
	print(domains)
	G=set([g_0(len(domains))])
	S=set([s_0(len(domains))])
	i=0
	print('\nG[{0}]: '.format(i),G)
	print('\nS[{0}]: '.format(i),S)
	for xcx in examples:
		i=i+1
		x,cx=xcx[:-1],xcx[-1]
		if cx=='Y':
			G={g for g in G if fulfills(x,g)}
			S=generalise_S(x,G,S)
		else:
			S={s for s in S if not fulfills(x,s)}
			G=specialise_G(x,domains,G,S)
		print('\nG[{0}]: '.format(i),G)
		print('\nS[{0}]: '.format(i),S)
	return



candidate(examples)
