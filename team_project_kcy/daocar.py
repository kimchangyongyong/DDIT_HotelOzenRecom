import cx_Oracle


class DaoCar:
    
    def __init__(self):
        self.conn = cx_Oracle.connect('TEAM1_202308F/java@112.220.114.130:1521/xe')
        self.cur = self.conn.cursor()
        
    def getCnt(self):
        sql = """
            SELECT
                COUNT(*)
            FROM TB_CAR
        """
        self.cur.execute(sql)
        cnt = self.cur.fetchone()
        return cnt[0] + 1
    
    def getLabels(self):
        sql = """
        
            SELECT * FROM (
            SELECT
                TO_NUMBER(REGEXP_REPLACE(TB_CAR.CAR_NO, 'CAR0*', '')) car_label,                
                TB_CAR.CAR_NO,

                TB_CSTMR.CST_GEN,
                CASE
                    WHEN (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 <= 24 THEN 20
                    WHEN (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 <= 29 AND (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 >= 25 THEN 25
                    WHEN (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 <= 39 AND (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 >= 30 THEN 30
                    WHEN (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 <= 49 AND (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 >= 40 THEN 40
                    WHEN (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 <= 59 AND (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 >= 50 THEN 50
                    WHEN (2000 - EXTRACT(YEAR FROM TB_CSTMR.CST_BIRTH) + TO_CHAR(SYSDATE, 'YY')) + 1 >= 60 THEN 60
                END AS CST_AGE
            FROM TB_CHKIN
            INNER JOIN TB_CAR ON (TB_CHKIN.CI_CAR_KIND = TB_CAR.CAR_NO)
            INNER JOIN TB_CSTMR ON (TB_CHKIN.CST_NO = TB_CSTMR.CST_NO) ) CAR
            GROUP BY CAR.CST_GEN, CAR.CST_AGE, CAR.CAR_NO, car_label
            ORDER BY CAR.CAR_NO
            
        """
        self.cur.execute(sql)
        car_list = self.cur.fetchall()
        myjson = []
        for c in car_list:
            myjson.append({'car_label':c[0], 'car_no':c[1]})
        return myjson
    
    def selectList(self):
        sql = """
            SELECT
                CAR_NO
                , CAR_NM
                , CAR_LIM
                , CAR_KIND
                , CAR_AGE
            FROM TB_CAR
        """
        self.cur.execute(sql)
        
        car_list = self.cur.fetchall()
        
        myjson = []
        for c in car_list:
            myjson.append({'car_no':c[0], 'car_nm':c[1], 'car_lim':c[2], 'car_kind':c[3], 'car_age':c[4]})
        return myjson
        
    def __del__(self):
        self.cur.close()
        self.conn.close()
        
if __name__ == '__main__':
    dc = DaoCar()
    print(dc.getCnt())
    print(dc.getLabels())
    print(dc.selectList())
