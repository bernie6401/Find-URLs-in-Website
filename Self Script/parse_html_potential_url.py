from bs4 import BeautifulSoup
import requests
import argparse


def url_connect_and_get_body(url, input_file_path, static_url=False):
    if not static_url:
        try:
            print('[*] Now Connect to ' + url)
            html = requests.get(url)
        except:
            print("[x] Error: Cannot get the URL: " + url)
            return 0
        s = BeautifulSoup(html.text, 'html.parser')
    else:
        url_preprocess = url.split('//')[-1].replace('/', '_')
        if url_preprocess[-1] == '/':
            url_preprocess = url_preprocess[:-1]
        filename = input_file_path + url_preprocess + '.html'
        html = open(filename, 'r', encoding='utf-8').read()
        s = BeautifulSoup(html, 'html.parser')
    return s.body

def parse_html_potential_url(body_content, url, args):
    links = []
    
    url_tags = ['a', 'link', 'img', 'script', 'iframe', 'source', 'area']
    tags_scan_or_not = {'a': args.a_tag, 'link': args.link_tag, 'img': args.img_tag, 'script': args.script_tag, 'iframe': args.iframe_tag, 'source': args.source_tag, 'area': args.area_tag}
    url_tags_attr = {'a': 'href', 'link': 'href', 'img': 'src', 'script': 'src', 'iframe': 'src', 'source': 'src', 'area': 'href'}
    for tag in url_tags:
        if tags_scan_or_not[tag]:
        #     if tag == 'a':
        #         for element in body_content.find_all('a'):
        #             if element.get('href') is not None and element.get('href') != '':
        #                 if "http" not in element.get('href') and "https" not in element.get('href'):
        #                     if element.get('href')[:2] == '//':
        #                         complete_url = "https:" + element.get('href') # //example.com -> http://example.com
        #                     elif element.get('href')[:2] == './':
        #                         complete_url = url + element.get('href')[1:] # ./p -> current url + 'p'
        #                     elif element.get('href')[0] == '#':
        #                         complete_url = url + element.get('href')
        #                     elif element.get('href')[:4] == 'tel:' or element.get('href')[:7] == 'mailto:':
        #                         pass
        #                     else:
        #                         complete_url = "/".join(url.split('/')[:3]) + element.get('href') # /zh-CN/docs/Web/HTML -> https://developer.mozilla.org/zh-CN/docs/Web/HTML
        #                 else:
        #                     complete_url = element.get('href')
                        
        #                 links.append(complete_url.replace(' ', ''))
        #     else:
        #         for element in body_content.find_all(tag):
        #             if element.get(url_tags_attr[tag]) is not None:
        #                 if "http" not in element.get(url_tags_attr[tag]) and "https" not in element.get(url_tags_attr[tag]):
        #                     complete_url = url[:-1] + element.get(url_tags_attr[tag])
        #                 else:
        #                     complete_url = element.get(url_tags_attr[tag])
        #                 links.append(complete_url.replace(' ', ''))
            for element in body_content.find_all(tag):
                if element.get(url_tags_attr[tag]) is not None and element.get(url_tags_attr[tag]) != '':
                    if "http" not in element.get(url_tags_attr[tag]) and "https" not in element.get(url_tags_attr[tag]):
                        if element.get(url_tags_attr[tag])[:2] == '//':
                            complete_url = "https:" + element.get(url_tags_attr[tag]) # //example.com -> http://example.com
                        elif element.get(url_tags_attr[tag])[:2] == './':
                            complete_url = url + element.get(url_tags_attr[tag])[1:] # ./p -> current url + 'p'
                        elif element.get(url_tags_attr[tag])[0] == '#':
                            complete_url = url + element.get(url_tags_attr[tag])
                        elif element.get(url_tags_attr[tag])[:4] == 'tel:' or element.get(url_tags_attr[tag])[:7] == 'mailto:':
                            pass
                        else:
                            complete_url = "/".join(url.split('/')[:3]) + element.get(url_tags_attr[tag]) # /zh-CN/docs/Web/HTML -> https://developer.mozilla.org/zh-CN/docs/Web/HTML
                    else:
                        complete_url = element.get(url_tags_attr[tag])
                    links.append(complete_url.replace(' ', ''))
        else:
            pass

    return sorted(list(set(links)))

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--static_scan', dest='static_scan', action='store_true', help='use static html file to scan or not', default=False)
    parser.add_argument('-f', '--file', dest='file', help='static html file path', default='./scanRootURLs.txt')
    parser.add_argument('-o', '--output', dest='output', help='output file path', default='./scan_output/')
    parser.add_argument('-i', '--input', dest='input', help='input file path', default='./static_scan_input/')
    parser.add_argument('--no_a_tag', dest='a_tag', action='store_false', help='scan a tag or not', default=True)
    parser.add_argument('--no_link_tag', dest='link_tag', action='store_false', help='scan link tag or not', default=True)
    parser.add_argument('--no_img_tag', dest='img_tag', action='store_false', help='scan img tag or not', default=True)
    parser.add_argument('--no_script_tag', dest='script_tag', action='store_false', help='scan script tag or not', default=True)
    parser.add_argument('--no_iframe_tag', dest='iframe_tag', action='store_false', help='scan iframe tag or not', default=True)
    parser.add_argument('--no_source_tag', dest='source_tag', action='store_false', help='scan source tag or not', default=True)
    parser.add_argument('--no_area_tag', dest='area_tag', action='store_false', help='scan area tag or not', default=True)
    parser.add_argument('-u', '--url', dest='url', help='Single url to scan', default='****')

    args = parser.parse_args()

    if args.url == '****':
        urls = open(args.file, 'r').read().splitlines()
    else:
        urls = [args.url]
    for url in urls:
        print('[+] Now scanning: ' + url)
        file_name = args.output + 'potential_url_' + url.split('/')[2] + '.txt'
        list_data = parse_html_potential_url(url_connect_and_get_body(url, args.input, args.static_scan), url, args)

        if list_data:
            with open(file_name, 'w', encoding='utf-8') as f:
                for item in list_data:
                    f.write("%s\n" % item)

if __name__ == '__main__':
    main()