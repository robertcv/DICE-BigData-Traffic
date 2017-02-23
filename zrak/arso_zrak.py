from urllib.request import urlopen
import xml.etree.ElementTree as ET

url = 'http://www.arso.gov.si/xml/zrak/ones_zrak_urni_podatki_zadnji.xml'

resp = urlopen(url).read().decode("utf-8")

root = ET.fromstring(resp)

for child in root.findall('./postaja[@sifra="E21"]'):
    for c in child:
        print(c.tag + " - " +c.text)
