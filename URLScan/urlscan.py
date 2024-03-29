import requests
import json
import time
import argparse

def write_file(file_path, data):
    if data:
        with open(file_path, 'w', encoding='utf-8') as f:
            for item in data:
                f.write("%s\n" % item)

def fetch_potential_url(json_file):
    potential_url = []

    # Parse Links
    for url in json_file['data']['links']:
        potential_url.append(url['href'])

    return list(set(potential_url))

def urlscan(url):
    apikey = 'c85f7dd5-4038-4571-9bac-13f56faf421f'
    headers = {'API-Key':apikey,'Content-Type':'application/json'}
    data = {"url": url, "visibility": "public"}

    response = requests.post('https://urlscan.io/api/v1/scan/', headers=headers, data=json.dumps(data))
    if "The submitted URL was blocked from scanning" in response.text:
        print("[x] Error: The submitted URL was blocked from scanning")
        return 0
    if "This scan looks like it might be spam" in response.text:
        print("[x] Error: This scan looks like it might be spam")
        return 0
    print("[+] Connect to ", response.json()['api'])
    result_url= response.json()['api']
    data_result = requests.get(result_url).json()
    while 'status' in data_result:
        if data_result['status'] != 200:
            time.sleep(5)
            print("[x] Error: Connect again")
            data_result = requests.get(result_url).json()
    return data_result

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', '--file', dest='file', help='static html file path', default='./scanRootURLs.txt')
    parser.add_argument('-o', '--output', dest='output', help='output file path', default='./scan_output/')

    args = parser.parse_args()

    urls = open(args.file, 'r').read().splitlines()
    root_dir = './'
    for url in urls:
        print('[+] Now scanning: ' + url)
        file_name = root_dir + args.output + './potential_url_' + url.split('/')[2] + '.txt'
        json_data = urlscan(url)
        if json_data:
            list_data = fetch_potential_url(json_data)
            write_file(file_name, list_data)
        

if __name__ == '__main__':
    main()