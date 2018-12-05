import numpy as np
from bokeh.plotting import show,figure,output_notebook
from bokeh.layouts import gridplot
from bokeh.io import push_notebook

def local_reg(x0,X,y,tau):
	x0=np.r_[1,x0]
	X=np.c_[np.ones(len(X)),X]
	
	xw=X.T * radial(x0,X,tau)
	beta= np.linalg.pinv(xw @ X) @ xw @ y
	return x0 @ beta
	
def radial(x0,X,tau):
	return np.exp(np.sum((X-x0)**2,axis=1)/(-2*tau*tau))

n=1000
X=np.linspace(-3,3,num=n)
print('\nX samples: ',X[1:10])
y=np.log(np.abs(X**2 -1)+.5)
print('\ny samples: ',y[1:10])
X+=np.random.normal(scale=.1,size=n)
print('\nX samples: ',X[1:10])
domain=np.linspace(-3,3,num=300)

def plt_lwr(tau):
	prediction=[local_reg(x0,X,y,tau) for x0 in domain]
	plot=figure(plot_width=400,plot_height=400)
	plot.scatter(X,y,alpha=.3)
	plot.line(domain,prediction,line_width=2,color='red')
	plot.title.text="tau=%g" %tau
	return plot

show(gridplot([[plt_lwr(10.),plt_lwr(1.)],[plt_lwr(0.1),plt_lwr(0.01)]]))
