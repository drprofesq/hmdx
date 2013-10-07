import sys

import glob, os

import log

def readtext(filepath):
    log.debug('Reading file "%s" as text' % filepath)
    with open (filepath, 'r') as f:
        return f.read()
        
def findfiles(pattern, path=None):
    if path:
        pattern = joinpath(path, pattern)
    return glob.glob(pattern)
    
def joinpath(path1, path2):
    return os.path.join(path1, path2)

def main(argv=None):
    pass

if __name__ == '__main__':
    sys.exit(main(sys.argv))
