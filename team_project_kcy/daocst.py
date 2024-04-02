import cx_Oracle
import numpy as np


def convertBinary(number):
    binary_representation = bin(number)[2:]  
    filled_binary = binary_representation.zfill(6)
    return filled_binary
# x_train 라벨, 년차는 2진법으로 6자리까지 표현함


class DaoCst: 

    def __init__(self):
        self.conn = cx_Oracle.connect('TEAM1_202308F/java@112.220.114.130:1521/xe')
        self.cur = self.conn.cursor()
    
    def selectList(self):
        sql = """ 
       SELECT
                CST_NO
                , CST_GEN
                , CST_AGE
                , CI_CAR_KIND
                ,TO_NUMBER(REGEXP_REPLACE(CAR_NO, 'CAR*', ''))
            FROM (
                SELECT
                    CST_NO
                    , CASE
                        WHEN (2000 - EXTRACT(YEAR FROM CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 <= 24 
                        THEN '20'
                        WHEN (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 <= 29 
                            AND (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 >= 25 
                        THEN '25'
                        WHEN (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 <= 39 
                            AND (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 >= 30 
                        THEN '30'
                        WHEN (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 <= 49 
                            AND (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 >= 40 
                        THEN '40'
                        WHEN (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 <= 59 
                            AND (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 >= 50 
                        THEN '50'
                        WHEN (2000 - EXTRACT(YEAR FROM CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 >= 60 
                        THEN '60'
                    END AS CST_AGE
                    ,CST_GEN
                FROM 
                TB_CSTMR
                )
         INNER JOIN TB_CHKIN USING (CST_NO)
            INNER JOIN TB_CAR ON (TB_CHKIN.CI_CAR_KIND = TB_CAR.CAR_NO)
        """
        self.cur.execute(sql)
        
        cert_list = self.cur.fetchall()  
        
        myjson = []
        for c in cert_list: 
            myjson.append({'cst_no':c[0], 'cst_gen':c[1], 'cst_age':c[2], 'ci_car_kind':c[3]})
        return myjson
        # 이용 데이터 조회 메서드(이용내역, 예약 내역, 체크인 내역 등)
        # 연차는 쿼리를 통해 계산함(객실 이용내역, 부대시설 이용 내역 등 확인 필요)
        # 이용 데이터는 키값만 가지고 추천 데이터(mbti, 성별, 나이 등등)는 없으므로 기존 사람 테이블(직원, 고객 등)과 조인해서 해당 추천 데이터를 조회함
        
    def getXtYt(self):
        sql = f'''
            SELECT
                CST_GEN
                , CST_AGE
                ,TO_NUMBER(REGEXP_REPLACE(CAR_NO, 'CAR*', ''))
            FROM(
                SELECT
                    CST_NO
                    , CASE
                        WHEN (2000 - EXTRACT(YEAR FROM CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 <= 24 
                        THEN '100000'
                        WHEN (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 <= 29 
                            AND (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 >= 25 
                        THEN '010000'
                        WHEN (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 <= 39 
                            AND (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 >= 30 
                        THEN '001000'
                        WHEN (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 <= 49 
                            AND (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 >= 40 
                        THEN '000100'
                        WHEN (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 <= 59 
                            AND (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 >= 50 
                        THEN '000010'
                        WHEN (2000 - EXTRACT(YEAR FROM CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 >= 60 
                        THEN '000001'
                    END AS CST_AGE
                    ,CASE
                        WHEN CST_GEN = 'F' THEN '1'
                        WHEN CST_GEN = 'M' THEN '0'
                    END AS CST_GEN
                FROM TB_CSTMR) INNER JOIN TB_CHKIN USING (CST_NO)
            INNER JOIN TB_CAR ON (TB_CHKIN.CI_CAR_KIND = TB_CAR.CAR_NO)
        '''
        self.cur.execute(sql)
        car_list = self.cur.fetchall()
        
        arr = []
        xt = []
        yt = [] 
        for i in car_list:
            xt.append(list(i[0]) + list(i[1]))
            yt.append(i[2])
            
        x_train = np.array(xt)
        
        x_train = x_train.astype(int)
        y_train = np.array(yt)
        
        return x_train, y_train
    # xtrain과 ytrain을 실제로 구성하는 메서드. 100000, 010000...등 규칙은 알아서 정하고 decode 또는 라벨을 통해 정리할것
    # 단, 하나의 속성은 같은 자릿수를 가져야함. ex) 객실 이용 횟수 : 3회 미만 : 100 /// 5회 미만 : 010 /// 7회 미만 : 001 ... 
    # xtrain, ytrain은 넘피로 구성함. xtrain에서 하나의 데이터는 1차원이든 2차원이든 그것도 알아서 정할것. 단, 차원별로 분리해서 구성 필요
    # ex) [[1000001000000], [1000000100000]] ==> 1차원으로 이루어진 두개의 xtrain
    # [
    #     [
    #         [100000], [100000]
    #     ],
    #     [
    #         [100000], [010000]
    #     ]
    # ] ==> 2차원으로 이루어진 2개의 xtrain
    
    def getLabels(self):
        sql = '''
           SELECT * FROM (
            SELECT TB_CSTMR.CST_GEN
                , CASE
                    WHEN (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 <= 24 THEN 20
                    WHEN (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 <= 29 AND (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 >= 25 THEN 25
                    WHEN (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 <= 39 AND (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 >= 30 THEN 30
                    WHEN (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 <= 49 AND (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 >= 40 THEN 40
                    WHEN (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 <= 59 AND (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 >= 50 THEN 50
                    WHEN (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 >= 60 THEN 60
                END AS CST_AGE,
                TB_CAR.CAR_NO
            FROM TB_CHKIN
            INNER JOIN TB_CAR ON (TB_CHKIN.CI_CAR_KIND = TB_CAR.CAR_NO)
            INNER JOIN TB_CSTMR ON (TB_CHKIN.CST_NO = TB_CSTMR.CST_NO) ) CAR
            GROUP BY CAR.CST_GEN, CAR.CST_AGE, CAR.CAR_NO
            ORDER BY CAR.CAR_NO
             
        '''
        self.cur.execute(sql)
        
        cst_list = self.cur.fetchall()  
        
        myjson = []
        for c in cst_list: 
            myjson.append({'cst_gen':c[0], 'cst_age':c[1]})
        return myjson
    # recom 테이블에 실제로 인서트하는 값은 xtrain의 값이 아닌 기본키의 값을 넣음.
    # ex) 봄 xtrain : 1000 
    #     e(mbti) xtrain : 10 => 오젠 벚꽃길 추천
    #  ===> 인서트되는 값 : spring, e, SB015
    # xtrain이 ytrain을 도출하는 값을 토대로 원래의 값을 알아내기 위해 사용하는 라벨 메서드
    
    def __del__(self):
        self.cur.close()
        self.conn.close()

    
if __name__ == '__main__':
    dcp = DaoCst()
    print(dcp.selectList())
    print(dcp.getLabels())
    # xt, yt = dcp.getXtYt()
    # print('xt', xt)
    # print('yt', yt)
    
