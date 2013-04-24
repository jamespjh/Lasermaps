import geopy
import yaml
import os
import sys
import urllib2
import urllib
import argparse

class Lasermap(object):
    def __init__(self,location,zoom=16,size=1200,outfile=None):
        self.zoom=zoom
        self.location=location
        self.size=size
        here=os.path.dirname(__file__)
        try:
            self.config=yaml.load(open(os.path.expanduser(os.path.join("~",".lasermaps",'config.yml'))))
        except:
            self.config=yaml.load(open(os.path.join(here,'config.yml')))
        if outfile is None:
            self.outfile='result.png'
        else:
            self.outfile=outfile
        self.result=open(self.outfile,'w')
        self.geocoder=geopy.geocoders.GoogleV3(domain="maps.google.co.uk")
        self.geocode()

    def geocode(self):
        print "Decoding %s"%self.location
        self.place,(self.latitude,self.longitude)=self.geocoder.geocode(self.location)
    
    def requesturl(self):
        request=urllib.urlencode(dict(
         size='%sx%s'%(self.size,self.size),
         center='%s,%s'%(self.latitude,self.longitude),
         zoom=self.zoom,
         sensor="false",
         maptype='roadmap',
         key=self.config['key']))
        return "http://maps.googleapis.com/maps/api/staticmap?%s"%request
        
    def getimage(self):
        return urllib2.urlopen(self.requesturl())

    def writeresult(self):
        self.result.write(self.getimage().read())
        
def main():
    sys.argv=sys.argv[1:]
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument("--size", help="Image Size")
    parser.add_argument("--zoom", help="Zoom Level")
    parser.add_argument("--outfile", help="Output Filename")
    parser.add_argument("location",help="Centre of map")
    options,extra = parser.parse_known_args(sys.argv)
    print options,extra 
    lasermap=Lasermap(**vars(options))
    lasermap.writeresult()

if __name__ == '__main__':
    main()

