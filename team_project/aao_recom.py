import tensorflow as tf
import numpy as np
from team_project.daocert import DaoCert
from team_project.daocertposs import DaoCertPoss
from team_project.daorecom import DaoRecom
import cx_Oracle
from sqlalchemy.sql.expression import except_

class AaoRecom : 
    def __init__(self):
        self.dc = DaoCert()
        self.dcp = DaoCertPoss()
        self.dr = DaoRecom()
        
        self.cnt = self.dc.getCnt()
        
        self.x_train = None
        self.y_train = None
        
        self.cert_labels = self.dc.getLabels()
        self.emp_labels = self.dcp.getLabels()
        self.label_name = self.dcp.selectList()
        
        # print(self.cert_labels)
        # print(len(self.cert_labels))
        # print(self.emp_labels)
        # print(len(self.emp_labels))
        self.setXYTrain()
        
        # print("x_train", self.x_train)
        # print("x_train", self.x_train.shape)
        # print("y_train", self.y_train)
        # print('cnt', self.cnt)
        
    def setXYTrain(self):
        self.x_train, self.y_train = self.dcp.getXtYt()
        
    def pred(self):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=(12,)),
            tf.keras.layers.Dense(512, activation=tf.nn.relu),
            tf.keras.layers.Dense(512, activation=tf.nn.relu),
            tf.keras.layers.Dense(self.cnt, activation=tf.nn.softmax)
        ])
        
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        
        # print("self.x_train",self.x_train)
        # print("self.y_train",self.y_train)
        
        model.fit(self.x_train, self.y_train, epochs=20)
        
        pred = model.predict(self.x_train)
        print(pred)
        for idx,i in enumerate(pred):
            try:
                myidx = np.argmax(i)
                print(self.label_name[idx]['emp_dept'], self.label_name[idx]['emp_annual'], myidx, 1 )
                self.dr.insertRecom(self.label_name[idx]['emp_dept'],self.label_name[idx]['emp_annual'], myidx, 1 )
                
                i[myidx] = 0
                myidx2 = np.argmax(i)
                print(self.label_name[idx]['emp_dept'], self.label_name[idx]['emp_annual'], myidx2, 2 )
                self.dr.insertRecom(self.label_name[idx]['emp_dept'],self.label_name[idx]['emp_annual'], myidx2, 2 )                
                
                i[myidx2] = 0
                myidx3 = np.argmax(i)
                print(self.label_name[idx]['emp_dept'], self.label_name[idx]['emp_annual'], myidx3, 3 )
                self.dr.insertRecom(self.label_name[idx]['emp_dept'],self.label_name[idx]['emp_annual'], myidx3, 3 )
                
            except cx_Oracle.DatabaseError as e:
                print(e)
                continue
            # print(cert_no2, self.emp_dept, self.emp_annual,2)
            # print(cert_no3, self.emp_dept, self.emp_annual,3)
if __name__ == '__main__' :
    ar = AaoRecom()
    ar.pred()
