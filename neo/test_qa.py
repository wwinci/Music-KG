from config import graph
name = '泡沫'
def get_KGQA_answer():
    data = graph.run("Match (p:Song {Name:'%s'})-[r:genre]-(g:Genre) return p,r,g"%(name))
    print(list(data))   
    return 

get_KGQA_answer()

# 查询歌曲流派