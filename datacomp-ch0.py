import os
import re 
import requests
import json

path=os.path.abspath(os.getcwd())
#pathdir="ch4-nike"
pathdir="data"
bindir="bin"
metadir="metadata_out"
backupdir="backup"
data_dir=os.path.join(path,pathdir)
bin_dir = os.path.join(path,bindir)
meta_dir = os.path.join(path,metadir)
backup_dir = os.path.join(path,backupdir)

if not os.path.exists(bin_dir):
   os.mkdir(bin_dir)

if not os.path.exists(meta_dir):
   os.mkdir(meta_dir)

if not os.path.exists(backupdir):
   os.mkdir(backupdir)

if not os.path.exists(data_dir):
   os.mkdir(data_dir)

os.chdir(data_dir)



# %%
import shutil

# %%


# %%
import xml.etree.ElementTree as ET
def split_parse(data):
    xml_docs = data.split('<MetadataStream')

    #root_close_tag = re.search(r'</\s*MetadataStream\s*>', data)
    xmllis=[]
    for i, xml_doc in enumerate(xml_docs):
        if i == 0:
            # Skip the first element, which is not a complete XML document
            continue
        xml_doc = '<MetadataStream' + xml_doc
        #xmllis.append(xml_doc)    
        try:
            # Parse the XML document
            #root = ET.fromstring(xml_doc)
            #root=ET.parse(xml_doc)
            #root =parse(xml_doc)
            xmllis.append(xml_doc)
        except ET.ParseError as e:
            print(f'Error parsing document {i}: {e}')
    
    return xmllis

# %%
def parse2(datelis,timelis,objlis,classtyplis,classlikelis,shapexlis,shapeylis,bboxxlis,bboxylis):
    
    coordinate=[720,480]
    try:
        tree = ET.parse('checkin~.xml')
    except ET.ParseError as e:
        return datelis,timelis,objlis,classtyplis,classlikelis,shapexlis,shapeylis,bboxxlis,bboxylis
    root = tree.getroot()

    #timelis=[]
    #objlis=[]
    #classtyplis=[]
    #classlikelis=[]
    #shapexlis=[]
    #shapeylis=[]

    

    for frame in root.findall('./VideoAnalytics/Frame'):
        frametime = frame.attrib['UtcTime']
        #print('Frame UtcTime:',frametime)
        
        for obj in frame.findall('./Object'):
            objid = obj.attrib['ObjectId']
            #print('Object ObjectId:', objid)
            
            for candidate in obj.findall('./Appearance/Class/ClassCandidate'):
                
                try:
                    classtype = candidate.find('./Type').text
                except Exception as e:
                        print(e)
                        classtype=0
                
                #print('Class Type:', classtype)
                
                try:
                    classlikeli = candidate.find('./Likelihood').text
                except Exception as e:
                        print(e)
                        classlikeli=0
                    #print('Class Likelihood:', classlikeli)
                
            for shape in obj.findall('./Appearance/Shape'):
                
                try:
                    bboxl = shape.find('./BoundingBox').attrib['left']
                except Exception as e:
                        print(e)
                        bboxl=0
                
                try:
                    bboxt = shape.find('./BoundingBox').attrib['top']
                except Exception as e:
                        print(e)
                        bboxt=0
        
                try:
                    bboxr = shape.find('./BoundingBox').attrib['right']
                except Exception as e:
                        print(e)
                        bboxr=0
                
                try:
                    bboxb = shape.find('./BoundingBox').attrib['bottom']
                except Exception as e:
                        print(e)
                        bboxb=0

                try:                   
                    boxx = (float(bboxl)+float(bboxr))/2.0
                except Exception as e:
                     print(e)
                     print(bboxl)
                     print(bboxr)
                     boxx=0
                try:     
                    boxy = (float(bboxt)+float(bboxb))/2.0
                #boxy = (bboxt+bboxb)/2.0
                except Exception as e:
                     print(e)
                     print(bboxl)
                     print(bboxr)
                     boxy=0

                boxx = boxx*int(coordinate[0])
                boxy = boxy*int(coordinate[1])

                boxx = int(boxx)
                boxy = int(boxy)

                bboxxlis.append(boxx)
                bboxylis.append(boxy)

                #print('Shape BoundingBox X:', boxx)
                #print('Shape BoundingBox Y:', boxy)

                
                #print('Shape BoundingBox left:', shape.find('./BoundingBox').attrib['left'])
                #print('Shape BoundingBox top:', shape.find('./BoundingBox').attrib['top'])
                #print('Shape BoundingBox right:', shape.find('./BoundingBox').attrib['right'])
                #print('Shape BoundingBox bottom:', shape.find('./BoundingBox').attrib['bottom'])
                #print('Frame UtcTime:',frametime)
                frametime
                dt = frametime.split('T')
                date = dt[0]
                dt2 = dt[1]

                dt2 = dt2.split('.')
                time = dt2[0]#.replace(':','')
                datelis.append(date)
                timelis.append(time)

                #print('Object ObjectId:', objid)
                objlis.append(objid)
                #print('Class Type:', classtype)
                classtyplis.append(classtype)
                #print('Class Likelihood:', classlikeli)
                classlikelis.append(classlikeli)
                try:
                    shapex = shape.find('./CenterOfGravity').attrib['x']
                except Exception as e:
                        print(e)
                        shapex=0
                shapexlis.append(shapex)
                #print('Shape CenterOfGravity x:', shapex)
                try:
                    shapey = shape.find('./CenterOfGravity').attrib['y']
                except Exception as e:
                        print(e)
                        shapey=0
                shapeylis.append(shapey)
                #print('Shape CenterOfGravity y:', shapey)
    
    return datelis,timelis,objlis,classtyplis,classlikelis,shapexlis,shapeylis,bboxxlis,bboxylis


# %%
import xml.etree.ElementTree as ET

def code_run(xmllis):
        x='checkin~.xml'
        timelis=[]
        objlis=[]
        classtyplis=[]
        classlikelis=[]
        shapexlis=[]
        shapeylis=[]
        datelis=[]
        bboxxlis=[]
        bboxylis=[]

        for i in range(0,len(xmllis)):
                with open(x, 'w') as f:
                        f.write(xmllis[i])
                #parse()
                datelis,timelis,objlis,classtyplis,classlikelis,shapexlis,shapeylis,bboxxlis,bboxylis = parse2(datelis,timelis,objlis,classtyplis,classlikelis,shapexlis,shapeylis,bboxxlis,bboxylis)
                i=i+1
                
        return datelis,timelis,objlis,classtyplis,classlikelis,shapexlis,shapeylis,bboxxlis,bboxylis

# %%
import pandas as pd
import datetime as dt
def saveexl(datelis,timelis,objlis,classtyplis,classlikelis,shapexlis,shapeylis,bboxxlis,bboxylis):
    data=pd.DataFrame()
    
    data['date'] = pd.to_datetime(datelis)
    data['time'] = pd.to_datetime(timelis)
    data['Object id'] = objlis
    data['Class_type'] = classtyplis
    data['Class-likelihood'] = classlikelis
    data['X'] = bboxxlis
    data['Y'] = bboxylis
    data['date']= pd.to_datetime(data['date']).apply(lambda x: dt.datetime.strftime(x, '%d-%m-%Y'))
    data['time'] = pd.to_datetime(data['time']).apply(lambda x: dt.datetime.strftime(x, '%H%M%S'))
    #data.to_csv('niketestCONSOLI.csv'
    #data2.append(data)
    return data

# %%
#dataf2=pd.DataFrame(columns=['date','time','Object id','Class_type','Class-likelihood','X','Y',])
dataf2=[]
for files in os.listdir(data_dir):
    with open(os.path.join(data_dir,files), "r") as f:
        try:
            data=f.read()
        except UnicodeDecodeError:
            print('Unicode Error')
            data=''
    #os.remove(os.path.join(data_dir,files))
    #shutil.move()
    os.rename(os.path.join(data_dir,files),os.path.join(backup_dir,files))
    os.chdir(bin_dir)
    with open('checki.xml', 'w') as f:
                f.write(data)

    with open('checki.xml', 'r') as f:
            data = f.read()
            data = data.replace('<tt:','<')
            data = data.replace('<wsnt:','<')
            data = data.replace('</wsnt:','</')
            data = data.replace('</tt:','</')
            data = data.replace('\n','')
            data = data.replace('\t','')
            data = data.replace('\x00','')
            #xml_docs = data.split('\n')

    with open('checkin~.xml', 'w') as f:
        f.write(data)

    xmllis = split_parse(data)
    datelis,timelis,objlis,classtyplis,classlikelis,shapexlis,shapeylis,bboxxlis,bboxylis = code_run(xmllis)
    dataf = saveexl(datelis,timelis,objlis,classtyplis,classlikelis,shapexlis,shapeylis,bboxxlis,bboxylis)
    dataf2.append(dataf)


from datetime import datetime 

try:
    dataf2 = pd.concat(dataf2)
    os.chdir(meta_dir)
    now = datetime.now()
    datev=now.strftime("%d-%m-%Y")
    dataf2.to_csv('ch3-'+datev+'.csv')
    dataf2.reset_index(drop=True, inplace=True)
    d={"df":dataf2.to_json(),"tablename":"tempdata"}

    res = requests.post('https://134.122.109.38:5000/api/datadump', verify=False, json=json.dumps(d))

    if res.ok:
        print("uploaded!")
    else:
        print("error:",res)
    
except Exception as e:
     print(e)



# %%



