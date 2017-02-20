
def prihodi(postaja):
    from urllib.request import urlopen, Request
    url = 'http://wbus.lpp.si/wap.aspx'
    data = '__EVENTTARGET=&__EVENTARGUMENT=&tb_postaja={}&b_send=Prika%C5%BEi'.format(postaja)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}
    req = Request(url, data.encode("utf-8"), headers)
    return urlopen(req).read().decode("utf-8")

txt = prihodi('803211')
print(txt)