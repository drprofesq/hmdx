import sys

import inspect, os

LEVELS = ['ignore', 'verbose', 'debug', 'warning', 'assertx', 'error', 'info', 'critical']
MIN_PRINT = 'debug'

def ignore(message, tag=None):
    log(tag, 'ignore', message)

def verbose(message, tag=None):
    log(tag, 'verbose', message)

def debug(message, tag=None):
    log(tag, 'debug', message)

def warning(message, tag=None):
    log(tag, 'warning', message)

def assertx(message, shouldBeTrue, tag=None):
    if not shouldBeTrue:
        log(tag, 'assert', message)

def error(message, tag=None):
    log(tag, 'error', message)

def info(message, tag=None):
    log(tag, 'info', message)

def critical(message, tag=None):
    log(tag, 'critical', message)

def log(tag, level, message):
    if not tag:
        caller = callerdetails()
        tag = '%s.%s[%s]' % (caller['module'], caller['method'], caller['line'])
        
    logline = '%s-%s: ** %s **' % (level.upper(), tag, message)
    if LEVELS.index(level) >= LEVELS.index(MIN_PRINT):
        print logline
    
def callerdetails():
    stack = inspect.stack()
    temp = []
    for call in stack:
        path = call[1]
        module = os.path.basename(path)
        module = os.path.splitext(module)[0]
        path = os.path.splitext(path)[0]
        filename = os.path.splitext(__file__)[0]
        line = call[2]
        method = call[3]
        #temp.append('path "%s"' % path)
        #temp.append('file "%s"' % filename)
        #temp.append('line "%s"' % line)
        #temp.append('method "%s"' % method)
        if filename == path:
            continue
        caller = {}
        caller['module'] = module
        caller['method'] = method
        caller['line'] = line
        #print caller
        #print temp
        return caller

def main(argv=None):
    pass

if __name__ == '__main__':
    sys.exit(main(sys.argv))
