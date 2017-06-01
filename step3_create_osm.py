'''
Task:
Create Sample OSM file
'''

OSM_FILE = "taipei_taiwan.osm"  # Replace this with your osm file
SAMPLE_FILE = "sample_taipei_taiwan.osm"


def get_element(osm_file, tags=('node', 'way', 'tag'), k = 10 ):
        # K Parameter: take every k-th top level element
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write('</osm>')

if __name__ == "__main__":
     get_element(OSM_FILE, tags=('node', 'way', 'tag'), k = 10 )