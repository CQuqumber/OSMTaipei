'''
1. 計算標籤數
2. 計算內層標籤數
3. 統計內從標籤屬性總數

'''

from collections import defaultdict
from collections import Counter
import xml.etree.cElementTree as ET
import pprint
import re
import json

OSMFILE = 'taipei_taiwan.osm'  #  ＯＳＭ檔名


def count_tag(filename):
'''計算文檔標籤數，回傳依序字典'''
	TAG = Counter()
	context = ET.iterparse(filename, events=("start",))
	for event, elem in context:
    	if elem.tag in TAG:
        	TAG[elem.tag] += 1
    	else:
        	TAG[elem.tag] = 1
	return TAG.most_common()


def count_2nd_tag(filename):
	'''計算way and node標籤底下的，keys attribute '''
	count = Counter()
	for _, element in ET.iterparse(filename):
    	if element.tag == "node" or element.tag == "way":
        	for sec_tag in element:
            	if sec_tag.tag == 'tag':
                	if sec_tag.attrib['k'] in count:
                    	count[sec_tag.attrib['k']] += 1
                	else:
                    	count[sec_tag.attrib['k']] = 1
	return count.most_common()


def keys_attribute(filename, keys):
	'''查詢興趣attribute的統計數目'''
	D = Counter()
	for _, element in ET.iterparse(filename):
    	if element.tag == 'node' or element.tag =='way':
        	for child in element:
            	if child.tag == 'tag':
                	if child.attrib['k'] == 'keys':
                    	if child.attrib['v'] in D:
                        	D[child.attrib['v']] +=1
                    	else:
                        	D[child.attrib['v']] = 1
	return D.most_common()


if __name__ == '__main__':

    # audit/count tag
    tags = count_tags(OSMFILE)
    print("計算主要標籤:")
    pprint.pprint(tags)

    # audit/count secondary tag
    secondary_tag = count_secondary_tag(OSMFILE)
    print("計算內層標籤:", '\n', secondary_tag)

    print("打印出興趣標籤屬性:")
    print(keys_attribute(OSMFILE, keys))








