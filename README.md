## About EZDomain

                               ____  ___  __    __   _  _     _    ___   _   _
                              |        / |  \  |  | | \/ |   / \    |   | \  |
                              |----   /  |   | |  | |    |  /___\   |   |  \ |
                              |____  /__ |__/  |__| |    | /     \ _|_  |   \|

                                                               by MAYASEVEN.com
                                           
EZdomain is red team tool based on python programming that use to enumerate and scan the domains such as sub-domains, directory, file, S3 bucket by customizing the position (specific an * in the URL) of the payload and brute-forcing with provided wordlists or string generated.

## Installation
```
git clone https://github.com/mayaseven/ezdomain.git
```

## Dependencies
Python modules (requests, argparse, tqdm, multiprocessing, termcolor)

- Installation on Windows:
```
c:\python3\python.exe -m pip install -r requirements.txt
```

- Installation on Linux and MacOSX
```
sudo pip3 install -r requirements.txt
```

## Usage

| Short         | Long            | Description
| ------------- |-----------------|------------
| -d            | --domain        | Providing a domain name (ex. domain-*.com)
| -w            | --wordlist      | Providing a path of a wordlist file
| -b            | --bruteforce    | Providing the character set (eariotnslcudpmhgbfywkvxzjq)
| -min          | --min-length    | Providing the min length of string (default is 1)
| -max          | --max-length    | Providing the max length of string (default is 3)
| -o            | --output        | Providing a path of output file
| -oS           | --output-subdomain| A list of subdomains output; Providing a path of output file
| -t            | --thread        | Providing a thread number (default is 3)
| -x            | --exclude       | Providing a exclude output status code (ex. -x 443,404)
| -h            | --help          | show this help message and exit

### Examples
* To list all the options use -h
```
python3 ezdomain.py -h
```

* To find the sub-domains
```
python3 ezdomain.py -d http://*.domain.com/ -w wordlists/subdomain/subdomains-1000.txt
```

* To find the directory or file in the domain
```
python3 ezdomain.py -d https://domain.com/* -w wordlists/directory/directory-list-med.txt -x 404
```

* To find the S3 bucket (You can exclude the 403 status code to find only a public bucket)
```
python3 ezdomain.py -d http://company-*.s3.amazonaws.com/ -w wordlists/word/common-words.txt -x 404
```

* To brute-force the domain with character set and you can provide a min or a max length of the payload string
```
python3 ezdomain.py -d https://*.domain.com/ -b abc -min 3 -max 5
```

## License
License of ezdomain is under GNU GPL license. [LICENSE](https://github.com/MAYASEVEN/ezdomain/blob/master/LICENSE)

## Version
**Current version is 1.0**
