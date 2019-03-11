import os



path = 'build/darknet/x64/data/obj/'
imgList = os.listdir(r'D:\Projects\Licenta\obj\img')
textFile = open('train.txt','w')
for img in imgList:
    imgPath = path+img+'\n'
    imgPath = imgPath.rstrip('\r')
    textFile.write(imgPath)
