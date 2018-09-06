from sklearn import svm
import numpy as np
import motiontracker.py as mt
from sklearn.externals import joblib
from ola.ClientWrapper import ClientWrapper
import sys


X=np.array([[2,3],[8,9],[2,1],[7,7]])

y=[1,2,3,4]
padrao=[]
wrapper = None
universe = 1



model = svm.SVC(kernel='linear',decision_function_shape='ovr') # criacao do svm

print y
print X

model.fit(X,y)   # treinamento do svm

print(model.predict([[11,10]]))


acc_x = 15
acc_y = 10
acc_z = 13
angv_x = 10
angv_y = 12
angv_z = 13
deg_x = 10
deg_y = 11
deg_z = 13



joblib.dump(model,'modelo.pkl')  #salva o modelo atual em um arquivo pickle


gatilho= True


buffer = np.zeros(50) # o buffer vai receber em tempo real os valores de aceleracao 


while gatilho: # loop do buffer, que continuara recebendo os valores e tentanto achar algum padrao correspondende, a principio vamos fazer  20k de amostras e ir incrementando no vetor de 50 em 50, se ficar muito pesado 
			# vamos diminuindo o numero de amostras
	buffer = np.roll(buffer,5) # rotaciona 5 espacos 
	buffer[:5] =  acc_x,acc_y,acc_z,angv_x,angv_y   # adiciona 5 valores para o inicio do buffer
	padrao=model.predict(buffer)
if padrao == 1
	data = 50
elif padrao == 2
	data = 100
elif padrao == 3
	data = 150
elif padrao == 4
	data = 200



global wrapper
wrapper = ClientWrapper()
client = wrapper.Client()
client.SendDmx(universe,data,DmxSent)
wrapper.run
