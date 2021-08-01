from config import graph
import jieba
need_word = ['歌曲','流派','公司','时间','语言','专辑','推荐']
num_list = []
ten_list=[]
for i in range(1,2021):
    if i < 10:
        ten_list.append(str(i))
    num_list.append(str(i))

def str2list(str):
    c_list = []
    word = []
    flag = 0
    if '《' in str:
        loc = str.index('《')
        flag = 0
        for i in range(loc+1, len(str)):
            if str[i] != '》':
                word.append(str[i])
            else:
                break
        word = ''.join(word)
        c_list.append(word)
        data1 = list(graph.run("MATCH (r:Song{Name: '%s'}) return r" % (word)))
        data2 = list(graph.run("MATCH (r:Company{Name: '%s'}) return r" % (word)))
        data3 = list(graph.run("MATCH (r:Album{Name: '%s'}) return r" % (word)))
        if data1 != []:
            flag = 0
        elif data2 != []:
            flag = 5
        elif data3 != []:
            flag =6
        for j in range(i + 1, len(str)):
            if len(c_list)==2 and str[j] == '歌':
                if c_list[1] == '时间':
                    c_list.append('歌曲')
            elif str[j] == '歌':
                if j+1<len(str) and str[j + 1] == '手':
                    c_list.append('歌手')
            elif str[j] == '信':
                c_list.append('信息')
            elif str[j] == '流' or str[j] == '风':
                c_list.append('流派')
            elif str[j] == '时':
                c_list.append('时间')
            elif str[j] == '公':
                c_list.append('公司')
            elif str[j] == '语':
                c_list.append('语言')
            elif str[j] == '专':
                c_list.append('专辑')
            elif str[j] == '推':
                c_list.append('推荐')

        return flag,c_list
    else:
        f = 1
        time = []
        flag = []
        c_list = list(jieba.cut(str))
        d_list = []
        for i in range(len(c_list)):
            p = c_list[i]
            data1 = list(graph.run("MATCH (r:Artist{Name: '%s'}) return r" % (p)))
            data2 = list(graph.run("MATCH (r:Genre{Name: '%s'}) return r" % (p)))
            data3 = list(graph.run("MATCH (r:Language{Name: '%s'}) return r" % (p)))
            if data1 != []:
                flag.append('1')
                d_list.append(p)
            elif data2 != []:
                flag.append('2')
                d_list.append(p)
            elif data3 != []:
                flag.append('3')
                d_list.append(p)
            elif p == '歌':
                d_list.append('歌曲')
            elif p == '风格':
                d_list.append('流派')
            elif p == '日期':
                d_list.append('时间')
            elif p in need_word:
                d_list.append(p)
            elif p in num_list and f == 1:
                f = 0
                time.append(p)
                if c_list[i+2] in ten_list:
                    time.append(('0'+c_list[i+2]))
                else:
                    time.append(c_list[i+2])
                if c_list[i+4] in ten_list:
                    time.append(('0'+c_list[i+4]))
                else:
                    time.append((c_list[i+4]))
                pub_time = '-'.join(time)
                d_list.append(pub_time)
                flag.append('4')

        flag = ''.join(flag)
        flag = int(flag)
        return flag,d_list

#str = input('please input a question:')
#flag,s = str2list(str)
#print(s,flag)

