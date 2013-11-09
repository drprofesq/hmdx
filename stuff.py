import sys

import glob, os, copy

import yaml

import log

def fileexists(filepath):
    return os.path.isfile(filepath)

def folderexists(folderpath):
    return  os.path.isdir(folderpath)

def readtext(filepath):
    log.verbose('Reading file "%s" as text' % filepath)
    with open (filepath, 'r') as f:
        return f.read()

def writetext(filepath, text):
    log.verbose('Writing to text file "%s"' % filepath)
    with open (filepath, 'w') as f:
        f.write(text)
        
def findfiles(pattern, path=None):
    if path:
        pattern = joinpath(path, pattern)
    return glob.glob(pattern)

def findfolders(path):
    return [ os.path.join(path, name) for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) ]
    
def filename(path, ext=True):
    filename = os.path.basename(path)
    if not ext:
        filename = os.path.splitext(filename)[0]
    return filename
    
def foldername(path):
    return os.path.dirname(path)
    
def fileext(path):
    return os.path.splitext(path)[1]
    
def joinpath(path1, path2):
    return os.path.join(path1, path2)

def dump(filename, whatever):
    text = yaml.dump(whatever, default_flow_style=False)
    writetext(filename, text)
    
def restore(filename):
    if not fileexists(filename):
        return None
    with open(filename, 'r') as yamlfile:
        return yaml.load(yamlfile)
        
def deepcopy(something):
    return copy.deepcopy(something)

def main(argv=None):
    pass

if __name__ == '__main__':
    sys.exit(main(sys.argv))
