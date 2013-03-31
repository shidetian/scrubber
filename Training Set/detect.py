from PIL import Image, ImageMath, ImageOps, ImageFilter
import sys

def loadImage(fname):
    return Image.open(fname)

def detectStains(fname, windowSize=50):
    im = loadImage(fname)
    im = ImageOps.equalize(im)
    #im = im.filter(ImageFilter.BLUR)
    sx, sy = im.size
    
    #first find average of all windows
    count = 0.0
    temp = None
    for x in range(sx / windowSize):
        for y in range(sy / windowSize):
            count+=1
            xp = x*windowSize
            yp = y*windowSize
            window = im.crop((xp,yp,xp+windowSize, yp+windowSize))
            if temp==None:
                window.load()
                temp = window
            else:
                temp = ImageMath.eval("float(a)+float(b)", a=temp, b=window)
    temp2 = temp.load()
    for x in range(windowSize):
        for y in range(windowSize):
            temp2[x,y]/=count
    #temp.show()
    avg = temp
    #raw_input("")
    
    """Basic difference method: subtract out each window with average window, then
    filter by average difference"""
    res = []
    for y in range(sx / windowSize):
        #res.append([])
        for x in range(sy / windowSize):
            xp = x*windowSize
            yp = y*windowSize
            window = im.crop((xp,yp,xp+windowSize, yp+windowSize))
            #window.show()
            #raw_input("")
            temp = ImageMath.eval("float(a)-float(b)",a=window, b=avg)
            temp2 = temp.load()
            diff = 0
            for c in range(windowSize):
                for r in range(windowSize):
                    diff+=pow(temp2[r,c],2.0)
            #res[x].append(diff)
            res.append(diff)
    #find average difference
    accum = 0
    accum = sum(res)
    """for r in res:
        for i in r:
            accum+=i"""
    accum/=count
    
    #subtract out average
    dmax = -1.0
    dmin = 1000000000.0
    for x in range(sx/windowSize):
        for y in range(sy/windowSize):
            res[x+y*(sx/windowSize)]-=accum
            res[x+y*(sx/windowSize)] = abs(res[x+y*(sx/windowSize)])
    #print res
    """for row in res:
        #print dmax,dmin
        dmax = max(max(row),dmax)
        dmin = min(min(row),dmin)"""
    dmax = max(res)
    dmin = min(res)
    vis = Image.new("L", (sx/windowSize, sy/windowSize), None)
    temp = dmax-dmin
    if temp==0:
        temprange =0
    else:
        temprange = 255/temp
    #print res
    print "dmin",dmin
    print "dmax",dmax
    print "max",temprange
    print len(res)
    vis.putdata(res, temprange, -dmin*(255/(-dmin+dmax)))
    temp = vis.load()
    """for x in range(sx/windowSize):
        for y in range(sx/windowSize):
            print sys.stdout.write(str(temp[x,y])+" ")
        print ' '"""
    vis.show()        

detectStains("2013-03-12 16.44.49.jpg", 50)