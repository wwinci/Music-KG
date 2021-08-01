import json
files=['26_2020_1_300.json','26_2019_1_300.json','26_2018_10_300.json']

def load(file_name):
    with open(file_name,'r',encoding='utf-8') as f:
        data = json.load(f)
        return data
relation = []
song_set = set()
for file_name in files:
    data_dic_list = load(file_name)
    for data_dic in data_dic_list:
        songname = data_dic['songname']
        if songname in song_set:
            print("done")
        else:
            song_set.add(songname)
            del data_dic['songname']
            del data_dic['artistid']
            del data_dic["songid"]
            source = 'Song'
            
            for item in data_dic.items():
                target = item[0].title()
                if item[0]=='artist':
                    for artist in item[1]:
                        relation.append((songname,artist,item[0],"Song","Artist"))
                elif item[0]=='album':
                    for album in item[1]:
                        relation.append((songname,album+"专辑",item[0],"Song","Album"))
                else :
                    relation.append((songname,item[1],item[0],source,target))
f = open("rdf.txt", 'w',encoding='utf-8')
for t in relation:
    line = ','.join(str(x) for x in t)   
    f.write(line + '\n')
f.close()