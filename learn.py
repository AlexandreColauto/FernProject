from sklearn import svm
from sklearn import preprocessing
import numpy as np
import motiontracker as mt
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
import sys
import time


##Variaveis, costume de C em declarar elas antes

rng=input('digite o valor do range :') ## o range sao quantas amostras eu vou ter
slp=.5/rng #esse e o tempo de espera entre uma amostra e outra
svm_vector=np.array([[0 for i in range(rng*9)]])   # o vetor que vai receber as amostras, o tamanho dele e proporcional ao numero de amostras sao 9 dados vezes o numero de amostras
model= svm.SVC(decision_function_shape='ovr') # esse e o classificador, o SVM, A pricipio so esta com um parametro determinado, que e a forma de comparacao one vs rest, mas ainda tenho que setar o C que e a tolerancia e o gamma que e a taxa de aprendizagem
label=np.array([4]) #esse vetor vai guardar o rotulo de cada amostra, comecei com 4 so para inicializar, mas depois eu dispenso as primeiras posicoes
mpu = mt.MotionTracker(bd_addr="20:17:12:04:51:13") # faz a conexao com o dispostivo bluetooth
try:
	mpu.start_read_data()
	time.sleep(3.5)
	print(slp)
	while (1):
		modelo=input('Digite o padrao :')  # esse e o rotulo do padrao que eu vou gravar a seguir
		if modelo==99:
			break
		else:
			for j in range(40):    # a principio eu treino 40 vezes cada padrao
				x=np.array([mpu.ang_x,mpu.acc_x,mpu.angv_x,mpu.ang_y,mpu.acc_y,mpu.angv_y,mpu.ang_z,mpu.acc_z,mpu.angv_z])
				for i in range(rng-1):
					x=np.append(x,[mpu.ang_x,mpu.acc_x,mpu.angv_x,mpu.ang_y,mpu.acc_y,mpu.angv_y,mpu.ang_z,mpu.acc_z,mpu.angv_z])
					#time.sleep(slp)
				label=np.append(label,modelo)
				svm_vector=np.append(svm_vector,[x],0)
	X_train,X_test,y_train,y_test = train_test_split(svm_vector[1:],label[1:],test_size=0.2) # esta funcao reparte meus dados em 80% para treinar e 20% de teste para conseguir obter o score do meu modelo
	model.fit(X_train,y_train)  #treino o modelo
	print(model.score(X_test,y_test))  # exibo o score do meu modelo ou seja quantas vezes ele acertou em predizer corretamente a informacao,atualmente estou em 80% mais ou menos com essas configuracoes
	joblib.dump(model,'model.pkl')    # isso e para salvar o modelo em um arquivo para poder abrir no outro programa
	print('JOB`S DONE!')


except KeyboardInterrupt:
	mpu.stop_read_data()
	raise
