import sys

import xml.etree.ElementTree as ET

import log, stuff

import wmimport, template

def convertgirls(importedgirls, basefolder=''):
    log.debug('Converting %s girls' % len(importedgirls))
    templates = {}
    contentfolder = stuff.joinpath(basefolder, 'content')
    loaded = template.loadalltemplates(contentfolder, templates)
    nonbases = template.findnonbasetemplates(loaded['girlbase'])
    girls = []
    for importedgirl in importedgirls:
        girl = {}
        for nonbase in nonbases:
            girl[nonbase['name']] = template.clone(nonbase)
        #sometraits = ['Big Boobs', 'Cool Person', 'Fast orgasms', 'Quick Learner', 'Cute', 'Strong', 'Adventurer', 'Good Kisser', 'Nymphomaniac', 'Fake orgasm expert', 'Sexy Air', 'Great Figure', 'Great Arse', 'Optimist', 'Fleet of Foot', 'Tough', 'Charismatic', 'Charming', 'Long Legs', 'Cool Scars', 'Nerd', 'Aggressive', 'Assassin', 'Nervous', 'Elegant', 'Masochist', 'Meek', 'Merciless', 'Iron Will', 'Dependant', 'Eye Patch', 'Perky Nipples', 'Clumsy', 'Lolita', 'Puffy Nipples', 'Sadistic', 'Fearless', 'Psychic', 'Strong Magic', 'Small Boobs', 'Sterile', 'Construct', 'Strange Eyes', 'Slow Learner', 'Tsundere', 'MILF', 'Twisted', 'Slow orgasms', 'Not Human', 'Yandere', 'Lesbian', 'Abnormally Large Boobs', 'Mind Fucked', 'Fragile', 'Pessimist', 'Incorporial', 'Broken Will']
        metastats = ['Name', 'Desc']
        basestats = ['Confidence', 'Constitution', 'Obedience', 'Charisma', 'Beauty', 'Libido', 'Spirit', 'Age', 'Intelligence', 'Agility']
        skillstats = ['Service', 'Magic', 'Combat']
        sexstats = ['NormalSex', 'Group', 'BDSM', 'Beastiality', 'Strip', 'Anal', 'Lesbian']
        tempstats = ['Health', 'PCHate', 'PCFear', 'PCLove', 'Tiredness', 'Happiness', 'Fame']
        ignoredstats = ['Status', 'Level', 'Exp', 'Gold', 'House', 'AskPrice', 'Mana', 'Traits']
        
        fullstats = sum([metastats, basestats, skillstats, sexstats, tempstats], [])
        for stat in fullstats:
            if stat in importedgirl:
                if not stat in girl:
                    log.warning('Could not find stat %s' % stat)
                    continue
                value = importedgirl[stat]
                if girl[stat]['valuetype'] == 'int':
                    value = int(value)
                girl[stat]['value'] = value
        girl['Traits'] = []
        if 'Traits' in importedgirl:
            girl['Traits'] = importedgirl['Traits']
        #stuff.dump('temp.yaml', girl)
        girls.append(girl)
    return girls
    
def imagefind(path):
    log.debug('Finding images')
    images = {}
    if not stuff.folderexists(path):
        log.warning('Folder not found: %s' % path)
        return images
    IMAGE_TYPES = ['anal', 'bdsm', 'beast', 'bunny', 'combat', 'death', 'ecchi', 'group', 'les', 'maid', 'mast', 'nude', 'oral', 'preg', 'profile', 'sex', 'sing', 'strip', 'titty', 'wait']
    IMAGE_TYPES.extend([ 'preg' + imagetype for imagetype in IMAGE_TYPES ])
    IMAGE_TYPES.sort(key=len, reverse=True)
    girlfolders = stuff.findfolders(path)
    templist = []
    for girlfolder in girlfolders:
        girlname = stuff.filename(girlfolder)
        images[girlname] = girlimages = {}
        imagefiles = stuff.findfiles('*.*', girlfolder)
        for imagefile in imagefiles:
            ignoredtypes = ['.db', '.txt']
            ext = stuff.fileext(imagefile)
            if ext in ignoredtypes:
                continue
            imagename = stuff.filename(imagefile, ext=False).lower()
            found = False
            for imagetype in IMAGE_TYPES:
                if imagename.startswith(imagetype):
                    if not imagetype in girlimages:
                        girlimages[imagetype] = []
                    girlimages[imagetype].append(imagefile)
                    found = True
                    break
            if not found:
                log.debug('Could not find image type for %s' % imagefile)
    return images
    

def newgame():
    basefolder = stuff.foldername(__file__)
    girldir = stuff.joinpath(basefolder, 'wmgirls')
    importedgirls = wmimport.importallgirls(girldir)
    girls = convertgirls(importedgirls, basefolder)
    images = imagefind(girldir)
    return {'girls':girls, 'images':images}

def test():
    newgame()
    #print girls

def main(argv=None):
    test()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
