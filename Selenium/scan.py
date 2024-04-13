import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait


def parse_html_potential_url(driver, url, args):
    links = []
    
    url_tags = ['a', 'link', 'img', 'script', 'iframe', 'source', 'area']
    tags_scan_or_not = {'a': args.a_tag, 'link': args.link_tag, 'img': args.img_tag, 'script': args.script_tag, 'iframe': args.iframe_tag, 'source': args.source_tag, 'area': args.area_tag}
    url_tags_attr = {'a': 'href', 'link': 'href', 'img': 'src', 'script': 'src', 'iframe': 'src', 'source': 'src', 'area': 'href'}
    
    print(url)
    driver.get(url)
    wait = WebDriverWait(driver,5)
    # a_elements = driver.find_elements_by_tag_name("a")
    # for a in a_elements:
    #     href = a.get_attribute("href")
    #     if href is not None:
    #         potential_urls.append(href)
    for tag in url_tags:
        if tags_scan_or_not[tag]:
            for element in driver.find_elements(By.TAG_NAME, tag):
                if element.get_attribute(url_tags_attr[tag]) is not None and element.get_attribute(url_tags_attr[tag]) != '':
                    if "http" not in element.get_attribute(url_tags_attr[tag]) and "https" not in element.get_attribute(url_tags_attr[tag]):
                        if element.get_attribute(url_tags_attr[tag])[:2] == '//':
                            complete_url = "https:" + element.get_attribute(url_tags_attr[tag]) # //example.com -> http://example.com
                        elif element.get_attribute(url_tags_attr[tag])[:2] == './':
                            complete_url = url + element.get_attribute(url_tags_attr[tag])[1:] # ./p -> current url + 'p'
                        elif element.get_attribute(url_tags_attr[tag])[0] == '#':
                            complete_url = url + element.get_attribute(url_tags_attr[tag])
                        elif element.get_attribute(url_tags_attr[tag])[:4] == 'tel:' or element.get_attribute(url_tags_attr[tag])[:7] == 'mailto:':
                            pass
                        else:
                            complete_url = "/".join(url.split('/')[:3]) + element.get_attribute(url_tags_attr[tag]) # /zh-CN/docs/Web/HTML -> https://developer.mozilla.org/zh-CN/docs/Web/HTML
                    else:
                        complete_url = element.get_attribute(url_tags_attr[tag])
                    links.append(complete_url.replace(' ', ''))
        else:
            pass

    return sorted(list(set(links)))

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', '--file', dest='file', help='static html file path', default='./scanRootURLs.txt')
    parser.add_argument('-o', '--output', dest='output', help='output file path', default='./scan_output/')
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
    
    s = Service(r'./chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    
    for url in urls:
        print('[+] Now scanning: ' + url)
        file_name = args.output + 'potential_url_' + url.split('/')[2] + '.txt'
        list_data = parse_html_potential_url(driver, url, args)

        if list_data:
            with open(file_name, 'w', encoding='utf-8') as f:
                for item in list_data:
                    f.write("%s\n" % item)

if __name__ == '__main__':
    main()