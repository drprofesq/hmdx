import sys

import log, stuff

def loadalltemplates(folder, templates):
    loaded = {}
    templatefiles = stuff.findfiles('*.yaml', folder)
    entries = {}
    for templatefile in templatefiles:
        namespace = stuff.filename(templatefile, ext=False).lower()
        content = stuff.restore(templatefile)
        entries[namespace] = entry = {}
        entry['namespace'] = namespace
        entry['content'] = content
        entry['dependencies'] = dependencies = []
        for item in content:
            if 'base' in item:
                for basetype in item['base']:
                    if not '.' in basetype:
                        continue
                    basenamespace = basetype[:basetype.index('.')].lower()
                    if namespace == basenamespace:
                        continue
                    if not basenamespace in dependencies:
                        dependencies.append(basenamespace)
                        
    toload = []
    notloaded = list(entries.keys())
    progress = False
    while len(notloaded) > 0:
        stillnotloaded = list(notloaded)
        for check in stillnotloaded:
            entry = entries[check]
            dependencies = entry['dependencies']
            ready = True
            for dependency in dependencies:
                if not dependency in toload:
                    ready = False
                    break
            if ready:
                notloaded.remove(check)
                toload.append(check)
                progress = True
        if not progress:
            log.warning('Could not load all dependencies: %s' % notloaded)
            for giveup in notloaded:
                toload.append(giveup)
            break
    
    for namespace in toload:
        entry = entries[namespace]
        content = entry['content']
        loaded[namespace] = loadtemplates(namespace, content, templates)
    return loaded

def loadtemplates(namespace, contents, templates):
    loadedtemplates = []
    for item in contents:
        if not 'name' in item:
            log.warning('No name for %s' % item)
            continue
        templatename = '%s.%s' % (namespace, item['name'])
        if 'fullname' in item:
            templatename = item['fullname']
        else:
            item['fullname'] = templatename
        parents = []
        fullbase = []
        if 'base' in item:
            for basetype in item['base']:
                fullbasename = basetype
                if not '.' in basetype:
                    fullbasename = '%s.%s' % (namespace, basetype)
                if not fullbasename in templates:
                    log.warning('Could not find %s in templates' % fullbasename)
                    continue
                fullbase.append(fullbasename)
                parents.append(templates[fullbasename])
            item['base'] = fullbase
        template = templates[templatename] = CascadeDict(parents, source=item)
        loadedtemplates.append(template)
    return loadedtemplates
    
def findnonbasetemplates(templatelist):
    basenames = []
    for template in templatelist:
        if 'base' in template:
            for basename in template['base']:
                if not basename in basenames:
                    basenames.append(basename)
    nonbase = []
    for template in templatelist:
        name = template['fullname']
        if not name in basenames:
            nonbase.append(template)
    return nonbase
    
def clone(template):
    return CascadeDict([template])

class CascadeDict:

    def __init__(self, parents=[], source={}):
        self.dict = {}
        self.parents = parents
        for key in source:
            self[key] = source[key]

    def __getitem__(self, key):
        if key in self.dict and not self.dict[key] is None:
            return self.dict[key]
        else:
            for parent in self.parents:
                if key in parent and not parent[key] is None:
                    return parent[key]
            raise KeyError('Key not found: %s' % key)
    def __setitem__(self, key, value):
        if value is None:
            raise ValueError('Value cannot be None')
        self.dict[key] = value
    def __delitem__(self, key):
        self.dict[key] = None 
    def keys(self):
        keys = []
        tocheck = [self.dict]
        tocheck.extend(self.parents)
        for checkdict in tocheck:
            for key in checkdict.keys():
                if not key in keys and not checkdict[key] is None:
                    if not key in self.dict or not self.dict[key] is None:
                        keys.append(key)
        return keys
    
    # second level definitions which assume only getitem and keys
    def has_key(self, key):
         return key in self.keys()
    def __iter__(self):
        for k in self.keys():
            yield k

    # third level uses second level instead of first
    def __contains__(self, key):
        return self.has_key(key)            
    def iteritems(self):
        for k in self:
            yield (k, self[k])

    # fourth level uses second and third levels instead of first
    def iterkeys(self):
        return self.__iter__()
    def itervalues(self):
        for _, v in self.iteritems():
            yield v
    def values(self):
        return list(self.itervalues())
    def items(self):
        return list(self.iteritems())
    def clear(self):
        for key in self.keys():
            del self[key]
    def setdefault(self, key, default):
        if key not in self:
            self[key] = default
            return default
        return self[key]
    def popitem(self):
        key = self.keys()[0]
        value = self[key]
        del self[key]
        return (key, value)
    def update(self, other):
        for key in other.keys():
            self[key] = other[key]
    def get(self, key, default=None):
        if key in self:
            return self[key]
        return default
    def __repr__(self):
        return repr(dict(self.items()))

def test():
    pass

def main(argv=None):
    test()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
