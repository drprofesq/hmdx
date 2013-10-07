import sys

import inspect, os

LEVELS = ['ignore', 'verbose', 'debug', 'warning', 'assertx', 'error', 'info', 'critical']

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
    print logline
    
def callerdetails():
    stack = inspect.stack()
    for call in stack:
        path = call[1]
        if path == __file__:
            continue
        module = os.path.splitext(path)[0]
        line = call[2]
        method = call[3]
        caller = {}
        caller['module'] = module
        caller['method'] = method
        caller['line'] = line
        return caller

def main(argv=None):
    pass

if __name__ == '__main__':
    sys.exit(main(sys.argv))
