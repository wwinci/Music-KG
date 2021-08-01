files=['26_2020_1_300.json','26_2019_1_300.json','26_2018_10_300.json']
import json
def merge_JsonFiles(filename):
    result = list()
    for f1 in filename:
        with open(f1, 'rb') as infile:
            result.extend(json.load(infile))

    with open('songs.json', 'w') as output_file:
        json.dump(result, output_file)

merge_JsonFiles(files)