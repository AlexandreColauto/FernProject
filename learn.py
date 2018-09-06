from sklearn import svm
from sklearn import preprocessing
import numpy as np
import motiontracker as mt
from sklearn.externals import joblib
import sys
import time



i = 0
rng=20
#svm_vector=np.array([[0 for i in range(5)]])
model= svm.SVC(decision_function_shape='ovr')
mpu = mt.MotionTracker(bd_addr="20:17:12:04:51:13")
try:
	mpu.start_read_data()
	time.sleep(3.5)
	for j in range(5):
		x=np.array([[mpu.ang_x,mpu.acc_x,mpu.angv_x,mpu.ang_y,mpu.acc_y,mpu.angv_y,mpu.ang_z,mpu.acc_z,mpu.angv_z]])
		for i in range(rng-1):
			x=np.append(x,[[mpu.ang_x,mpu.acc_x,mpu.angv_x,mpu.ang_y,mpu.acc_y,mpu.angv_y,mpu.ang_z,mpu.acc_z,mpu.angv_z]],0)
			#y=np.append(y,x,axis=0)
			time.sleep(.1)
			#print(x)

		print(x)
		scaled_acc=preprocessing.StandardScaler().fit(x)
		y=scaled_acc.transform(x)
		if j == 0:
			svm_vector=np.array([y])
		else:
			svm_vector=np.append(svm_vector,[y],0)
	print svm_vector
	model.fit(y,[1])
	

except KeyboardInterrupt:
	mpu.stop_read_data()
	raise
	
