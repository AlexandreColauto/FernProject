from sklearn import svm
from sklearn import preprocessing
import numpy as np
import motiontracker as mt
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import sys
import time


##Variaveis

rng=input('digite o valor do range :') ## o range sao quantas amostras eu vou ter

slp=3.0/rng #esse e o tempo de espera entre uma amostra e outra

svm_vector=np.array([[0 for i in range(rng*9)]])   # o vetor que vai receber as amostras, o tamanho dele e proporcional ao numero de amostras sao 9 dados vezes o numero de amostras

model_svm= svm.SVC(C=0.001, cache_size=1000,kernel='rbf') # esse e o classificador, o SVM, A pricipio so esta com um parametro determinado, que e a forma de comparacao one vs rest, mas ainda tenho que setar o C que e a tolerancia e o gamma que e a taxa de aprendizagem
model_LogR=LogisticRegression() # devido a falta de precisao do SVM, foi testado o LogisticRegression para comparar a acuracia

label=np.array([4]) #esse vetor vai guardar o rotulo de cada amostra, comecei com 4 so para inicializar, mas depois eu dispenso as primeiras posicoes

mpu = mt.MotionTracker(bd_addr="20:17:12:04:51:13") # faz a conexao com o dispostivo bluetooth





try:
	mpu.start_read_data()
	time.sleep(3.5)
	print(slp)
	while (1):
		modelo=input('Digite o padrao :')  # esse e o rotulo do padrao que eu vou gravar a seguir
		if modelo==99:    # o padrao 99 finaliza o aprendizado
			break
		else:
			for j in range(45):    # a principio e treinado 45 vezes cada padrao
				x=np.array([])
				Accx=np.array([mpu.acc_x])
				Accy=np.array([mpu.acc_y])
				Accz=np.array([mpu.acc_z])
				Angx=np.array([mpu.ang_x])
				Angy=np.array([mpu.ang_y])
				Angz=np.array([mpu.ang_z])
				Accax=np.array([mpu.angv_x])
				Accay=np.array([mpu.angv_y])
				Accaz=np.array([mpu.angv_z])
				for i in range(rng-1):
					Accx=np.append(Accx,[mpu.acc_x])
					Accy=np.append(Accy,[mpu.acc_y])
					Accz=np.append(Accz,[mpu.acc_z])
					Angx=np.append(Angx,[mpu.ang_x])
					Angy=np.append(Angy,[mpu.ang_y])
					Angz=np.append(Angz,[mpu.ang_z])
					Accax=np.append(Accax,[mpu.angv_x])
					Accay=np.append(Accay,[mpu.angv_y])
					Accaz=np.append(Accaz,[mpu.angv_z])
					time.sleep(slp)
				label=np.append(label,modelo)
				print(j)
				x=np.append(x,[Accx,Accy,Accz,Angx,Angy,Angz,Accax,Accay,Accaz])
				svm_vector=np.append(svm_vector,[x],0)
	X_train,X_test,y_train,y_test = train_test_split(svm_vector[1:],label[1:],test_size=0.2) # esta funcao reparte meus dados em 80% para treinar e 20% de teste para conseguir obter o score do meu modelo
	model_LogR.fit(X_train,y_train) # Treinamento do Logistic Regression
	model_svm.fit(X_train,y_train)  # Treinamento do SVM
	print(model.score(X_test,y_test),model1.score(X_test,y_test))  # exibo o score do meu modelo ou seja quantas vezes ele acertou em predizer corretamente a informacao
	joblib.dump(model_svm,'model.pkl')    # isso e para salvar o modelo svm em um arquivo para poder abrir no outro programa
	joblib.dump(model_LogR,'model1.pkl')  # e aqui salvamos o modelo da regressao logistica.
	print('JOB`S DONE!')


except KeyboardInterrupt:
	mpu.stop_read_data()
	raise
