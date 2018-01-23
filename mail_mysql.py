import os
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from datetime import datetime, timedelta
from key_info import Mail, Database
from log import logging
import pymysql


def get_infos(sql, *args):
    """
    连接数据库
    SQLite 弃用
    conn = sqlite3.connect('data-product.sqlite')
    MsSQL 弃用
    conn=pymssql.connect(host=hostname,user=username,
    password=pwd,database=databasename)
    MySQL 当前
    返回[{},...]形式的查询结果
    """
    conn = pymysql.connect(host=Database.host,
        user=Database.user,
        password=Database.password,
        db=Database.db,
        charset=Database.charset,
        cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        cursor.execute(sql, args)
        res = cursor.fetchall()
    finally:
        conn.close()
    return res

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send_mail(res):
    from_addr = Mail.from_addr
    password = Mail.password
    smtp_server = Mail.smtp_server
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    for r in res:
        to_addr = [r.get('email', None)]
        to_addr2 = r.get('email2', None)
        if to_addr is None:
            continue
        # 排除抄送邮箱为空,或主副邮箱相同的情况
        if to_addr2 is not None and to_addr != [to_addr2]:
            to_addr.append(to_addr2)
        end_date = r.get('end_date', None)
        if end_date is not None:
            end_date = datetime.strftime(end_date, '%Y-%m-%d')
        title = r.get('title', '')
        note = r.get('note', '')
        summary = r.get('summary', '')
        content = '''
            合同即将到期提醒：
            标题：{}
            到期日期：{}
            摘要：{}
            备注：{}
            合同提醒系统
            友情提示：请勿直接回复本邮件。
            '''.format(title, end_date, summary, note)
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = _format_addr(from_addr)
        msg['Subject'] = Header('合同即将到期提醒', 'utf-8').encode()
        msg['To'] = _format_addr(to_addr)
        server.sendmail(from_addr, to_addr, msg.as_string())
        succ = '正在发送邮件给 {}.'.format(str(to_addr))
        logging(succ)
    server.quit()


def main():
    today = datetime.today()
    date0 = datetime.strftime(today, '%Y-%m-%d')
    date60 = datetime.strftime(today + timedelta(days=60), '%Y-%m-%d')
    date90 = datetime.strftime(today + timedelta(days=90), '%Y-%m-%d')

    #根据提醒日期获取合同信息：
    sql_remind = '''select users.id, users.email, posts.id, posts.title, posts.summary,
             posts.note, posts.end_date, users.email2
             from users, posts where posts.author_id = users.id and
             posts.remind_date = %s '''

    #根据结束日期获取合同信息：
    sql_end = '''select users.id, users.email, posts.id, posts.title, posts.summary,
             posts.note, posts.end_date, users.email2
             from users, posts where posts.author_id = users.id and
             posts.end_date = %s'''

    res = get_infos(sql_remind, date0)
    # res.extend(get_infos(sql_end, date60))
    # res.extend(get_infos(sql_end, date90))
    if res is not None:
        logging('开始发送邮件', res)
        send_mail(res)
        logging('邮件发送完毕')


if __name__ == '__main__':
    main()