import pandas as pd
from pandas import DataFrame

df_tennis=DataFrame.from_csv('tennis.csv')
print('\nDataset: \n',df_tennis)

def entropy(probs):
	import math
	return sum([-prob*math.log(prob,2) for prob in probs])

def entropy_list(a_list):
	from collections import Counter
	cnt=Counter(x for x in a_list)
	num_inst=len(a_list)*1.0
	print('\nNo of instanses in the current sub class: ',num_inst)
	probs=[x/num_inst for x in cnt.values()]
	print('\nClasses are: ',min(cnt),max(cnt))
	print('\n Probabilty of Class {0} is {1}'.format(min(cnt),min(probs)))
	print('\n Probabilty of Class {0} is {1}'.format(max(cnt),max(probs)))
	return entropy(probs)

print('\nToal entropy of original dataset: \n')
total_entropy=entropy_list(df_tennis['PlayTennis'])
print(total_entropy)

def info_gain(df,split_attr,target_attr,trace=0):
	print('\nCalculation of info_gain for ',split_attr)
	df_split=df.groupby(split_attr)
	for name,grp in df_split:
		print('\n',name)
		print('\n',grp)
	nobs=len(df.index)*1.0
	print('\nNOBS = ',nobs)
	df_agg_ent=df_split.agg({target_attr:[entropy_list, lambda x: len(x)/nobs]})[target_attr]
	print([target_attr])
	df_agg_ent.columns=['Entropy','ProbObs']
	print('\nDFAGGENT: ',df_agg_ent)
	if trace:
		print(df_agg_ent)
	
	new_ent=sum(df_agg_ent['Entropy']*df_agg_ent['ProbObs'])
	old_ent=entropy_list(df[target_attr])
	return old_ent-new_ent

print('Information Gain of Outlook: '+str(info_gain(df_tennis,'Outlook','PlayTennis')))
print('Information Gain of Temp: '+str(info_gain(df_tennis,'Temperature','PlayTennis')))
print('Information Gain of Humidity: '+str(info_gain(df_tennis,'Humidity','PlayTennis')))
print('Information Gain of Wind: '+str(info_gain(df_tennis,'Wind','PlayTennis')))

def id3(df,target_attr,attributes,default_class=None):
	from collections import Counter
	cnt=Counter(x for x in df[target_attr])
	print('\nCount: ',cnt)
	if len(cnt)==1:
		return next(iter(cnt))
	elif df.empty or (not attributes):
		return default_class
	else:
		default_class=max(cnt.keys())
		gainz=[info_gain(df,attr,target_attr) for attr in attributes]
		max_index=gainz.index(max(gainz))
		bst_attr=attributes[max_index]
		tree={bst_attr:{}}
		remaining_attr= [attr for attr in attributes if attr!=bst_attr]
		for att_val,subset in df.groupby(bst_attr):
			subtree=id3(subset,target_attr,remaining_attr,default_class)
			tree[bst_attr][att_val]=subtree
		return tree

attributes=list(df_tennis.columns)
print('\nAttributes: ',attributes)
attributes.remove('PlayTennis')
print('\nPredicting attr: ',attributes)

from pprint import pprint
tree=id3(df_tennis,'PlayTennis',attributes)
pprint(tree)

def classify(instance,tree,default=None):
	attribute=next(iter(tree))
	print('\nKey: ',tree.keys())
	print('\nAttribute: ',attribute)
	if instance[attribute] in tree[attribute].keys():
		result=tree[attribute][instance[attribute]]
		print('\nAttribute instance ',instance[attribute])
		print('\nTreeKeys: ',tree[attribute].keys())
		if isinstance(result,dict):
			return classify(instance,result)
		else:
			return result
	else:
		return default
	
training_data=df_tennis.iloc[1:-4]
test_data=df_tennis[-4:]
train_tree=id3(training_data,'PlayTennis',attributes)

test_data['predict']=test_data.apply(classify,axis=1,args=(train_tree,'Yes'))
print('\nAccuracy is '+str(sum(test_data['PlayTennis']==test_data['predict'])/(1.0*len(test_data.index))))
