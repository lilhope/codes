#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Create data for 2D object detection algorithm
@author: genonova
"""
import numpy as np
import pandas as pd
import cv2
import os

from glob import glob


def create_data(img_dir,label_path,dst_path):
    """create data for 2d object detection algorithm"""
    patient_ids = os.listdir(img_dir)
    for patient_id in patient_ids:
        img_path = os.path.join(img_dir,patient_id)
        img_paths = glob(img_path + '/*_i.png')
        img_paths.sort()
        images = [cv2.imread(img_path,cv2.IMREAD_GRAYSCALE) for img_path in img_paths]
        if len(images)==0:
            print(patient_id)
        try:
            images = [im.reshape((1,) + im.shape) for im in images]
        except:
            print(patient_id)
        res = np.vstack(images)
        label_path = os.path.join(label_path,patient_id+'.csv')
        if not os.path.exists(label_path):
            print("cant find annotation files")
            continue
            
        print('find annoation label files.')
        labels = pd.read_csv(label_path)
        #get the bounding box record
        lab = process_label(labels,res)
        labf = [[] for _ in xrange(len(lab))]
        labl = [[] for _ in range(len(lab))]
        for ilab in xrange(len(lab)):
            h = lab[ilab][5] - lab[ilab][2]
            labf[ilab] = np.round(lab[ilab][2] + 0.2 * h)
            labl[ilab] = np.round(lab[ilab][2] + 0.8 * h)
        for islice in xrange(1,res.shape[0]-1):
            cr_img = 0
            cr_xml = 0
            for j in xrange(len(lab)):
                if(islice >= labf[j]) and (islice <= labl[j]):
                    print('creat detection files')
                    if cr_img == 0:
                        img = np.dstack((res[islice-1,:,:],res[islice,:,:],res[islice+1,:,:]))
                        print(img.shape)
                        cv2.imwrite(dst_path+'/JPEGImages/' + str(patient_id) + '_'+str(islice) + '.jpg',img)
                        cr_img = 1
                    if cr_xml == 0:
                        fid = open(dst_path+'/Annotations/' + str(patient_id) + '_' + str(islice) +'.xml','w')
                        print >> fid,'<annoation>\n'
                        print >> fid,'\t<size>\n'
                        print >> fid,'\t\t<width>',res.shape[2],'</width>\n'
                        print >> fid,'\t\t<height>',res.shape[1],'</height>\n'
                        print >> fid,'\t\t<depth>3</depth>\n'
                        print >> fid,'\t</size>\n'
                        print >> fid,'\t<object>\n'
                        print >> fid,'\t\t<name>nodule</name>\n'
                        print >> fid,'\t\t<diffcult>0</diffcult>\n'
                        print >> fid,'\t\t<bndbox>\n'
                        print >> fid,'\t\t\t<xmin>',int(np.round(lab[j][0])),'</xmin>\n'
                        print >> fid,'\t\t\t<ymin>',int(np.round(lab[j][1])),'</ymin>\n'
                        print >> fid,'\t\t\t<xmax>',int(np.round(lab[j][3])),'</xmax>\n'
                        print >> fid,'\t\t\t<ymax>',int(np.round(lab[j][4])),'</ymax>\n'
                        print >> fid,'\t\t</bndbox>\n'
                        print >> fid,'\t</object>\n'
                        cr_xml = 1
                    else:
                        print >> fid,'\t<object>\n'
                        print >> fid,'\t\t<name><nodule></name>\n'
                        print >> fid,'\t\t<diffcult>0</diffcult>\n'
                        print >> fid,'\t\t<bndbox>\n'
                        print >> fid,'\t\t\t\<xmin>',int(np.round(lab[j][0])),'</xmin>\n'
                        print >> fid,'\t\t\t<ymin>',int(np.round(lab[j][1])),'</ymin>\n'
                        print >> fid,'\t\t\t<xmax>',int(np.round(lab[j][3])),'</xmax>\n'
                        print >> fid,'\t\t\t<ymax>',int(np.round(lab[j][4])),'</ymax>\n'
                        print >> fid,'\t\t</bndbox>\n'
                        print >> fid,'\t</object>\n'
                if cr_xml:
                    print >> fid,'</annoation>\n'
                    fid.close()
            
            
def process_label(labels,imgs):
    depth,height,width = imgs.shape
    recs = list()
    for index,row in labels.iterrows():
        x1 = int((row['x'] - row['d']) * width)
        y1 = int((row['y'] - row['d']) * height)
        z1 = int((row['z'] - row['d']) * depth)
        x2 = int((row['x'] + row['d']) * width)
        y2 = int((row['y'] + row['d']) * height)
        z2 = int((row['z'] + row['d']) * depth)
        recs.append([x1,y1,z1,x2,y2,z2])
    return recs
        
if __name__ == "__main__":
    img_path = "/home/genonova/ndsb3_images"
    label_path = '/home/genonova/resources/ndsb3_manual_labels'
    dst_path = '/home/genonova/data'
    create_data(img_path,label_path,dst_path)
        
        
        
        
        
    

