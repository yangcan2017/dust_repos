#/usr/bin/python3
import zlib

import urllib.request
import urllib.error
import urllib

from bs4 import BeautifulSoup
import urllib3

def create_header():
	head = urllib3.util.make_headers(keep_alive=True, accept_encoding="gzip, deflate", user_agent='Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36', basic_auth=None)
	head['Host'] = 'www.hnlawyer.org'
	head['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
	head['Accept-Encoding'] = 'gzip, deflate, sdch'
	head['Accept-Language'] = 'zh-CN,zh;q=0.8'

	return head


def track_info(tbody, fp):
	trs = tbody.findAll('tr')
	for people in trs[1:]:
		tds = people.findAll('td')
		fp.write("%s %s %s %s %s http://www.hnlawyer.org%s\n" %(tds[0].a.string, tds[1].string, tds[2].string, tds[3].string, tds[4].string, tds[0].a.get('href')))
	return	
	
	
if __name__ == "__main__":
	
	url_prefix = 'http://www.hnlawyer.org/index.php/Home-index-firmcx-is_check-1-p-'	
	result_file = 'henan_firm.txt'	
	
	fp = open(result_file, 'w')
	header = create_header()
	
	page_id = 1
	while True:
		print("Current page: %d" % page_id)
		url = url_prefix + repr(page_id)
		req = urllib.request.Request(url, headers=header)
		response = urllib.request.urlopen(req)
		if response.info().get('Content-Encoding') == 'gzip':
			r_read = zlib.decompress(response.read(), 16+zlib.MAX_WBITS)
		else:    
			r_read = response.read()
		soup = BeautifulSoup(r_read.decode('utf-8'), 'lxml')
		info_soup = soup.find('table')
		if info_soup:
			track_info(info_soup, fp)
		
		page_id += 1
		if page_id > 52:
			break
	
	fp.close()
	print("Done!")
