import tensorflow as tf
import numpy as np
from team_project_kcy.daocst import DaoCst
from team_project_kcy.daocar import DaoCar
from team_project_kcy.daorecom import DaoRecom
import cx_Oracle

class CarRecom : 
    def __init__(self):
        self.cst = DaoCst()
        self.car = DaoCar()
        self.dr = DaoRecom()
        
        self.cnt = self.car.getCnt()
        
        self.x_train = None
        self.y_train = None
        
        self.car_labels = self.car.getLabels()
        self.cst_labels = self.cst.getLabels()
        self.label_name = self.cst.selectList()
        print(tf.__version__)
        # print(self.car_labels)
        # print(len(self.car_labels))
        # print(self.cst_labels)
        # print(len(self.cst_labels))
        
        self.setXYTrain()
        
        # print("x_train", self.x_train)
        # print("x_train", self.x_train.shape)
        # print("y_train", self.y_train)
        # print('cnt', self.cnt)
        
    def setXYTrain(self):
        self.x_train, self.y_train = self.cst.getXtYt()
        
    def pred(self):
        
        model = tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=(7,)),
            tf.keras.layers.Dense(2048, activation=tf.nn.relu),
            tf.keras.layers.Dense(2048, activation=tf.nn.relu),
            tf.keras.layers.Dense(self.cnt, activation=tf.nn.softmax)
        ])
        
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
       
        model.fit(self.x_train, self.y_train, epochs=20)
        model.summary();
        pred = model.predict(self.x_train)
        # model.save('recomCar.h5');
        # print(pred)
        for idx,i in enumerate(pred) :
            try:
                myidx = np.argmax(i)
                print(self.label_name[idx]['cst_gen'], self.label_name[idx]['cst_age'], myidx, 1 )
                # self.dr.insertRecom(self.label_name[idx]['cst_gen'],self.label_name[idx]['cst_age'], myidx, 1 )
                
                i[myidx] = 0
                myidx2 = np.argmax(i)
                print(self.label_name[idx]['cst_gen'], self.label_name[idx]['cst_age'], myidx2, 2 )
                # self.dr.insertRecom(self.label_name[idx]['cst_gen'],self.label_name[idx]['cst_age'], myidx2, 2 )                

                i[myidx2] = 0
                myidx3 = np.argmax(i)
                print(self.label_name[idx]['cst_gen'], self.label_name[idx]['cst_age'], myidx3, 3 )
                # self.dr.insertRecom(self.label_name[idx]['cst_gen'],self.label_name[idx]['cst_age'], myidx3, 3 )
                
            except cx_Oracle.DatabaseError as e:
                print(e)
                continue
            
if __name__ == '__main__' :
    ar = CarRecom()
    ar.pred()
