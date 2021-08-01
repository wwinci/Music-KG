from py2neo import Graph, Node, Relationship
from config import graph
cnt = 0
error_src = ['可惜我是水瓶座','Please Don\'t Go',"AS IF IT\'S YOUR LAST (마지막처럼)",
'你那么爱她 (《土地》电视剧片头曲|《前男友不是人》电视剧插曲)',"I\'M OK","Don\'t Tie Me Down",'와 (哇！)',
"We Don\'t Talk Anymore","We Can\'t Stop","Don\'t Let Me Down","Fantastic Baby","Friendships (Album Version)","至少还有你",
"Let\'s not fall in love (우리 사랑하지 말아요)"]
with open("rdf.txt",encoding='utf-8') as f:
    for line in f.readlines():
        rela_array=line.strip("\n").split(",")
        if len(rela_array)>5 or rela_array[0] in error_src:
            print("done")
            continue
        if rela_array[2]=="album":
            graph.run("MERGE(p: Song{cate:'%s',Name: '%s'})"%(rela_array[3],rela_array[0]))
            graph.run("MERGE(p: Album{cate:'%s',Name: '%s'})" % (rela_array[4], rela_array[1]))
            graph.run(
                "MATCH(e: Song), (cc: Album) \
                WHERE e.Name='%s' AND cc.Name='%s'\
                CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
                RETURN r" % (rela_array[0], rela_array[1], rela_array[2],rela_array[2])

            )
        elif rela_array[2]=='artist':
            graph.run("MERGE(p: Song{cate:'%s',Name: '%s'})"%(rela_array[3],rela_array[0]))
            graph.run("MERGE(p: Artist{cate:'%s',Name: '%s'})" % (rela_array[4], rela_array[1]))
            graph.run(
                "MATCH(e: Song), (cc: Artist) \
                WHERE e.Name='%s' AND cc.Name='%s'\
                CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
                RETURN r" % (rela_array[0], rela_array[1], rela_array[2],rela_array[2])

            )
        elif rela_array[2]=='company':
            graph.run("MERGE(p: Song{cate:'%s',Name: '%s'})"%(rela_array[3],rela_array[0]))
            graph.run("MERGE(p: Company{cate:'%s',Name: '%s'})" % (rela_array[4], rela_array[1]))
            graph.run(
                "MATCH(e: Song), (cc: Company) \
                WHERE e.Name='%s' AND cc.Name='%s'\
                CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
                RETURN r" % (rela_array[0], rela_array[1], rela_array[2],rela_array[2])

            )
        elif rela_array[2]=='lan':
            graph.run("MERGE(p: Song{cate:'%s',Name: '%s'})"%(rela_array[3],rela_array[0]))
            graph.run("MERGE(p: Language{cate:'%s',Name: '%s'})" % (rela_array[4], rela_array[1]))
            graph.run(
                "MATCH(e: Song), (cc: Language) \
                WHERE e.Name='%s' AND cc.Name='%s'\
                CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
                RETURN r" % (rela_array[0], rela_array[1], rela_array[2],rela_array[2])

            )
        elif rela_array[2]=='pub_time':
            graph.run("MERGE(p: Song{cate:'%s',Name: '%s'})"%(rela_array[3],rela_array[0]))
            graph.run("MERGE(p: Time{cate:'%s',Name: '%s'})" % (rela_array[4], rela_array[1]))
            graph.run(
                "MATCH(e: Song), (cc: Time) \
                WHERE e.Name='%s' AND cc.Name='%s'\
                CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
                RETURN r" % (rela_array[0], rela_array[1], rela_array[2],rela_array[2])

            )
        elif rela_array[2]=="genre":
            graph.run("MERGE(p: Song{cate:'%s',Name: '%s'})"%(rela_array[3],rela_array[0]))
            graph.run("MERGE(p: Genre{cate:'%s',Name: '%s'})" % (rela_array[4], rela_array[1]))
            graph.run(
                "MATCH(e: Song), (cc: Genre) \
                WHERE e.Name='%s' AND cc.Name='%s'\
                CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
                RETURN r" % (rela_array[0], rela_array[1], rela_array[2],rela_array[2])

            )
        
        cnt = cnt + 1 
    
    print(graph)
    print(cnt)    
