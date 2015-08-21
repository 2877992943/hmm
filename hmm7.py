import random
import os
import sys
import math
from numpy import *


inpath = "D://python2.7.6//MachineLearning//hmm"
filename="RenMinData2.txt"
outfile = "D://python2.7.6//MachineLearning//hmm//wordDic.txt"
outfileo = "D://python2.7.6//MachineLearning//hmm//omitProb.txt"
outfilep= "D://python2.7.6//MachineLearning//hmm//pi.txt"
outfilet= "D://python2.7.6//MachineLearning//hmm//transProb.txt"
outfile2 = "D://python2.7.6//MachineLearning//hmm//markSentence.txt"  

testDocName= "test.txt"          
result=[]

######################

def loadData():
    allMarkList=[]
    wordDic={}
    charaDic={}
    f=open(inpath+'/'+filename,'r')
    content=f.readline()
    while content:
        eachMark=[]
        
        words=content.strip('\n').split(' ');#print words##
        for eachwid in words:  ########### go through each danci'wo men'
            wid=eachwid.strip()
            if len(wid)<2:
                #print '<',wid
                continue
            
            #if wid not in wordDic.keys():
                #wordDic[wid]={}
            
            if len(wid)==2:
                #print '1',wid
                if wid not in charaDic.keys():
                    charaDic[wid]={'b':0,'m':0,'e':0,'s':0}
                charaDic[wid]['s']+=1;eachMark.append('s')
                
                    
                
            if len(wid)>2: #4 zijie   6 zijie
                #print '3', wid
                r=range(0,len(wid))[0:len(wid)-1:2];#print r
                for i in r:############go through each zi'wo' r=[0, 2, 4, 6, 8]
                    #print wid[i:i+2],i# wid[i,i+2],wid[i:i+1] not work
                    if wid[i:i+2] not in charaDic.keys():
                        charaDic[wid[i:i+2]]={'b':0,'m':0,'e':0,'s':0}
                    if i==0:
                        charaDic[wid[i:i+2]]['b']+=1;eachMark.append('b');#print 'b'
                    if i==len(wid)-2:
                        charaDic[wid[i:i+2]]['e']+=1;eachMark.append('e');#print 'e'
                    elif i!=len(wid)-2 and i!=0:  ####else not work  , one chara will be marked both b and m
                        charaDic[wid[i:i+2]]['m']+=1;eachMark.append('m');#print 'm'
            
        allMarkList.append(eachMark)
        content=f.readline()

    ###############################
    ####  output
    outPutfile=open(outfile,'w')
    for wid in charaDic.keys():
        outPutfile.write(str(wid));
        outPutfile.write(':')
        outPutfile.write(str(charaDic[wid]))
        outPutfile.write('\n')
    outPutfile.close()
    
    outPutfile=open(outfile2,'w')
    for eachM in allMarkList:
        outPutfile.write(str(eachM))
        outPutfile.write('\n')
    outPutfile.close()
    #################################
    #  pi     each state as first charact in each sentence ,count freq
    #################################
    pi={'b':0,'m':0,'e':0,'s':0}
    clas=['b','m','e','s']
    for sentence in allMarkList:
        for c in clas:
            if sentence[0]==c:
                pi[c]+=1

    #print 'pi',pi;
    sm=0 #if not initiallize sm, will warning:local variable 'sm' referenced before assignment
    for c in clas:
        sm+=float(pi[c])
    #print sm
    for (k,v) in pi.items():
        if v!=0:
            pi[k]=math.log(float(v)/sm) #v=float(pi[k])/sm #  not work v remain not divided,
        else:pi[k]=0
    #print 'pi',pi
    ############################    
    outPutfile=open(outfilep,'w')
    for (k,v) in pi.items():
        outPutfile.write(str(k));
        outPutfile.write(':')
        outPutfile.write(str(v))
        outPutfile.write(' ')
    outPutfile.close() 
    ######################################
    #  each state total count freq
    ######################################
    state={'b':0,'m':0,'e':0,'s':0}
    for sentence in allMarkList:
        for chara in sentence:
            for c in clas:
                if chara==c:
                    state[c]+=1              
    #print 'state freq',state
    
    ############################################
    #  trans prob
    ############################################
    print 'num of sentence',len(allMarkList);
    transProb={'b':{'b':0,'m':0,'e':0,'s':0},'m':{'b':0,'m':0,'e':0,'s':0},'e':{'b':0,'m':0,'e':0,'s':0},'s':{'b':0,'m':0,'e':0,'s':0}}
    for index1 in range(len(allMarkList)):
        for index2 in range(len(allMarkList[index1])):
            for si in clas:
                for sii in clas:
                    if index2+1 in range(len(allMarkList[index1])): 
                        if allMarkList[index1][index2]==si and allMarkList[index1][index2+1]==sii:
                            transProb[si][sii]+=1
    #print 'transprob',transProb
    for si in clas:
        for sii in clas:
            if transProb[si][sii]==0.0:transProb[si][sii]=0#math.log(1/float(state[si]*state[si]*state[si]))####
            else:transProb[si][sii]= math.log(float(transProb[si][sii]-1)/float(state[si]))
    ##############################
    outPutfile=open(outfilet,'w')
    for (k,v) in transProb.items():
        outPutfile.write(str(k));outPutfile.write(' ')
        for k1 in v.keys():
            outPutfile.write(str(k1));
            outPutfile.write(':');
            outPutfile.write(str(v[k1]));
            outPutfile.write(' ')
        outPutfile.write('\n')
    outPutfile.close()        
    
    #print 'transprob',transProb
            
    ############################################
    #   omit probabilistic
    ############################################
    for (k,v) in charaDic.items():
        for c in clas:
            if v[c]!=0:
                charaDic[k][c]=math.log(float(v[c])/float(state[c]))
            else:charaDic[k][c]=-100000
    
    #############################
    outPutfile=open(outfileo,'w')
    for (k,v) in charaDic.items():
        outPutfile.write(str(k));
        outPutfile.write(' ')
        for k1 in v.keys():
            outPutfile.write(str(k1));
            outPutfile.write(':');
            outPutfile.write(str(v[k1]));
            outPutfile.write(' ')
        outPutfile.write('\n')
    outPutfile.close()   
    #########################################
    
    return pi,transProb,charaDic

def loadModel():
    #load pi transprob omitprob from txt since parameter  trained for once only go through 200000sentence for once
      
    ############################pi
    pi={}
    f=open(outfilep,'r')
    content=f.readline()
    while content:
        content=content.strip('\n').split(' ');#print content   ['e:0', 's:-1.23214368129', 'b:-0.344840486292', 'm:0', '']
        for elem in content:
            if len(elem)<1:break  #######necesssary
            #print elem,elem[0]
            if elem[0] not in pi.keys():
                #print elem[2:]#elem[2:-1] last postion not included
                pi[str(elem[0])]=float(elem[2:])
        content=f.readline()
    #print pi
    ################################trans
    transProb={}
    f=open(outfilet,'r')
    content=f.readline()
    while content:
        content=content.strip('\n').split(' ');#print content   ['e:0', 's:-1.23214368129', 'b:-0.344840486292', 'm:0', '']
        for elem in content:
            if len(elem)<1:break  #######necesssary
             
            if len(elem)==1:
                if elem not in transProb.keys():
                    #print elem[2:]#elem[2:-1] last postion not included
                    transProb[elem]={}
            if len(elem)>1:
                if elem[0] not in transProb[content[0]]:
                    transProb[content[0]][elem[0]]=float(elem[2:])
        content=f.readline()
    #print transProb
    ################################omitprob
    omitProb={}
    f=open(outfileo,'r')
    content=f.readline()
    while content:
        content=content.strip('\n').split(' ');#print content   ['e:0', 's:-1.23214368129', 'b:-0.344840486292', 'm:0', '']
        for elem in content:
            if len(elem)<1:break  #######necesssary
             
            if len(elem)==2:
                if elem not in transProb.keys():
                    #print elem[2:]    #if elem[2:-1] last postion not included
                    omitProb[elem]={}
            if len(elem)>2:
                if elem[0] not in omitProb[content[0]]:
                    omitProb[content[0]][elem[0]]=float(elem[2:])
        content=f.readline()
    #################################
    print 'finish load'
    return pi,transProb,omitProb
    
    
    
    


def normalize(pi,transProb,omitProb):
    clas=['b','m','e','s'];s=0.0
    ####################
    #pi
    ####################
    for c in clas:
        s=pi[c]*pi[c]+s
    s=math.sqrt(s)
    for c in clas:
        pi[c]=float(pi[c]/s)
    #print 'pi',pi
    ############################    
    outPutfile=open(outfilep,'w')
    for (k,v) in pi.items():
        outPutfile.write(str(k));
        outPutfile.write(':')
        outPutfile.write(str(v))
        outPutfile.write(' ')
    outPutfile.close() 
    ###############################
    #transprob
    ###############################
    for c in clas:
        for cc in clas:
            s=transProb[c][cc]*transProb[c][cc]+s
        s=math.sqrt(s)
        for cc in clas:
            transProb[c][cc]/=s
    #print 'transprob',transProb
    ############################
    outPutfile=open(outfilet,'w')
    for (k,v) in transProb.items():
        outPutfile.write(str(k));outPutfile.write(' ')
        for k1 in v.keys():
            outPutfile.write(str(k1));
            outPutfile.write(':');
            outPutfile.write(str(v[k1]));
            outPutfile.write(' ')
        outPutfile.write('\n')
    outPutfile.close()      
    ##################################
    #omitprob
    #################################
    for (k,v) in omitProb.items():
        for c in clas:
            s=v[c]*v[c]+s
        s=math.sqrt(s)
        for c in clas:
            omitProb[k][c]=omitProb[k][c]/s
    ############################
    outPutfile=open(outfileo,'w')
    for (k,v) in omitProb.items():
        outPutfile.write(str(k));
        outPutfile.write(' ')
        for k1 in v.keys():
            outPutfile.write(str(k1));
            outPutfile.write(':');
            outPutfile.write(str(v[k1]));
            outPutfile.write(' ')
        outPutfile.write('\n')
    outPutfile.close()
    ##################

    return pi,transProb,omitProb
    
        
        
    



    

def test(omitProb):
    result=[];omitProb1=[]
    f=open(inpath+'/'+testDocName,'r')
    content=f.readline()
    while content:
        content=content.strip('\n');#print content,len(content)#
    
        n=range(len(content))[::2];#print n #[0, 2, 4, 6] len=8
     
        for i in n:
            omitProb1.append(omitProb[content[i:i+2]])
            result.append(0)
        content=f.readline()  #without this doc cannot close
    return omitProb1,result,len(result)




######################total failue  
def seekAllPath(omitProb1,pi,transProb):
    #print'seekbestpath' #### track the flow /change of t
    st1List=['b','m','e','s'];scoreMin=inf;scoreMin0=inf;  #in pursuit of prob max, seek min
    
    tt=len(omitProb1)
    pathRecord={}
    for i in range(tt):
        pathRecord[i]=[]
    #print pathRecord    #not work when di gui call function itself
        
    for t in range(tt): #tt=4   [0 1 2 3]
        if t==1:
            for st1 in st1List:
                #print 'st1',st1
                #scoreMin=inf###wrong if not locate here
                scoreDic=initialDic
                for st in st1List:
                    if transProb[st][st1]!=0 and scoreDic[st]!=0:
                        s=scoreDic[st]+transProb[st][st1]+omitProb1[t][st1]; 
                        pathi=[]
                        pathi.append(st);pathi.append(st1);pathi.append(s);
                        pathRecord[t].append(pathi)
                        #print 't 1', st+'->'+st1 ,s
            #print 't 1',pathRecord

        if t>=2 and t!=tt-1:
            #scoreDic=seekBestPath(omitProb1,pi,transProb,t-1);print'1',t,scoreDic  #di gui not work
            for st1 in range(len(st1List)):
                #scoreMin=inf###always forget to reset the  value to compare 
                for st in range(len(st1List)):   #[0 1 2 3]
                    if transProb[st1List[st]][st1List[st1]]!=0:
                        s=scoreDic[st1List[st]]+transProb[st1List[st]][st1List[st1]]+omitProb1[t][st1List[st1]];#print '2', transProb[st1List[st]][st1List[st1]],s,st1List[st],st1List[st1] 
                        #print  st1List[st]+'->'+st1List[st1],s
                        pathi=[]
                        pathi.append(st1List[st]);pathi.append(st1List[st1]);pathi.append(s);
                        pathRecord[t].append(pathi)
            #print 't 2345...',pathRecord

        if t==tt-1:
            for st1 in range(len(st1List)):
                for st in range(len(st1List)):   #[0 1 2 3]
                    if transProb[st1List[st]][st1List[st1]]!=0 and st1List[st1] not in ['m','b']:
                        s=scoreDic[st1List[st]]+transProb[st1List[st]][st1List[st1]]+omitProb1[t][st1List[st1]];#print '2', transProb[st1List[st]][st1List[st1]],s,st1List[st],st1List[st1] 
                        #print st1List[st]+'->'+st1List[st1],s
                        pathi=[]
                        pathi.append(st1List[st]);pathi.append(st1List[st1]);pathi.append(s);
                        pathRecord[t].append(pathi)
            #print 't 2345...',pathRecord
            

        if t==0:
            initialDic={'b':0,'m':0,'e':0,'s':0}
            for s in st1List:
                if pi[s]!=0:
                    initialDic[s]=float(pi[s]+omitProb1[0][s])
            pathRecord[t].append(initialDic)
            #print 't 0',pathRecord

    return pathRecord

    
def judge(pi,transProb,omitProb1):
    clas=['b','m','e','s'];score={'b':0,'m':0,'e':0,'s':0}; s=0
    numChara=len(omitProb1)
    for t in range(numChara):  # 3 char 0 1 2
        if t==1:
            for s1 in clas:
                for s0 in ['s','b']:
                    if transProb[s0][s1]!=0:
                        score[s1]=omitProb1[t-1][s0]+omitProb1[t][s1]+pi[s0]+transProb[s0][s1]   #score[s0] wrong
                print '0',score
        if t>=2 and t!=numChara-1:
            for s1 in clas:
                tempMax=None
                for s0 in clas:
                    if transProb[s0][s1]!=0:
                        s=score[s0]+transProb[s0][s1]#+omitProb1[t][s1]        
                    if transProb[s0][s1]!=0 and(s>tempMax or tempMax==None):#transProb[s0][s1]!=0 without this, s0=b will go into this 'if'  
                        tempMax=s   #when s0==b, tempmax=0 is max
                        maxState=s0
                score[s1]=tempMax+omitProb1[t][s1]
                print maxState,'->',s1,score[s1],tempMax,omitProb1[t][s1]
        if t==numChara-1:
            for s1 in ['s','e']:
                tempMax=None
                for s0 in clas:
                    if transProb[s0][s1]!=0:
                        s=score[s0]+transProb[s0][s1]#+omitProb1[t][s1]
                    if transProb[s0][s1]!=0 and(s>tempMax or tempMax==None):
                        tempMax=s
                        maxState=s0
                score[s1]=tempMax+omitProb1[t][s1]
                print maxState,'->',s1,score[s1]
    
######main
#pi,transProb,omitProb=loadData() # go through 200000000doc only once,train to get parameter
#pi,transProb,omitProb=normalize(pi,transProb,omitProb)

pi,transProb,omitProb=loadModel() 

omitProb1,result,lenSentence=test(omitProb)

pathRecord=seekAllPath(omitProb1,pi,transProb)
print pathRecord
judge(pi,transProb,omitProb1)
        
        
    
    
    







    
    
