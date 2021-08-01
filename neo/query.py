from config import graph
from str2list import str2list


def QA(str):
    output = []
    flag,s = str2list(str)
    #print(flag,s)
    length = len(s)
    if length == 1:
        p = s[0]
        if flag == 0:
            data = list(graph.run("Match (p:Song {Name:'%s'})-[r:artist]-(g:Artist) return g.Name" % (p)))
            output.append(data)
            data = list(graph.run("Match (p:Song {Name:'%s'})-[r:album]-(g:Album) return g.Name" % (p)))
            output.append(data)
            data = list(graph.run("Match (p:Song {Name:'%s'})-[r:genre]-(g:Genre) return g.Name" % (p)))
            output.append(data)
            data = list(graph.run("Match (p:Song {Name:'%s'})-[r:lan]-(g:Language) return g.Name" % (p)))
            output.append(data)
            data = list(graph.run("Match (p:Song {Name:'%s'})-[r:pub_time]-(g:Time) return g.Name" % (p)))
            output.append(data)
            data = list(graph.run("Match (p:Song {Name:'%s'})-[r:company]-(g:Company) return g.Name" % (p)))
            output.append(data)
        elif flag == 1:
            data = list(graph.run("Match (p:Artist {Name:'%s'})-[r:artist]-(g:Song) return g.Name" % (p)))
            output.append(data)
        elif flag == 2:
            data = list(graph.run("Match (p:Genre {Name:'%s'})-[r:genre]-(g:Song) return g.Name" % (p)))
            output.append(data)
        elif flag == 3:
            data = list(graph.run("Match (p:Language {Name:'%s'})-[r:lan]-(g:Song) return g.Name" % (p)))
            output.append(data)
        elif flag == 4:
            data = list(graph.run("Match (p:Time {Name:'%s'})-[r:pub_time]-(g:Song) return g.Name" % (p)))
            output.append(data)
        elif flag == 5:
            data = list(graph.run("Match (p:Company {Name:'%s'})-[r:company]-(g:Song) return g.Name" % (p)))
            output.append(data)
        elif flag == 6:
            data = list(graph.run("Match (p:Album {Name:'%s'})-[r:album]-(g:Song) return g.Name" % (p)))
            output.append(data)

    elif length == 2:
        p = s[0]
        q = s[1]
        if flag == 0:
            if q == '歌手':
                data = list(graph.run("Match (p:Song {Name:'%s'})-[r:artist]-(g:Artist) return g.Name" % (p)))
                output.append(data)
            elif q == '信息':
                data = list(graph.run("Match (p:Song {Name:'%s'})-[r:artist]-(g:Artist) return g.Name" % (p)))
                output.append(data)
                data = list(graph.run("Match (p:Song {Name:'%s'})-[r:album]-(g:Album) return g.Name" % (p)))
                output.append(data)
                data = list(graph.run("Match (p:Song {Name:'%s'})-[r:genre]-(g:Genre) return g.Name" % (p)))
                output.append(data)
                data = list(graph.run("Match (p:Song {Name:'%s'})-[r:lan]-(g:Language) return g.Name" % (p)))
                output.append(data)
                data = list(graph.run("Match (p:Song {Name:'%s'})-[r:pub_time]-(g:Time) return g.Name" % (p)))
                output.append(data)
                data = list(graph.run("Match (p:Song {Name:'%s'})-[r:company]-(g:Company) return g.Name" % (p)))
                output.append(data)
            elif q == '专辑':
                data = list(graph.run("Match (p:Song {Name:'%s'})-[r:album]-(g:Album) return g.Name" % (p)))
                output.append(data)
            elif q == '时间':
                data = list(graph.run("Match (p:Song {Name:'%s'})-[r:pub_time]-(g:Time) return g.Name" % (p)))
                output.append(data)
            elif q == '流派':
                data = list(graph.run("Match (p:Song {Name:'%s'})-[r:genre]-(g:Genre) return g.Name" % (p)))
                output.append(data)
            elif q == '公司':
                data = list(graph.run("Match (p:Song {Name:'%s'})-[r:company]-(g:Company) return g.Name" % (p)))
                output.append(data)
            elif q == '推荐':
                data = list(graph.run("Match (p:Song {Name:'%s'})-[t:genre]-(r:Genre)-[s:genre]-(g:Song) return g.Name LIMIT 10" % (p)))
                output.append(data)
                data = list(graph.run( "Match (p:Song {Name:'%s'})-[t:artist]-(r:Artist)-[s:artist]-(g:Song) return g.Name LIMIT 10" % (p)))
                output.append(data)
            elif q == '语言':
                data = list(graph.run("Match (p:Song {Name:'%s'})-[r:lan]-(g:Language) return g.Name" % (p)))
                output.append(data)

        elif flag == 1:
            if q == '歌曲':
                data = list(graph.run("Match (p:Artist {Name:'%s'})-[r:artist]-(g:Song) return g.Name" % (p)))
                output.append(data)
            elif q == '推荐':
                data = list(graph.run("Match (p:Artist {Name:'%s'})-[d:artist]-(r:Song)-[s:genre]-(t:Genre)-[a:genre]-(b:Song)-[c:artist]-(g:Artist) return g.Name LIMIT 100" % (p)))
                output.append(data)
            elif q == '专辑':
                data = list(graph.run("Match (p:Artist {Name:'%s'})-[r:artist]-(b:Song)-[a:album]-(g:Album) return .Name" % (p)))
                output.append(data)
        elif flag == 6:
            if q == '歌手':
                data = list(graph.run("Match (p:Album{Name:'%s'})-[r:album]-(g:Song)-[h:artist]-(k:Artist) return k LIMIT 1" % (p)))
                output.append(data)
        elif flag == 2:
            if q == '歌曲':
                data = list(graph.run("Match (p:Genre{Name:'%s'})-[r:genre]-(g:Song) return g.Name" % (p)))
                output.append(data)
        elif flag == 3:
            if q == '歌曲':
                data = list(graph.run("Match (p:Language{Name:'%s'})-[r:lan]-(g:Song) return g.Name" % (p)))
                output.append(data)
        elif flag == 4:
            if q == '歌曲':
                data = list(graph.run("Match (p:Time{Name:'%s'})-[r:pub_time]-(g:Song) return g.Name" % (p)))
                output.append(data)
    elif length == 3:
        p = s[0]
        q = s[1]
        r = s[2]
        if flag == 0:
            if q == '时间' and r == '歌曲':
                data = list(graph.run("Match (p:Song{Name:'%s'})-[r:pub_time]-(l:Time)-[h:pub_time]-(g:Song) return g.Name" % (p)))
                output.append(data)

        if flag == 13:
            if r == '歌曲':
                data1 = list(graph.run("Match (p:Artist{Name:'%s'})-[r:artist]-(g:Song) return g.Name" % (p)))
                data2 = list(graph.run("Match (p:Language{Name:'%s'})-[r:lan]-(g:Song) return g.Name" % (q)))
                data=[]
                for item in data1:
                    if item in data2:
                        data.append(item)
                output.append(data)
    return output

while True:
    str = input('please input a question:')
    s=QA(str)
    k=s[0]
    anwser=[]
    for j in k:
        l=j['g.Name']
        if l not in anwser:
            anwser.append(l)
    for i in anwser:
        print(i)