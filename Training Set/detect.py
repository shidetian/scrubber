from PIL import Image, ImageMath, ImageOps, ImageFilter

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
    for x in range(sx / windowSize):
        res.append([])
        for y in range(sy / windowSize):
            window = im.crop((xp,yp,xp+windowSize, yp+windowSize))
            temp = ImageMath.eval("float(a)-float(b)",a=window, b=avg)
            temp2 = temp.load()
            diff = 0
            for c in range(windowSize):
                for r in range(windowSize):
                    diff+=pow(temp2[r,c],2.0)
            res[x].append(diff)
    #find average difference
    accum = 0
    for r in res:
        for i in r:
            accum+=i
    accum/=count
    
    #subtract out average
    dmax = -1.0
    dmin = 1000000000.0
    for x in range(sx/windowSize):
        for y in range(sy/windowSize):
            res[x][y]-=accum
            res[x][y] = abs(res[x][y])
#    print res
    for row in res:
        dmax = max(max(res[x]),dmax)
        dmin = min(min(res[x]),dmin)
    vis = Image.new("L", (len(res), len(res[0])), None)
    vis.putdata(res, 255/dmax, -dmin)
    vis.show()        

detectStains("2013-03-05 17.01.45.jpg", 50)
