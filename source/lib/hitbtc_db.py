#!/usr/bin/python
#coding: utf-8
#hitbtc_db.py => class HITBTCDB
import MySQLdb

class HITBTCDB(object):
    def __init__(self):
        self.db_host     = 'localhost'
        self.db_port     = 3306
        self.db_user     = 'yama'
        self.db_pass     = 'sYr6nukU'
        self.db_name     = 'altcoins'
        self.open_conn()

    def open_conn(self):
        """Get symbol."""
        self.conn = MySQLdb.connect(
          host   = self.db_host,
          port   = self.db_port,
          user   = self.db_user,
          passwd = self.db_pass,
          db     = self.db_name,
        )
        self.cursor = self.conn.cursor()

    def regist_dict(self,data_dict):
        for data_row in data_dict :
            # 現在存在するかどうかチェック
            current_sql  = ' SELECT instrument,quantity,price,volume,fee,rebate,total FROM t_trades'
            current_sql += ' WHERE id=%s '
            placehold = (
                data_row['id'],
            )
            self.cursor.execute(current_sql,placehold)
            data_one = self.cursor.fetchall()
            print len(data_one)
            print('data row : "%s"' % data_row)
            if len(data_one) == 0:
                placehold = (
                    data_row['timestamp'].translate(
                    {ord(u'T'): u' ',ord(u'Z'): u' ',}
                    ),data_row['symbol'],data_row['id'],
                    data_row['orderId'],data_row['side'],data_row['quantity'],data_row['price'],
                    data_row['fee'],
                )
                current_sql  = ' INSERT INTO t_trades '
                current_sql += ' (exec_date,instrument,id'
                current_sql += ' ,order_id,side,quantity,price'
                # current_sql += ' ,volume,fee,rebate,total,uptime)'
                current_sql += ' ,fee,uptime)'
                # current_sql += ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())'
                current_sql += ' VALUES (CONVERT_TZ(%s,"+00:00","+09:00"),%s,%s'
                current_sql += ',%s,%s,%s,%s,%s,now())'
                self.cursor.execute(current_sql,placehold)
                result = self.cursor.fetchall()
                # print('xINSERT OK : "%s"' % result)
                print('this INSERT OK %d' , data_row['id'])
            else :
                placehold = (
                    data_row['timestamp'].translate(
                    {ord(u'T'): u' ',ord(u'Z'): u' ',}
                    ),data_row['symbol'],
                    data_row['orderId'],data_row['side'],data_row['quantity'],data_row['price'],
                    data_row['fee'],
                    data_row['id'],
                )
                current_sql  = ' UPDATE t_trades SET '
                current_sql += ' exec_date = CONVERT_TZ(%s,"+00:00","+09:00"),instrument=%s'
                current_sql += ' ,order_id=%s,side=%s,quantity=%s,price=%s'
                # current_sql += ' ,volume=%s,fee=%s,rebate=%s,total=%s,uptime=now()'
                current_sql += ' ,fee=%s,uptime=now()'
                current_sql += ' WHERE id=%s '
                self.cursor.execute(current_sql,placehold)
                result = self.cursor.fetchall()
                # print('sUPDATE OK : "%s"' % result)
                print('this UPDATE OK %d' , data_row['id'])
        print('finish and commit ')
        self.conn.commit()

    def regist_balance_now_dict(self,account_data_dict,trading_data_dict):
        for data_row in account_data_dict :
            if float(data_row['available']) > 0 :
                print('account balance: "%s"' % data_row)
        for data_row in trading_data_dict :
            if float(data_row['available']) > 0 :
                print('trading balance: "%s"' % data_row)

    def calculate_current_price(self,instrument):
        #一つの銘柄の現在価格を計算
        current_sql  = ' SELECT price,quantity FROM t_trades '
        current_sql += ' WHERE uptime > (now() - INTERVAL 3 month) AND  instrument like "%s%%" '
        placehold = (
            instrument,
        )
        print current_sql
        self.cursor.execute(current_sql,placehold)
        data_one = self.cursor.fetchall()

    def regist_transactions_dict(self,data_dict):
        for data_row in data_dict :
            # 現在存在するかどうかチェック
            current_sql  = ' SELECT t_hash FROM payment_history '
            current_sql += ' WHERE operation_id_1=%s AND operation_id_2=%s AND operation_id_3=%s '
            current_sql += ' AND operation_id_4=%s AND operation_id_5=%s ;'
            placehold = (
                  data_row['id'].split("-")[0], data_row['id'].split("-")[1], data_row['id'].split("-")[2],
                  data_row['id'].split("-")[3], data_row['id'].split("-")[4],
            )
            self.cursor.execute(current_sql,placehold)
            data_one = self.cursor.fetchall()
            print len(data_one)
            print('transactions balance: "%s"' % data_row)
            if len(data_one) == 0:
                current_sql  = ' INSERT INTO payment_history '
                current_sql += ' (exec_date,operation_id_1,operation_id_2,operation_id_3'
                current_sql += ' ,operation_id_4,operation_id_5,type,amount'
                if 'hash' not in data_row :
                    # hashのkeyはないことがある
                    current_sql += ' ,currency,uptime)'
                    current_sql += ' VALUES (CONVERT_TZ(%s,"+00:00","+09:00"),'
                    current_sql += '%s,%s,%s,'
                    current_sql += '%s,%s,%s,%s,'
                    current_sql += '%s,now());'
                    placehold = (
                      data_row['updatedAt'].translate(
                      {ord(u'T'): u' ',ord(u'Z'): u' ',}
                      ),
                      data_row['id'].split("-")[0], data_row['id'].split("-")[1], data_row['id'].split("-")[2],
                      data_row['id'].split("-")[3], data_row['id'].split("-")[4], data_row['type'], data_row['amount'],
                      data_row['currency'],
                    )
                    self.cursor.execute(current_sql,placehold)
                else :
                    current_sql += ' ,t_hash,currency,uptime)'
                    current_sql += ' VALUES (CONVERT_TZ(%s,"+00:00","+09:00"),%s,%s,%s,%s,%s,%s,%s,%s,%s,now());'
                    placehold = (
                      data_row['updatedAt'].translate(
                      {ord(u'T'): u' ',ord(u'Z'): u' ',}
                      ), data_row['id'].split("-")[0], data_row['id'].split("-")[1], data_row['id'].split("-")[2],
                      data_row['id'].split("-")[3], data_row['id'].split("-")[4], data_row['type'], data_row['amount'],
                      data_row['hash'], data_row['currency'],
                    )
                    self.cursor.execute(current_sql,placehold)
                print 'INSERT OK'
            else :
                current_sql  = ' UPDATE payment_history SET '
                current_sql += ' exec_date = CONVERT_TZ(%s,"+00:00","+09:00") '
                current_sql += ' ,type=%s,amount=%s'
                if 'hash' not in data_row :
                    # hashのkeyはないことがある
                    current_sql += ' ,currency=%s,uptime=now() '
                    current_sql += ' WHERE operation_id_1=%s AND operation_id_2=%s AND operation_id_3=%s '
                    current_sql += ' AND operation_id_4=%s AND operation_id_5=%s ;'
                    placehold = (
                      data_row['updatedAt'].translate(
                      {ord(u'T'): u' ',ord(u'Z'): u' ',}
                      ),
                      data_row['type'],data_row['amount'],
                      data_row['currency'],
                      data_row['id'].split("-")[0], data_row['id'].split("-")[1], data_row['id'].split("-")[2],
                      data_row['id'].split("-")[3], data_row['id'].split("-")[4]
                    )
                else:
                    current_sql += ' ,t_hash=%s,currency=%s,uptime=now() '
                    current_sql += ' WHERE operation_id_1=%s AND operation_id_2=%s AND operation_id_3=%s '
                    current_sql += ' AND operation_id_4=%s AND operation_id_5=%s ;'
                    placehold = (
                      data_row['updatedAt'].translate(
                      {ord(u'T'): u' ',ord(u'Z'): u' ',}
                      ),
                      data_row['type'],data_row['amount'],
                      data_row['hash'],data_row['currency'],
                      data_row['id'].split("-")[0], data_row['id'].split("-")[1], data_row['id'].split("-")[2],
                      data_row['id'].split("-")[3], data_row['id'].split("-")[4]
                    )

                self.cursor.execute(current_sql,placehold)
                print 'UPDATE OK'
            self.conn.commit()
