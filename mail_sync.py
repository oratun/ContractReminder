from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import sqlite3
from datetime import datetime, timedelta
#key_info.py的mail类中定义了邮箱信息
from key_info import mail
# import pymssql

#log功能暂未生效
# import logging
# logging.basicConfig(filename='history.log',level=logging.info)
# conn.close()
def get_infos(sql, val):
    conn = sqlite3.connect('data-dev.sqlite')
    cursor = conn.cursor()
    # conn=pymssql.connect(host=hostname,user=username,
    #     password=pwd,database=databasename)
    # cur=conn.cursor()
    try:
        res = cursor.execute(sql, (val,)).fetchall()
    finally:
        conn.close()
    return res

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send_mail(res):
    from_addr = mail.from_addr
    password = mail.password
    smtp_server = mail.smtp_server
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    for i in res:
        to_addr = [i[1]]
        if i[7]:
            to_addr = [i[1], i[7]]
        to_addr = list(set(to_addr))
        content = '''
    合同即将到期提醒：
    标题：{}
    到期日期：{}
    摘要：{}
    备注：{}
    合同提醒系统
    友情提示：请勿直接回复本邮件。
    '''.format(i[3], i[6], i[4], i[5])
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = _format_addr(from_addr)
        msg['Subject'] = Header('合同即将到期提醒', 'utf-8').encode()
        msg['To'] = _format_addr(to_addr)
        server.sendmail(from_addr, to_addr, msg.as_string())
        # succ = 'a mail has been send to ' + to_addr
        # logging.info(succ)
    server.quit()

today = datetime.today()
date0 = datetime.strftime(today, '%Y-%m-%d')
date30 = datetime.strftime(today + timedelta(days=30), '%Y-%m-%d')
date90 = datetime.strftime(today + timedelta(days=90), '%Y-%m-%d')

#根据提醒日期获取合同信息：
sql_remind = '''select users.id, users.email, posts.id, posts.title, posts.summary,
         posts.note, posts.end_date, users.email2
         from users, posts where posts.author_id = users.id and
         posts.remind_date = ?'''

#根据结束日期获取合同信息：
sql_end = '''select users.id, users.email, posts.id, posts.title, posts.summary,
         posts.note, posts.end_date, users.email2
         from users, posts where posts.author_id = users.id and
         posts.end_date = ?'''

res = get_infos(sql_remind, date0)
res.extend(get_infos(sql_end, date30))
res.extend(get_infos(sql_end, date90))

if res is not None:
    send_mail(res)
