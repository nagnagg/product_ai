import xml.etree.ElementTree as ET
from os import getcwd
import sys,os
sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["bns-v","btk","hsr","srg","bnk","dsp","sdan-v","hcr","gsr","hdr","lm guide","hand"]

if len(sys.argv) > 1:
    classes = sys.argv[1:]

with open('model_data/voc_classes.txt','w') as f:
    f.write('\n'.join(classes))


def convert_annotation(year, image_id, list_file):
    in_file = open('VOCDevkit/VOC%s/Annotations/%s.xml'%(year, image_id.replace(".jpg","")))
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(float(xmlbox.find('xmin').text)),
             int(float(xmlbox.find('ymin').text)),
             int(float(xmlbox.find('xmax').text)),
             int(float(xmlbox.find('ymax').text)))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

wd = getcwd()

for year, image_set in sets:
    image_ids = open('VOCDevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
    list_file = open('model_data/%s_%s.txt'%(year, image_set), 'w')
    for image_id in image_ids:
        if image_id == '1': continue
        if image_id == '-1': continue
        image_file_path = '%s/VOCDevkit/VOC%s/JPEGImages/%s'%(wd, year, image_id)
        list_file.write(image_file_path)
        convert_annotation(year, image_id, list_file)
        list_file.write('\n')
    list_file.close()
