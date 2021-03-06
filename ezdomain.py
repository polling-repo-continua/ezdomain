"""
SOFTWARE: ezdomain
VERSION : 1.0
AUTHOR  : MAYASEVEN.com
GITHUB  : https://github.com/MAYASEVEN/ezdomain
"""
import requests
import sys
import argparse
import time
import tqdm
import math
from itertools import chain, product
from termcolor import colored
from multiprocessing import Pool

start = time.time()
subdomains = []


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s%s" % (s, size_name[i])


def bruteforce(charset, minlength, maxlength):
    return (''.join(candidate)
            for candidate in chain.from_iterable(product(charset, repeat=i)
                                                 for i in range(minlength, maxlength + 1)))


def main():
    print("""
       ____  ___  __    __   _  _     _    ___   _   _
      |        / |  \  |  | | \/ |   / \    |   | \  |
      |----   /  |   | |  | |    |  /___\   |   |  \ |
      |____  /__ |__/  |__| |    | /     \ _|_  |   \|

                                       by MAYASEVEN.com

    """)
    parser = argparse.ArgumentParser(
        description="""EZdomain is red team tool based on python programming that use to enumerate and scan the domains such as sub-domains, directory, S3 bucket by customizing the position (specific an * in the URL) of the payload and brute-forcing with provided wordlists or string generated.""")
    parser.add_argument("-d", "--domain", type=str,
                        help="Providing a domain name (ex. domain-*.com)")
    parser.add_argument("-w", "--wordlist", type=str,
                        help="Providing a path of a wordlist file")
    parser.add_argument("-b", "--bruteforce", type=str,
                        help="Providing the character set (default are eariotnslcudpmhgbfywkvxzjq)")
    parser.add_argument("-min", "--min-length", type=str,
                        help="Providing the min length of string (default is 1)")
    parser.add_argument("-max", "--max-length", type=str,
                        help="Providing the max length of string (default is 3)")
    parser.add_argument("-o", "--output", type=str,
                        help="A standard output format; Providing a path of output file")
    parser.add_argument("-oS", "--output-subdomain", type=str,
                        help="A list of subdomains output; Providing a path of output file")
    parser.add_argument("-t", "--thread", type=str,
                        help="Providing a thread number (default is 3)")
    parser.add_argument("-x", "--exclude", type=str,
                        help="Providing a exclude output status code (ex. -x 443,404)")
    args = parser.parse_args()
    domain = args.domain if args.domain != None else sys.exit(
        "Please specify the domain, using -d (ex. -d domain-*.com)")
    words = args.wordlist
    global outputfile
    outputfile = args.output
    global outputfile_subdomain
    outputfile_subdomain = args.output_subdomain if outputfile == None else None
    global exclude
    exclude = args.exclude.split(",") if args.exclude != None else "999"
    thread = args.thread or 3
    bruteforce_text = args.bruteforce or "eariotnslcudpmhgbfywkvxzjq"
    min_length = args.min_length or 1
    max_length = args.max_length or 3

    try:
        if(words != None):
            file = open(words, 'r')
            word = file.readlines()
        else:
            print("Waiting to generate a set of wordlists..")
            word = list(bruteforce(bruteforce_text,
                                   int(min_length), int(max_length)))
            print(str(len(word))+" words generated")

        p = Pool(processes=int(thread))
        pbar = tqdm.tqdm(p.imap_unordered(checkurl, [domain.replace(
            '*', x.split('\n')[0].strip()) for x in word]), total=len(word), desc="[Progress]", unit="word")
        if(outputfile != None):
            sys.stdout = open(outputfile, 'w')
        for message in pbar:
            if(message != None and message[1]):
                pbar.write("\r"+" "*150+"\r"+message[1])
                subdomains.append(message[0])
                pbar.update()
                time.sleep(0.1)
        if(outputfile_subdomain != None):
            f = open(outputfile_subdomain, "w+")
            for i in set(subdomains):
                f.write(i+'\n')
            f.close()
            print("\n".join(map(str, set(subdomains))))
    except KeyboardInterrupt:
        p.terminate()
        sys.exit()
    except Exception as e:
        print("Error messages: {%s} \nusage: python ezdomain.py -h" % e)
        sys.exit()


def checkurl(url):
    status = ''
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1'}
        conn = requests.get(url, headers=headers)
        if(conn.url != url and '302' not in exclude):
            status = "{} - {} - {}{}".format(
                colored('[302]', 'blue'),
                convert_size(len(conn.content)),
                url,
                colored(" > "+conn.url, 'white')
            )

        elif (conn.status_code == 200 and '200' not in exclude):
            status = "{} - {} - {}".format(
                colored('[200]', 'green'),
                convert_size(len(conn.content)),
                url
            )

    except requests.exceptions.HTTPError as e:
        if(str(e.response.status_code) not in exclude):
            status = "{} - {} - {}".format(
                colored('[{}]'.format(e.code), 'red'),
                convert_size(len(e.read())),
                url
            )

        else:
            return
    except:
        return

    if(outputfile != None and outputfile_subdomain != None):
        print("\r"+" "*150+"\r"+status+"inloop")

    return (url, status)


if __name__ == "__main__":
    main()
