import cv2
import os

def getVideoFrames(basepath):
#    img_lst = []        # store image matrices in list
#    
#    for entry in os.listdir(basepath):      # lists all images
#        file_path = os.path.join(basepath,entry)
#        if os.path.isfile(file_path):       # checks if file exists
#            img = cv2.imread(file_path)   # 0 means greyscale
#            img_lst.append(img)
#    return(img_lst)
    
    images = []
    files = os.listdir(folder)
    files = natsort.natsorted(files)
    for filename in files:
        img = cv2.imread(os.path.join(folder,filename), 1)
        img = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
        if img is not None:
            images.append(img)
    return images

basepath = "/home/burhan/Vision Group/MAV_course/AE4317_2019_datasets/cyberzoo_poles_panels_mats/20190121-142935" #basepath for seperate images from sim
#basepath = os.path.join(basepath, os.listdir(basepath)[0])
e1 = cv2.getTickCount()     # number of clock cycles
img_lst = getVideoFrames(basepath)

N = len(img_lst)

w,h = 240,520

step_number = 5

steps = int(h/step_number)

count_lst = []

for i in range(N):
    green = cv2.split(img_lst[i])[1]
    _, thres = cv2.threshold(green,75,255,cv2.THRESH_TOZERO)
    filtered_img = cv2.bitwise_and(green, green, mask = thres)
    for i in range(step_number):      # slices of image to count
        slice = thres[(i*steps):((i+1)*steps)]
        count = cv2.countNonZero(slice)
        count_lst.append(count)
    print(count_lst)
    #print(green[400])
    cv2.imshow("image",filtered_img)
    k = cv2.waitKey(0)
    #if k==27:
        #break
cv2.destroyAllWindows()
    


