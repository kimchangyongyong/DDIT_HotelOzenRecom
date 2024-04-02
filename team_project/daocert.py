import cx_Oracle

# 자격증 다오(추천 대상 ex/객실 타입, 멤버십, 부대시설, 렌터카에 해당)

class DaoCert: 

    def __init__(self):
        self.conn = cx_Oracle.connect('TEAM1_202308F/java@112.220.114.130:1521/xe')
        self.cur = self.conn.cursor()
    
    def getCnt(self):
        sql = '''
            SELECT 
                COUNT(*)
            FROM TB_CERT
        '''
        self.cur.execute(sql)
        cnt = self.cur.fetchone()
        return cnt[0] + 1
        # 자격증 넘버링은 1 ~ 31번에 돼있음. 0번이 없기 때문에 0을 포함시켜주기 위해 +1
        # 모델 학습에서 아웃풋 개수가 됨
    
    def getLabels(self):
        sql = """
            SELECT 
                TO_NUMBER(REGEXP_REPLACE(CERT_NO, 'CERT0*', '')),
                CERT_NO
            FROM TB_CERT_POSS
            INNER JOIN TB_EMP ON (TB_EMP.EMP_NO = TB_CERT_POSS.EMP_NO)
            GROUP BY TO_NUMBER(REGEXP_REPLACE(CERT_NO, 'CERT0*', '')), CERT_NO
            ORDER BY TB_CERT_POSS.CERT_NO
        """
        self.cur.execute(sql)
        cert_list = self.cur.fetchall()
        myjson = []
        for m in cert_list: 
            myjson.append({'cert_label':m[0], 'cert_no':m[1]})
        return myjson
        # 라벨링을 위한 메서드 
        # ex/ 실제 프라이머리키 이름 : CERT001 
        # 추천에 사용할 이름 : 1 
        # 자격증 이름 : 호텔 관리사
        # 숫자 1이 호텔 관리사를 뜻함을 알기 위한 메서드
        # 쿼리에서 TO_NUMBER(REGEXP_REPLACE(CERT_NO, 'CERT0*', '')) 이 부분은 CERF001로 돼있는 자격증의 기본키를 ==> 1로 추출하는 역할을 함.
        # 다른 테이블에서도 동작하는거 확인했으니까   CERT_NO, 'CERT0*' 에서 CERT만 바꿔서 쓸사람은 쓸것
        # CERT0* 에서 대소문자 지켜서 써야함!!
        
    def selectList(self):
        sql = """ 
            SELECT 
            CERT_NO
            , CERT_NM
            , DECODE(USE_Y, 'Y', 'O', 'N', 'X', '-')
            FROM TB_CERT
        """  
        self.cur.execute(sql)
        
        cert_list = self.cur.fetchall()  
        
        myjson = []
        for m in cert_list: 
            myjson.append({'cert_no':m[0], 'cert_nm':m[1], 'use_y':m[2]})
        return myjson
    
    def __del__(self):
        self.cur.close()
        self.conn.close()
    
if __name__ == '__main__':
    dc = DaoCert()
    print(dc.getLabels())
    # print(dc.selectList())
