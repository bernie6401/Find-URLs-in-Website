from bs4 import BeautifulSoup
import requests

def url_connect_and_get_body(url, static_url=False):
    if not static_url:
        try:
            html = requests.get(url)
        except:
            print("[x] Error: Cannot get the URL: " + url)
            return 0
        s = BeautifulSoup(html.text, 'html.parser')
    else:
        filename = './static_scan_input/' + url.split('//')[-1][:-1] + '.html'
        html = open(filename, 'r', encoding='utf-8').read()
        s = BeautifulSoup(html, 'html.parser')
    return s.body

def parse_html_potential_url(body_content, url):
    links = []
    
    url_tags = ['a', 'link', 'img', 'script', 'iframe', 'source', 'area']
    url_tags_attr = {'a': 'href', 'link': 'href', 'img': 'src', 'script': 'src', 'iframe': 'src', 'source': 'src', 'area': 'href'}
    for tag in url_tags:
        if tag == 'a':
            for element in body_content.find_all('a'):
                if element.get('href') is not None and element.get('href') != '':
                    if "http" not in element.get('href') and "https" not in element.get('href'):
                        if element.get('href')[:2] == '//':
                            links.append(url[:-1] + element.get('href')) # //example.com -> http://example.com
                        elif element.get('href')[:2] == './':
                            links.append('http:' + element.get('href')[1:]) # ./p -> current url + 'p'
                        elif element.get('href')[0] == '#':
                            links.append(url + element.get('href'))
                        elif element.get('href')[:4] == 'tel:' or element.get('href')[:8] == 'mailto:':
                            pass
                        else:
                            links.append("/".join(url.split('/')[:3]) + element.get('href')) # /zh-CN/docs/Web/HTML -> https://developer.mozilla.org/zh-CN/docs/Web/HTML       
                    else:
                        links.append(element.get('href'))
        else:
            for element in body_content.find_all(tag):
                if element.get(url_tags_attr[tag]) is not None:
                    if "http" not in element.get(url_tags_attr[tag]) and "https" not in element.get(url_tags_attr[tag]):
                        links.append(url[:-1] + element.get(url_tags_attr[tag]))
                    else:
                        links.append(element.get(url_tags_attr[tag]))
    return list(set(links))

def main():
    urls = open('./scanRootURLs.txt', 'r').read().splitlines()
    for url in urls:
        print('[+] Now scanning: ' + url)
        file_name = './scan_output/potential_url_' + url.split('/')[2] + '.txt'
        list_data = parse_html_potential_url(url_connect_and_get_body(url, static_url=True), url)
        if list_data:
            with open(file_name, 'w', encoding='utf-8') as f:
                for item in list_data:
                    f.write("%s\n" % item)

if __name__ == '__main__':
    main()