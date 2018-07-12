
# coding: utf-8

# In[172]:


from matplotlib import pyplot as PLT
from matplotlib import cm as CM
from matplotlib import mlab as ML
import numpy as NP


# In[185]:


n = 1e5
x = y = NP.linspace(0, 400, 400) #Valor min, valor max, Numero de divisões
X, Y = NP.meshgrid(x, y) #Transforma em grid
'''Quanto maior o numero de divisões mais qualidade a imagem tem'''
print(X)


# In[186]:


Z1 = ML.bivariate_normal(X, Y, 2, 2, 0, 0)
Z2 = ML.bivariate_normal(X, Y, 4, 1, 1, 1)
ZD = Z2 - Z1
print (ZD)


# In[189]:


x = X.ravel()
y = Y.ravel()
z = NP.random.randn(400*400)#ZD.ravel() #Tem que ser um array com (Numero de divisões)^2
print(x)
print(y)
print(z)


# In[190]:



gridsize=60
PLT.subplot(111)

# if 'bins=None', then color of each hexagon corresponds directly to its count
# 'C' is optional--it maps values to x-y coordinates; if 'C' is None (default) then 
# the result is a pure 2D histogram 

PLT.hexbin(x, y, C=z, gridsize=gridsize, cmap=CM.jet, bins=None)
PLT.axis([x.min(), x.max(), y.min(), y.max()])

cb = PLT.colorbar()
cb.set_label('mean value')
PLT.show()   

