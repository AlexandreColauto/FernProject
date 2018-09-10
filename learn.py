from sklearn import svm
from sklearn import preprocessing
import numpy as np
import motiontracker as mt
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
import sys
import time


loop='n'


i = 0
rng=input('digite o valor do range :')
slp=.5/rng
modelo=0
svm_vector=np.array([[0 for i in range(rng*9)]])
model= svm.SVC(decision_function_shape='ovr')
label=np.array([4])
mpu = mt.MotionTracker(bd_addr="20:17:12:04:51:13")
try:
	mpu.start_read_data()
	time.sleep(3.5)
	print(slp)
	while (1):
		modelo=input('Digite o padrao :')
		if modelo==99:
			break
		else:
			for j in range(40):
				x=np.array([mpu.ang_x,mpu.acc_x,mpu.angv_x,mpu.ang_y,mpu.acc_y,mpu.angv_y,mpu.ang_z,mpu.acc_z,mpu.angv_z])
				for i in range(rng-1):
					x=np.append(x,[mpu.ang_x,mpu.acc_x,mpu.angv_x,mpu.ang_y,mpu.acc_y,mpu.angv_y,mpu.ang_z,mpu.acc_z,mpu.angv_z])
					#time.sleep(slp)
				label=np.append(label,modelo)
				svm_vector=np.append(svm_vector,[x],0)
	X_train,X_test,y_train,y_test = train_test_split(svm_vector[1:],label[1:],test_size=0.2)
	model.fit(X_train,y_train)
	print(model.score(X_test,y_test))
	joblib.dump(model,'model.pkl')
	print('JOB`S DONE!')







	time.sleep(.5)
	while(loop == 'y'):
		buffer= np.roll(buffer,9)
		print(mpu.ang_x,mpu.acc_x,mpu.angv_x,mpu.ang_y,mpu.acc_y,mpu.angv_y,mpu.ang_z,mpu.acc_z,mpu.angv_z)
		buffer[:9]=mpu.ang_x,mpu.acc_x,mpu.angv_x,mpu.ang_y,mpu.acc_y,mpu.angv_y,mpu.ang_z,mpu.acc_z,mpu.angv_z
		print(buffer[:20])
		time.sleep(.1)
		if (buffer[-1] != 0):
			saida=model.predict([buffer])
			buffer=np.array([0 for i in range(180)],dtype=float)
			print(saida,'DEU CERTO KOROIII')
			loop=input('continuar no loop : ')
except KeyboardInterrupt:
	mpu.stop_read_data()
	raise
	
