import sys

import kivy
kivy.require('1.0.6')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, DictProperty, ListProperty, StringProperty, NumericProperty

import log, stuff
import hmdx


class GirlEditApp(App):

    def build(self):
        gamedata = hmdx.newgame()
        gamedata['girlnames'] = girlnames = []
        girls = gamedata['girls']
        stuff.dump('temp.yaml', girls)
        for girl in girls:
            if 'Name' in girl:
                girlnames.append(girl['Name']['value'])
        girlnames.sort()
        gamedata['currentgirlname'] = girlnames[0]
        return Editor(**gamedata)
        
class Editor(BoxLayout):
    girls = ListProperty()
    images = DictProperty()
    girlnames = ListProperty()
    currentgirlname = StringProperty()
    
class GirlImage(Image):
    images = DictProperty()
    categories = ListProperty()
    category = StringProperty()
    image = StringProperty()
    index = 0
    
    def loadimages(self, girlname, source):
        self.image = ''
        images = source.get(girlname)
        if not images:
            return []
        categories = list(images.keys())
        categories.sort()
        self.categories = categories
        self.category = self.categories[0]
        self.index = 0
        self.image = images[self.category][self.index]
        return images
        
    def next(self):
        self.move(1)
        
    def last(self):
        self.move(-1)
        
    def move(self, change):
        newindex = self.index + change
        if newindex < 0 or newindex >= len(self.images[self.category]):
            self.index = 0
            categoryindex = self.categories.index(self.category)
            categoryindex = (categoryindex + change) % len(self.categories)
            self.category = self.categories[categoryindex]
            if change < 1:
                self.index = len(self.images[self.category]) - 1
        else:
            self.index = newindex
        self.image = self.images[self.category][self.index]
            
    def setcategory(self, newcategory):
        if newcategory in self.images:
            self.category = newcategory
        else:
            self.category = self.images.keys()[0]
        self.index = 0
        self.image = self.images[self.category][self.index]
        

def main(argv=None):
    GirlEditApp().run()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
