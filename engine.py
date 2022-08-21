import pymysql
from datetime import datetime

con = None
cur = None

USER = 'root'
PASSWORD = 'pass'
DBNAME = 'document'


def connect():
    global con, cur, USER, PASSWORD, DBNAME
    print('连接数据库中。。。')
    try:
        con = pymysql.connect(host='localhost', user=USER, password=PASSWORD, database=DBNAME)
        cur = con.cursor()
        print('连接数据库成功！')
        return True
    except:
        print('数据库连接失败！')
        return False


def disconnect():
    global con, cur
    cur.close()
    con.close()

uname = ''

def login(name, password):
    global con, cur
    cur.execute('select * from user where name="%s" and password="%s"' % (name, password))
    users = cur.fetchall()
    if len(users) is not 1:
        return False
    return True


def add_document(name, time, typ, position, content):
    global con, cur
    if typ is '0':
        cur.execute("insert into document(name, time, type, position) values('%s', '%s', '%s', '%s')" % (name, time, typ, position))
    else:
        cur.execute("insert into document(name, time, type, content) values('%s', '%s', '%s', '%s')" % (name, time, typ, content))
    con.commit()

def add_document_mode():
    print('')
    name = input('请输入文档名:')
    time = input('请输入登记时间(格式：2022-07-01 10:05:23, 直接回车设置为当前时间): ')
    typ = input('请输入文档类型(0为纸质文档，其他为电子文档): ')
    try:
        if not time:
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if typ is '0':
            position = input('请输入仓库中的位置: ')
            add_document(name, time, typ, position, '')
        else:
            content = input('请输入文档内容: ')
            add_document(name, time, typ, '', content)   
    except:
        print('文档登记失败！')

def display_documents(documents):
    print('{0:<25}{1:<25}{2:<25}{3:<25}{4:<25}'.format('ID', 'Name', 'Time', 'Type', 'Position'))
    print('-----------------------------------------------------------------------------------------------------------------------')
    for document in documents:
        print('{0:<25}{1:<25}{2:<25}{3:<25}{4:<25}'.format(
            document[0],
            document[1],
            document[2].strftime('%Y-%m-%d %H:%M:%S'),
            'paper' if document[3] is 0 else 'electric',
            document[4] if document[4] else '---'
        ))
    if len(documents) is 0:
        print('{0:>55}'.format('无数据'))
    print('')

def show_content(id):
    global cur, con
    cur.execute('select content from document where id="%s"' % id)
    res = cur.fetchall()
    if len(res) is not 1:
        return False
    print('内容为:')
    print(res[0][0])

def search_document_mode():
    global con, cur
    print('')
    print('1. 按文件名查询')
    print('2. 按登记时间查询')
    print('3. 显示全部')
    print('4. 显示电子文档内容')
    print('其他键. 回主菜单')
    mode = input('请输入操作号: ')
    documents = []
    if mode is '1':
        name = input('请输入文档名: ')
        cur.execute('select id, name, time, type, position, content from document where name like "%{0}%"'.format(name))
        documents = cur.fetchall()
    elif mode is '2':
        time = input('请输入登记日期(格式：2022-01-10): ')
        cur.execute('select id, name, time, type, position, content from document where date(time)="%s"' % time)
        documents = cur.fetchall()
    elif mode is '3':
        cur.execute('select id, name, time, type, position, content from document')
        documents = cur.fetchall()
    elif mode is '4':
        id = input('请输入文档ID(如果不清楚先查ID): ')
        if not show_content(id):
            print('找不到文档！')
    else:
        return
    display_documents(documents)
    if len(documents) is 1 and documents[0][3] is not 0:
        op = input('是否查看当前电子文档内容?(y/n): ')
        if op is 'Y' or op is 'y':
            show_content(documents[0][0])

def change_password():
    global cur, con, uname
    password = input('请输入密码: ')
    cur.execute('select id from user where name="%s" and password="%s"' % (uname, password))
    res = cur.fetchall()
    if len(res) is not 1:
        print('密码错误！')
        return
    password = input('请输入新的密码: ')
    cur.execute('update user set password="%s" where id="%s"' % (password, res[0][0]))
    con.commit()
    print('修改成功！')

def main():
    if not connect():
        return

    global uname
    
    print('-----------------------------')
    print('|       文档管理系统        |')
    print('-----------------------------')
    logged = False
    while not logged:
        name = input('请输入用户名: ')
        password = input('请输入密码: ')
        if login(name, password):
            uname = name
            logged = True
        else:
            mode = input('用户名或密码错误，是否要重试?(y/n) ');
            if mode is not 'y' and mode is not 'Y':
                break

    if not logged:
        disconnect()
        return

    print('\n%s, 您好！欢迎进入本系统。' % uname)

    while True:
        print('')
        print('1. 修改用户密码')
        print('2. 文档登记')
        print('3. 文档查询')
        print('其他键. 退出')
        mode = input('请输入操作号:')
        if mode is '1':
            change_password()
        elif mode is '2':
            add_document_mode()
        elif mode is '3':
            search_document_mode()
        else:
            break

    disconnect()


if __name__ == '__main__':
    main()
