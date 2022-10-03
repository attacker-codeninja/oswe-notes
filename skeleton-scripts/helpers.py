def url_encode_all(url):
    return "".join("%{0:0>2}".format(format(ord(char), "x")) for char in url)

def url_encode_unsafe(url):
    return requests.utils.quote(url, safe='')
