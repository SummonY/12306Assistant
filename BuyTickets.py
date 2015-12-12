#!/usr/bin/python
# -*- coding:utf-8 -*-


from optparse import OptionParser
from splinter.browser import Browser
from time import sleep
import traceback


login_url = 'https://kyfw.12306.cn/otn/login/init'
select_tickets_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
index_url = 'https://kyfw.12306.cn/otn/index/initMy12306'


def login(username='', password=''):
    b.find_by_text(u'登录').click()
    sleep(3)
    if username == '':
        print u'请输入用户名'
        return
    else:
        b.fill("loginUserDTO.user_name", username)
    sleep(1)
    b.fill("userDTO.password", password)
    sleep(1)
    print u'等待验证码，请手动输入验证码...'
    while True:
        if b.url != index_url:
            sleep(1)
        else:
            break


def OpenBrowser(username='', password='', start_pos=u'', end_pos=u'', \
                start_time=''):
    """Open Chorme Browser

    """
    global b
    b = Browser(driver_name="chrome")
    b.visit(select_tickets_url)

    while b.is_text_present(u"登录"):
        print u'尚未登录，正在登录...'
        sleep(1)
        login(username, password)
        if b.url == index_url:
            break

    try:
        print u'开始购票...'
        b.visit(select_tickets_url)

        b.cookies.add({u"_jc_save_fromStation" : start_pos})
        b.cookies.add({u"_jc_save_toStation" : end_pos})
        b.cookies.add({u"_jc_save_fromDate" : start_time})
        b.reload()

        sleep(2)

        count = 0
        while b.url == select_tickets_url:
            b.find_by_text(u"查询").click()
            count += 1
            sleep(1)
            try:
                for i in b.find_by_text(u"预定"):
                    i.click()
            except:
                continue
        sleep(1)
        #b.find_by_text()


    except Exception as e:
        print(traceback.print_exc())



def SetupCommandLineOptions():
    """Sets up command line parsing.

    Return:
        An optparse.OptionParser() object.
    """
    Usage = "Usage: ./BuyTickets.py -u username -p password "
    parser = OptionParser(Usage)
    parser.add_option('-u', '--user', dest='USER', help=u'用户名')
    parser.add_option('-p', '--password', dest='PASSWORD', help=u'密码')
    parser.add_option('-s', '--start', dest='START', help=u'出发地')
    parser.add_option('-e', '--end', dest='END', help=u'目的地')
    parser.add_option('-t', '--time', dest='TIME', help=u'出发时间')
    parser.add_option('-n', '--name', dest='NAME', help=u'购票人姓名')

    return parser

def ParseCommandLineArguments(parser):
    """Parses command line arguments and handlers error checking.

    Args:
        parser: An optparse.OptionParser() object initialized with options.

    Returns:
        The resutl of OptionParser.parse after it has been checked for errors.
    """
    opts, args = parser.parse_args()

    if args:
        parser.error('unexpected positional arguments "%s"' % ' '.join(args))
    if not opts.USER and not opts.PASSWORD:
        parser.error("-u requires a value and -p requires a value.")
    return opts

def main():
    parser = SetupCommandLineOptions()
    opts = ParseCommandLineArguments(parser)

    username = ''
    password = ''
    start_pos = ''
    end_pos = ''
    start_time = ''

    if opts.USER:
        username = opts.USER
        print '用户名: ', username
    if opts.PASSWORD:
        password = opts.PASSWORD
        print '密码: ', password
    if opts.START:
        start_pos = opts.START
        print '出发地: ', start_pos
    if opts.END:
        end_pos = opts.END
        print '目的地: ', end_pos
    if opts.TIME:
        start_time = opts.TIME
        print '出发时间: ', start_time

    OpenBrowser(username, password, unicode(start_pos, 'utf-8'), \
                unicode(end_pos, 'utf-8'), start_time)


if __name__ == '__main__':
    main()
