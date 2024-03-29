# Find All URLs in A Webpage
## What is this?
This is a tool try to parse a webpage html code and find all potential urls with the script myself or using [urlscan](https://urlscan.io/) API

## How to use
If you want to use, just decide which method you'd prefer(My own script or urlscan's API). And then just go to their own folder.

### My Script
Put your target in `scanRootURLs.txt`. It'll parse all `a` tag, `link` tag, `img` tag, `script` tag, `iframe` tag, `source` tag, `area` tag, and find url for each attribute as more as possible. The output is default stored at `./Self Script/scan_output/`

* It'll use ./scanRootURLs.txt as input target Root URL to scan and put output to ./scan_output
  ```bash
  $ python parse_html_potential_url.py
  ```
* To use static scan attribute, you must manually store the webpage html in ./static_scan_input and it'll use ./scanRootURLs.txt as target to fetch the static file in ./static_scan_input
  ```bash
  $ python parse_html_potential_url.py --static_scan
  ```

* All CLI arguments
  ```bash
  $ python parse_html_potential_url.py -h
  usage: parse_html_potential_url.py [-h] [--static_scan] [-f FILE] [-o OUTPUT] [-i INPUT]

  Process some integers.

  optional arguments:
    -h, --help            show this help message and exit
    --static_scan         use static html file to scan or not
    -f FILE, --file FILE  static html file path
    -o OUTPUT, --output OUTPUT
                          output file path
    -i INPUT, --input INPUT
                          input file path
  ```

### URLScan
I just try to call [urlscan](https://urlscan.io/)'s API and parse the result to store in `./scan_output`. Some URL cannot be parsed by urlscan because of some reason such as looking like a spam or submitted URL was blocked from scannning.

* It'll use the URLs in ./scanRootURLs.txt as default and store the output result in ./scan_output
  ```bash
  $ python urlscan.py
  ```

* All CLI arguments
  ```bash
  $ python urlscan.py -h
  usage: urlscan.py [-h] [-f FILE] [-o OUTPUT]

  Process some integers.

  optional arguments:
    -h, --help            show this help message and exit
    -f FILE, --file FILE  static html file path
    -o OUTPUT, --output OUTPUT
                          output file path
  ```