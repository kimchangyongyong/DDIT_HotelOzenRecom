import cx_Oracle
import numpy as np

def convertBinary(number):
    binary_representation = bin(number)[2:]  
    filled_binary = binary_representation.zfill(6)
    return filled_binary
# x_train 라벨, 년차는 2진법으로 6자리까지 표현함

class DaoCertPoss: 

    def __init__(self):
        self.conn = cx_Oracle.connect('TEAM1_202308F/java@112.220.114.130:1521/xe')
        self.cur = self.conn.cursor()
    
    def selectList(self):
        sql = """ 
            SELECT 
                TB_CERT_POSS.EMP_NO
                , TB_EMP.EMP_DEPT
                , EXTRACT (YEAR FROM SYSDATE) - EXTRACT (YEAR FROM TB_EMP.EMP_JNCMP_YMD) +1
                , TB_EMP.EMP_TOEIC_SCORE
                , TB_EMP.EMP_TOEFL_SCORE
                , TB_CERT_POSS.CERT_NO
                , TB_CERT.CERT_NM
            FROM TB_CERT_POSS
                INNER JOIN TB_EMP ON (TB_CERT_POSS.EMP_NO = TB_EMP.EMP_NO)
                INNER JOIN TB_CERT ON (TB_CERT_POSS.CERT_NO = TB_CERT.CERT_NO)
            ORDER BY TB_EMP.EMP_NO
        """
        self.cur.execute(sql)
        
        cert_list = self.cur.fetchall()  
        
        myjson = []
        for m in cert_list: 
            myjson.append({'emp_no':m[0], 'emp_dept':m[1], 'emp_annual':m[2]
                           , 'emp_toeic':m[3], 'emp_toefl':m[4]
                           , 'cert_no':m[5], 'cert_nm':m[6]})
        return myjson
        # 이용 데이터 조회 메서드(이용내역, 예약 내역, 체크인 내역 등)
        # 연차는 쿼리를 통해 계산함(객실 이용내역, 부대시설 이용 내역 등 확인 필요)
        # 이용 데이터는 키값만 가지고 추천 데이터(mbti, 성별, 나이 등등)는 없으므로 기존 사람 테이블(직원, 고객 등)과 조인해서 해당 추천 데이터를 조회함
        
    def getXtYt(self):
        sql = f'''
                SELECT 
                    E_ANNUAL.EMP_ANNUAL,
                    E_ANNUAL.EMP_DEPT,
                    TO_NUMBER(REGEXP_REPLACE(TB_CERT_POSS.CERT_NO, 'CERT0*', '')) AS CERT_NO
                FROM (
                    SELECT 
                        EMP_NO,
                        DECODE(EMP_DEPT,'FMT','100000'
                                        ,'HKP','010000'
                                        ,'FTO','001000'
                                        ,'CRM','000100'
                                        ,'POS','000010'
                                        ,'HRM','000001') EMP_DEPT,
                        EXTRACT(YEAR FROM SYSDATE) - EXTRACT(YEAR FROM EMP_JNCMP_YMD) + 1 AS EMP_ANNUAL
                    FROM 
                        TB_EMP
                ) E_ANNUAL
                    INNER JOIN 
                        TB_CERT_POSS ON E_ANNUAL.EMP_NO = TB_CERT_POSS.EMP_NO
                    INNER JOIN 
                        TB_EMP E ON TB_CERT_POSS.EMP_NO = E.EMP_NO
                    INNER JOIN 
                        TB_CERT C ON TB_CERT_POSS.CERT_NO = C.CERT_NO
                    ORDER BY E.EMP_NO
        '''
        self.cur.execute(sql)
        cert_list = self.cur.fetchall()
        # print(cert_list)
        
        xt = []
        yt = [] 
        for i in cert_list :
            # print(i)
            xt.append(list(convertBinary(i[0])) + list(i[1]))
            yt.append(i[2])
        

        # print("xt",xt)
        # print("yt",yt)
        
        x_train = np.array(xt)
        x_train = x_train.astype(int)
        y_train = np.array(yt)
        # for idx,i in enumerate(x_train) : 
        #     print(x_train[idx], y_train[idx])
        # print("y_train",y_train)
        
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
            SELECT 
                TB_EMP.EMP_DEPT,
                EXTRACT(YEAR FROM SYSDATE) - EXTRACT(YEAR FROM TB_EMP.EMP_JNCMP_YMD) + 1 AS EMP_ANNUAL,
                TO_NUMBER(REGEXP_REPLACE(CERT_NO, 'CERT0*', '')),
                CERT_NO
            FROM TB_CERT_POSS
            INNER JOIN TB_EMP ON (TB_EMP.EMP_NO = TB_CERT_POSS.EMP_NO)
            GROUP BY TB_EMP.EMP_DEPT, EXTRACT(YEAR FROM SYSDATE) - EXTRACT(YEAR FROM TB_EMP.EMP_JNCMP_YMD) + 1,CERT_NO
            ORDER BY TB_CERT_POSS.CERT_NO
        '''
        self.cur.execute(sql)
        
        cert_list = self.cur.fetchall()  
        
        myjson = []
        for m in cert_list: 
            myjson.append({'emp_dept':m[0], 'emp_annual':m[1]})
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
    dcp = DaoCertPoss()
    print(dcp.selectList())
    # print(dcp.getLabels())
    # print(dcp.getXtYt())
    
