import sys

import xml.etree.ElementTree as ET

import log, stuff

def importgirls(girlsfile):
    log.debug('Importing girls from file %s' % girlsfile)
    importedgirls = []
    contents = stuff.readtext(girlsfile)
    xml = ET.ElementTree(ET.fromstring(contents))
    girls = xml.findall('Girl')
    for girl in girls:
        importedgirl = {}
        for name, value in girl.attrib.items():
            importedgirl[name] = value
        importedgirl['Traits'] = []
        traits = girl.findall('Trait')
        for trait in traits:
            name = trait.attrib.get('Name')
            if name:
                importedgirl['Traits'].append(name)
        importedgirls.append(importedgirl)
    return importedgirls
    
def importallgirls(girlsdir):
    log.debug('Importing all girls from folder %s' % girlsdir)
    girls = []
    files = stuff.findfiles('*.girlsx', girlsdir)
    for girlsfile in files:
        newgirls = importgirls(girlsfile)
        girls.extend(newgirls)
    log.debug('Imported %s girls' % len(girls))
    return girls
    

def test():
    girls = importallgirls('wmgirls')
    #print girls

def main(argv=None):
    test()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
