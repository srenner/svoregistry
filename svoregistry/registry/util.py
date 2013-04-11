import urllib2

def geocode(city, state, country, zip):
    
    if zip.len() > 0:
        pass
    
    address="1600+Amphitheatre+Parkway,+Mountain+View,+CA"
    url="http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % address

    response = urllib2.urlopen(url)
    jsongeocode = response.read()