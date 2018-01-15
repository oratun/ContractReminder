from datetime import datetime
import os


def logging(*args):
    '''
    保存日志到文件中
    '''
    folder = 'log'
    if not os.path.exists(folder):
        os.mkdir(folder)
    today = datetime.today()
    date = datetime.strftime(datetime.today(), '%Y-%m-%d')
    value = datetime.strftime(datetime.today(), '%H:%M:%S')
    # 使用当天的日期作为日志文件名 2018-01-08
    filename = '{}.txt'.format(date)
    path = os.path.join(folder, filename)
    with open(path, 'w', encoding='utf-8') as f:
        print(value, *args, file=f)


def test(res):
    logging('正在发送邮件', res)
    # logging('邮件发送成功')


if __name__ == '__main__':
    test([1,2,3,4])