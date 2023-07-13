import datetime
import csv
import codecs
import logging
import tempfile
import smtplib
from django.conf import settings
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from meetings.models import User, ActivitySign
from .email_templates import applicants_info_template

logger = logging.getLogger('log')


def run(queryset, mailto):
    tmpdir = tempfile.gettempdir()
    target_name = tmpdir + '活动报名表单.csv'
    f = codecs.open(target_name, 'w')
    writer = csv.writer(f)
    writer.writerow(['姓名', '微信号', '性别', '年龄', '电话', '邮箱', '所在公司/就读学校', '职业方向', '职业名称', '工作年限',
                     'giteeID', '签到'])
    for applicant_info in queryset:
        user_id = applicant_info.user_id
        user = User.objects.get(id=user_id)
        name = user.name
        wx_account = user.wx_account
        gender = user.gender
        age = user.age
        telephone = user.telephone
        email = user.email
        company = user.company
        career_direction = user.career_direction
        profession = user.profession
        working_years = user.working_years
        gitee_name = user.gitee_name
        activity_id = applicant_info.activity_id
        if gender == 1:
            gender = '男'
        elif gender == 2:
            gender = '女'
        else:
            gender = '未知'
        if user_id in ActivitySign.objects.filter(activity_id=activity_id).values_list('user_id'):
            is_sign = '是'
        else:
            is_sign = '否'
        writer.writerow([name, wx_account, gender, age, telephone, email, company, career_direction, profession,
                         working_years, gitee_name, is_sign])
    f.close()
    send_csv(target_name, mailto)


def send_csv(csv_file, mailto):
    msg = MIMEMultipart()
    body_of_email = applicants_info_template()
    content = MIMEText(body_of_email, 'html', 'utf-8')
    msg.attach(content)

    # 添加邮件附件
    file_path = csv_file
    enclosure = MIMEApplication(open(file_path, 'rb').read())
    enclosure.add_header('Content-Disposition', 'attachment',
                         filename='活动报名表单' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.csv')
    msg.attach(enclosure)

    # 完善邮件信息
    msg['Subject'] = '活动报名表单'
    msg['From'] = 'Mindspore MiniProgram<public@mindspore.cn>'
    msg['To'] = mailto

    # 登录服务器发送邮件
    try:
        gmail_username = settings.GMAIL_USERNAME
        gmail_password = settings.GMAIL_PASSWORD
        sender = 'public@mindspore.cn'
        server = smtplib.SMTP(settings.SMTP_SERVER_HOST, settings.SMTP_SERVER_PORT)
        server.ehlo()
        server.starttls()
        server.login(gmail_username, gmail_password)
        server.sendmail(gmail_username, [mailto], msg.as_string())
        print('发送成功')
        server.quit()
    except smtplib.SMTPException as e:
        logger.error(e)