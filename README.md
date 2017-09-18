## ContractReminder
send email to user when the contract they added expires.

#中文说明：
##合同到期提醒系统
可以进行合同信息录入、查询，包含标题、摘要、备注、开始/结束/提醒日期。
通过Windows系统计划任务执行独立的mail_sync.py，
每日定时遍历数据库，将提醒日期为当日的合同及对应的用户取出，并向他们发送提醒邮件。
