import requests
import json
from os import listdir
from hyper.contrib import HTTP20Adapter
from lxml import etree
from selenium.webdriver import Edge
from time import sleep

def elms(drv, xp, attr):

	lis = []
	flis = drv.find_elements_by_xpath(xp)
	for i in flis:
		lis.append(i.get_attribute(attr))
	return lis

def song_sp(drv, sid):
	
	try:
		drv.get('https://y.qq.com/n/yqq/song/'+sid+'.html')
		info = {}
		info['songname'] = elms(drv, '/html/body/div[2]/div[1]/div/div[1]/h1', 'title')[0]
		info['songid'] = sid
		info['album'] = elms(drv, '/html/body/div[2]/div[1]/div/ul/li[1]/a', 'title')
		info['artist'] = elms(drv, '/html/body/div[2]/div[1]/div/div[2]/a', 'title')
		info['artistid'] = elms(drv, '/html/body/div[2]/div[1]/div/div[2]/a', 'data-mid')
		info['rela_hot'] = elms(drv, '/html/body/div[2]/div[2]/div[2]/div[2]/div/ul/li', 'data-disstid')
	except:
		return {}, True
	
	st = etree.HTML(drv.page_source).xpath('/html/body/script[@type="text/javascript"][2]/text()')[0]
	for j in range(9):
		st = st[st.find('\n')+1:]
	st = st[10:st.find('\n')]
	jst = json.loads(st)
	if 'company' in jst.keys():
		info['company'] = jst['company']['content'][0]['value']
	if 'genre' in jst.keys():
		info['genre'] = jst['genre']['content'][0]['value']
	info['lan'] = jst['lan']['content'][0]['value']
	if 'pub_time' in jst.keys():
		info['pub_time'] = jst['pub_time']['content'][0]['value']
	return info, False

def playlist_sp(drv, plid):

	drv.implicitly_wait(5)	
	drv.get('https://y.qq.com/n/yqq/playlist/'+plid+'.html')
	sleep(2)

	info = {
		'dissid': plid,
		'dissname': elms(drv, '/html/body/div[2]/div[1]/div/div[1]/h1', 'title')[0],
		'songlist': [],}	
	sl = etree.HTML(drv.page_source).xpath('/html/body/div[2]/div[2]/div[1]/div[1]/ul[2]/li/div/div[3]/span/a/@href')
	for s in sl:
		s = s[28:s.find('.html')]
		info['songlist'].append(s)

	return info

def toplist_sp(topid, date, song_num):

	prs = {
		'tpl': 1,
		'page': 'detail',
		'date': date,
		'topid': topid, # 26hot, 5main, 59hk, 61tw, 3ea, 16kr, 17jp
		'type': 'top',
		'song_begin': 0,
		'song_num': song_num,
		'g_tk': 5381,
		'loginUin': 0,
		'hostUin': 0,
		'format': 'json',
		'inCharset': 'utf8',
		'outCharset': 'utf8',
		'notice': 0,
		'platform': 'yqq.json',
		'needNewCode': 0,}

	r = requests.get('https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg', params=prs)
	f = open('./json/'+topid+'_'+date+'_'+song_num+'.txt', 'w', encoding='utf8')
	r.encoding = 'utf-8'
	print(r.text, file=f)
	f.close()+

	js = json.loads(r.text)
	infolist = []
	for song in js['songlist']:
		infolist.append(song_sp(song['data']['songmid']))
		print(song['cur_count'])

	f = open('./json/'+topid+'_'+date+'_'+song_num+'.json', 'w', encoding='utf-8')
	json.dump(infolist, f, indent=4, ensure_ascii=False)
	f.close()

def listexp(plid, depth, mpl, localcheck):

	if mpl<=0:
		mpl = 9999

	drv = Edge('msedgedriver.exe')

	tmp = []
	if localcheck:
		folderlist = listdir('./json')
		for fd in folderlist:
			if fd=='new':
				continue
			if fd.find('7z')>0:
				continue
			print('./json/'+fd+'/'+'playlist'+fd+'.json')
			f = open('./json/'+fd+'/'+'playlist'+fd+'.json', 'r')
			tmp.extend(json.load(f))
			f.close()
		print('LocalCheck Done')

	f = open('./json/new/playlist.json', 'w', encoding='utf-8')
	print('[', file=f)
	f.close()
	f = open('./json/new/songlist.json', 'w', encoding='utf-8')
	print('[', file=f)
	f.close()

	pllk = []
	for ln in tmp:
		if ln[0:ln.find('_')] not in pllk:
			pllk.append(ln[0:ln.find('_')])

	plsk = []	
	tupll = [plid]
	for d in range(depth):
		upll = {}
		for tuplid in tupll:
			if tuplid not in pllk:
				upll[tuplid] = playlist_sp(drv, tuplid)
				pllk.append(tuplid)
			if len(upll)==200:
				break
		tupll = []

		cnt = -len(upll)
		for pl in upll.values():
			print(d, cnt, len(tupll), end=' ')
			print(pl['dissname'])
			cnt = cnt + 1

			pls = []
			tsl = pl['songlist']
			if len(tsl)>mpl:
				tsl = tsl[0:mpl]
			for sid in tsl:
				if sid not in plsk:
					ts,err = song_sp(drv, sid)
					if err:
						continue
					plsk.append(sid)
					pls.append(ts)
					if len(tupll)<500:
						if len(ts['rela_hot'])==3:
							ts['rela_hot'] = ts['rela_hot'][:2]
						for tuplid in ts['rela_hot']:
							tupll.append(tuplid)

			f = open('./json/new/'+pl['dissid']+'_pll.json', 'w', encoding='utf-8')
			json.dump([pl], f, indent=4, ensure_ascii=False)
			f.close()
			f = open('./json/new/'+pl['dissid']+'_pls.json', 'w', encoding='utf-8')
			json.dump(pls, f, indent=4, ensure_ascii=False)
			f.close()

			f = open('./json/new/playlist.json', 'a', encoding='utf-8')
			print('    "'+pl['dissid']+'_pll.json",', file=f)
			f.close()

			f = open('./json/new/songlist.json', 'a', encoding='utf-8')
			print('    "'+pl['dissid']+'_pls.json",', file=f)
			f.close()

	f = open('./json/new/playlist.json', 'a', encoding='utf-8')
	print(']', file=f)
	f.close()
	f = open('./json/new/songlist.json', 'a', encoding='utf-8')
	print(']', file=f)
	f.close()

	drv.quit()

#playlist_sp('4237344828')
listexp('7075523230', 5, 0, True)
