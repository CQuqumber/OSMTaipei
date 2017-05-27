'''
Task:
1. 修正，興趣屬性的Value值
2. 設計輸出格式
3. 轉 xml 檔案為 json

輸出： json file 格式如以下
{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"Tour":{ 
		 'building':....,
		 'amenity':.....,
		 'public_transport':.......
	},
"Daily":{
		'shop':....., 
		'leisure':..., 
		'natural':.......
	}
}
'''

import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json

problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
OSMFILE = 'taipei_taiwan.osm'


def audit_info(elem):
    '''修正information value'''
    infomap = {'map; guidepost': 'guidepost', 'guide_post' :'guidepost'}
    if elem in infomap.keys():
        return elem.replace(elem, infomap[elem])
    return elem

def audit_wiki(elem):
    '''移除zh'''
    if elem.startswith('zh:E%'):
        return None
    elif elem.startswith('zh:'):
        return elem[3:]
    return elem

def audit_surface(elem):
	'''修正surfeace重複項目'''
    surmap = {'瀝青':'asphalt', 'cement_paving':'asphalt', 'asphalt;paving_stones':'asphalt',
              'asphaltdesignated':'asphalt','sett' :'paving_stones', 'paving_stones:30': 'paving_stones'}
    if elem in surmap.keys():
        return elem.replace(elem, surmap[elem])
    return elem

def audit_operator(elem):
	'''修正operator(重複項目'''
    opermap = {'台灣中油股份有限公司':'台灣中油', '中國石油':'台灣中油','中華郵政股份有限公司':'中華郵政',
                '臺灣鐵路管理局':'Taiwan Railway Administration',
                '7-11':'7-Eleven', '7-ELEVEN':'7-Eleven', '統一超商':'7-Eleven', '統一超商股份有限公司':'7-Eleven',
                '萊爾富國際':'萊爾富國際股份有限公司', '萊爾富':'萊爾富國際股份有限公司',
                'Family Mart':'全家便利商店', '全家便利商店股份有限公司':'全家便利商店', '全家':'全家便利商店',
                'FamilyMart':'全家便利商店', '台灣麥當勞餐廳股份有限公司':'麥當勞',
                '台北市政府':'臺北市政府 Taipei City Government', 'Starbucks Coffee':'星巴克'}
    if elem in opermap.keys():
        return elem.replace(elem, opermap[elem])
    return elem

def audit_maxspeed(elem):
	'''轉整數型態'''
    return int(elem)


def shape_element(element):
    node = {}
    created = {}
    address = {}
    firehydrant= {}
    tour = {}
    daily = {}

    high_lv_items = ['id', 'visible']

    CreatedField = [ "version", "changeset", "timestamp", "user", "uid"]

    daily_of_interest = ['building', 'amenity', 'public_transport', 
                         'landuse', 'operator', 'surface', 'maxspeed', 'religion']

    tour_of_interest = ['shop', 'leisure', 'natural', 'opening_hours', 'tourism', 
                        'cuisine', 'information', 'wikipedia'] #information, wikipedia, surface, operator

    if element.tag == "node" or element.tag == "way":
        node['type'] = element.tag 

        keys = element.attrib.keys()
        for item in keys:
            if item in CreatedField:
                created[item] = element.attrib[item]

            if item in high_lv_items:
                node[item] = element.attrib[item]

            if 'lat' in keys:
                node['pos'] = [float(element.attrib['lat']), float(element.attrib['lon'])]
        node['Created'] = created

        for sec_tag in element:
            ref = []
            if sec_tag.tag == 'nd':
                ref.append(sec_tag.attrib['ref'])
                node['Refs'] = ref

            if sec_tag.tag == 'tag':
                if problemchars.search(sec_tag.attrib['k']):
                    continue
                if sec_tag.attrib['k'].startswith('addr:') and \
                    sec_tag.attrib['k'].count(':')==1:
                    __, __, add_key = sec_tag.attrib['k'].partition(':')
                    address[add_key] = sec_tag.attrib['v']
                    node['Address'] = address 

                if sec_tag.attrib['k'].startswith('fire_hydrant:') :
                    _, _ , fire_item = sec_tag.attrib['k'].partition(':')
                    firehydrant[fire_item] = sec_tag.attrib['v']
                    node['FireHydrant'] = firehydrant 

                if sec_tag.attrib['k'] in tour_of_interest:
                    if sec_tag.attrib['k'] == 'information':
                        tour[sec_tag.attrib['k']] = audit_info(sec_tag.attrib['v'])
                        node['Tour'] = tour
                    elif sec_tag.attrib['k'] == 'wikipedia':
                        tour[sec_tag.attrib['k']] = audit_wiki(sec_tag.attrib['v'])
                        node['Tour'] = tour
                    else:
                        tour[sec_tag.attrib['k']] = sec_tag.attrib['v']
                        node['Tour'] = tour

                if sec_tag.attrib['k'] in daily_of_interest:
                    if sec_tag.attrib['k'] == 'surface':
                        daily[sec_tag.attrib['k']] = audit_surface(sec_tag.attrib['v'])
                        node['Daily'] = daily
                    elif sec_tag.attrib['k'] == 'operator':
                        daily[sec_tag.attrib['k']] = audit_operator(sec_tag.attrib['v'])
                        node['Daily'] = daily
                    elif sec_tag.attrib['k'] == 'maxspeed':
                        daily[sec_tag.attrib['k']] = audit_maxspeed(sec_tag.attrib['v'])
                        node['Daily'] = daily
                    else:
                        daily[sec_tag.attrib['k']] = sec_tag.attrib['v']
                        node['Daily'] = daily
        return node
    else:
        return None

def process_map(file_in, pretty = False):
    '''轉換ＸＭＬ成為JSON檔案'''
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+","+"\n") # added a comma
                else:
                    fo.write(json.dumps(el) +","+ "\n")
    return data

if __name__ == "__main__":
    data = process_map(OSMFILE, True)
