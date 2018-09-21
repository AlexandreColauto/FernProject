
from __future__ import print_function
from sklearn import svm
import numpy as np
import motiontracker as mt
from sklearn.externals import joblib
from ola.ClientWrapper import ClientWrapper
import sys
import time
import array

mpu=mt.MotionTracker(bd_addr="20:17:12:04:51:13")

model_svm = joblib.load('model.pkl') # criacao do svm
model_LogR = joblib.load('model1.pkl') # criacao do  logistic regression


gatilho= True # Apenas para manter no loop
rng=250   # Rng e o sample rate, ou seja quantas amostras eu vou pegar em um segundo
slp=3.0/rng # o tempo entre uma amostra e outra
arry=9*rng  # o tamanho do vetor que recebera as amostras
universe=1  # o universo criado no OLA
data=array.array('B') # O pacote de dados que sera enviado via dmx, o parametro B representa o UNSIGNED





for i in range(11):
	data.append(0)   # inicializo o vetor data  com 0 nas 11 primeiras posicoes, pois o dispositivo utilizado neste projeto (Triton sp 250 mini), possui apenas 11 canais controlaveis

global wrapper
wrapper = ClientWrapper()
client = wrapper.Client()


def DmxSent(status):
	if status.Succeeded():
		print("success")
	else:
		print('Error %s' %status.message, file=sys.stderr)
	global wrapper
	if wrapper:
		wrapper.Stop()

# o buffer vai receber em tempo real os valores de aceleracao

mpu.start_read_data()
time.sleep(2.5)
print('here we go!')
while gatilho: # loop do buffer, que continuara recebendo os valores e tentanto achar algum padrao correspondende
	buffer=np.array([]) # zera o buffer, para as amostras anteriores nao influenciar na atual
	Accx=np.array([mpu.acc_x])
	Accy=np.array([mpu.acc_y])
	Accz=np.array([mpu.acc_z])
	Acgx=np.array([mpu.ang_x])
	Acgy=np.array([mpu.ang_y])
	Acgz=np.array([mpu.ang_z])
	Acax=np.array([mpu.angv_x])
	Acay=np.array([mpu.angv_y])
	Acaz=np.array([mpu.angv_z])
	for i in range(rng-1):
		Accx=np.append(Accx,[mpu.acc_x])
		Accy=np.append(Accy,[mpu.acc_y])
		Accz=np.append(Accz,[mpu.acc_z])
		Acgx=np.append(Acgx,[mpu.ang_x])
		Acgy=np.append(Acgy,[mpu.ang_y])
		Acgz=np.append(Acgz,[mpu.ang_z])
		Acax=np.append(Acax,[mpu.angv_x])
		Acay=np.append(Acay,[mpu.angv_y])
		Acaz=np.append(Acaz,[mpu.angv_z])
		time.sleep(slp)



	buffer=np.append(buffer,[Accx,Accy,Accz,Acgx,Acgy,Acgz,Acax,Acay,Acaz])
	padrao=model_svm.predict([buffer]) #previsao com o SVM
	padrao1=model_LogR.predict([buffer]) # previsao com o logistic regression, para comparacao de precisao
	print(padrao,padrao1)



	# A partir do numero previsto e entao ativado um dos dois padroes de cores, o primeiro e com o dimmer a 30% cores mais calmas e sem piscar
	if padrao1==1:
		data[1]=125
		data[2]=38
		data[9]=150
	elif padrao1==2:    # o segundo ja e com o dimmer a 100%, cores alternantes e o efeito estrobbe
		data[3]=130
		data[1]=220
		data[0]=255
		data[9]=255
	client.SendDmx(universe,data,DmxSent)
	wrapper.Run() # envia os padroes para os dispositivos
	time.sleep(0.5)
