import cx_Oracle

def convertLabel(cert_label):
    return "CERT" + str(cert_label).zfill(3)

class DaoRecom: 

    def __init__(self):
        self.conn = cx_Oracle.connect('TEAM1_202308F/java@112.220.114.130:1521/xe')
        self.cur = self.conn.cursor()
    
    def selectRecom(self):
        sql = """
            SELECT
                EMP_DEPT
                , EMP_ANNUAL
                , CERT_NO
            FROM TB_RECOM_CERT
        """
        self.cur.execute(sql)
        recom = self.cur.fetchall()
        myjson = []
        for r in recom :
            myjson.append({'emp_dept':r[0], 'emp_annual':r[1], 'cert_no':r[2]})
        return myjson
    def insertRecom(self, emp_dept, emp_annual, cert_label, recom_rank):
        cert_no = convertLabel(cert_label)
        
        sql = f"""
            INSERT INTO TB_RECOM_CERT(
                EMP_DEPT
                , EMP_ANNUAL
                , CERT_NO
                , RECOM_RANK                
            ) VALUES(
                '{emp_dept}'
                ,'{emp_annual}'
                ,'{cert_no}'
                , '{recom_rank}'
            )
        """
        self.cur.execute(sql)
        self.conn.commit()
        
        rowcnt = self.cur.rowcount
        
        return rowcnt
    # 추천 테이블에 실제로 인서트하는 메서드. 추천 데이터(나이, 성별, mbti, 인원수...)를 메서드의 파라미터로 받음. 
    # 만약 추천을 n위까지 하고싶으면 rank(임시 이름)같은 칼럼이 추가되어야함. 몇번째로 추천하는 데이터인지 구분 필요.

        
    def __del__(self):
        self.cur.close()
        self.conn.close()
        
if __name__ == "__init__":
    dr = DaoRecom()
