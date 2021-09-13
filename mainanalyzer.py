import os
import matplotlib.pyplot as plt
import random
import matplotlib.colors as mcolors
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
from os import path


def count_days(day,mon,year):
    if (year%4==0 and year%100!=0) or year%400==0:#for feb
        x=29#if leap yr
    else:
        x=28
    dict_days={1:31,2:x,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
    arr_days=[31,x,31,30,31,30,31,31,30,31,30,31]
    for i in range(1,len(arr_days)):
        arr_days[i]+=arr_days[i-1]#cumulative no of days till present month
    if mon!=1:
        return day+arr_days[mon-2]#to count the no of days from beg of year
    else:
        return day#if 1st month only then day count==day

def create_lists(f):
    k=[]
    admins=set()
    timestamp=[]  # '-' splitted
    msglog=[]     # '-' splitted
    date=[]       # ',' splitted
    time=[]       # ',' splitted
    dates={}
    for i in f.readlines():
        k.append(i.split('-'))

    for i in k:
        if(len(i)>=2):
            if i[0].count('/')==2 and i[0].count(',')!=0:#i[0] is date and time
                #timestamp.append(i[0])
                temp=''
                for j in range(1,len(i)):
                    temp+=i[j]#i[1]-->name and msg
                if temp.find(':')!=-1:
                    msglog.append(temp)
                    timestamp.append(i[0])#only if : is found then the timestamp is added 
                elif temp.find('added')!=-1:#for grp
                    admins.add(temp[:temp.find('added')])#all names with "added" next to them are added to admins
                elif temp.find('created')!=-1:#for grp
                    admins.add(temp[:temp.find('created')])#all names with "created" next to them are added to admins
            else:
                temp=''
                temp+=msglog[len(msglog)-1]
                temp+='\n'+i[0]
                msglog[len(msglog)-1]=temp
        else:
            temp=''
            temp+=msglog[len(msglog)-1]
            temp+='\n'+i[0]
            msglog[len(msglog)-1]=temp

    for i in timestamp:
        temp=i.split(',')
        date.append(temp[0])
        time.append(temp[1])

    for i in date:#to count the number of times a date occurs in the timestamp or chat
        if dates.get(i,-1)==-1:
            dates[i]=0  
        dates[i]+=1
    return date,dates,msglog,admins


#MOST ACTIVE DAY AND NUMBER OF MESSAGES ON THAT DATE/DAY
def most_active_day(dates,months):
    o=0
    for key in dates:
        if o==0:
            m_dates=key
            o+=1
            continue
        if dates[key]>dates[m_dates]:
            m_dates=key
    t=m_dates.split('/')
    most_active_day=t[0]+' '+months[int(t[1])]+' '+t[2]
    return m_dates,most_active_day

def most_active_month(date,months):
    day=[]
    month=[]
    year=[]
    for i in date:
        temp=i.split('/')
        day.append(int(temp[0]))
        month.append(int(temp[1]))
        year.append(int(temp[2]))

    mon_cnt=[]
    for i in range(1,13):
        mon_cnt.append(0)
    for i in month:
        mon_cnt[i-1]+=1
    max_month_msg=max(mon_cnt)
    max_month=mon_cnt.index(max_month_msg)+1
    return max_month,max_month_msg


#Plot no of messages per day
def plt_num_msgsperday(date):
    plt.clf()
    days=[0]*367
    for i in range(len(days)):
        days[i]=i+1
    arr_plot=[]
    i=0
    while i<len(date):
        start=date[i].split('/')[2]#start contains the starting year of chat
        temp=[0]*367
        while i<len(date) and date[i].split('/')[2]==start:# and i<len(date):
            d,m,y=[int(k) for k in date[i].split('/')]
            temp[count_days(d,m,y)]+=1
            i+=1

        arr_plot.append(temp)
    lbl=1
    for i in arr_plot:
        plt.plot(days,i,label=str(lbl)+' year')
        lbl+=1
    plt.xlabel('Day in year (out of 365/366)')
    plt.ylabel('No. of messages')
    plt.title('No. of messages each day')
    plt.legend()
    plt.savefig('static//images//plot1.png')
    # plt.show()


##COUNT THE NUMBER OF USERS IN THE CHAT
def num_users(msglog):
    users=set() #to store phoneno. name
    users_cnt={}     #   string--->list.....phoneno/name--->list of its messages
    for i in msglog:
        name=''
        ind=i.index(':')
        name+=i[:ind]
        users.add(name.strip)
        if users_cnt.get(name,-1)==-1:
            users_cnt[name]=[]
        users_cnt[name].append(i[ind+1:])
    return users_cnt

##FIND THE MOST ACTIVE USER IN THE CHAT
def most_active_user(users_cnt):
    nmsg=-1
    mxuser='-1'
    for key in users_cnt:
        if len(users_cnt[key])>nmsg:
            mxuser=key
            nmsg=len(users_cnt[key])

    return mxuser,nmsg

def plot_num_msgs_per_user(users_cnt):
    
    plt.clf()
    nmsg_per_user={}
    for key, values in users_cnt.items():
            nmsg_per_user[key] = len(values)  
    sorted_users_cnt=sorted(nmsg_per_user,key=nmsg_per_user.__getitem__,reverse=True)
    
    top_users=[]
    
    cols = random.choices(list(mcolors.CSS4_COLORS.values()),k = 5)
    if len(sorted_users_cnt)<5:
        n=len(sorted_users_cnt)
    else:
        n=5
    for i in range(n):
        top_users.append([sorted_users_cnt[i],nmsg_per_user[sorted_users_cnt[i]]])  # [user,no. of msg by him/her]

    #explode can be also added as a parameter
    plt.pie([i[1] for i in top_users], labels=[i[0] for i in top_users],colors=cols, startangle=90, shadow=True, autopct='%1.1f%%')
    plt.title('Top Active Users')
    plt.legend(loc=(.65,-0.12))
    plt.savefig('static//images//plot2.png')
    # plt.show()



def create_word_dict(users_cnt):
    word_dict={}
    chars=['.','/','"',';',':','=','+','-','*','!','@','#','&',',','?','<','>','(',')','[',']','{','}','^','%','$','_','|']
    for key in users_cnt:
        for i in users_cnt[key]:# i iterates over messages!
            temp=i.split()#temp is list of unfiltered-words in msg!
            for j in range(len(temp)): # filter ./'";:=+-*!@#&,?<>()[]{}^%$
                temp2=list(temp[j])#temp[j]is a word!
                for ch in chars:
                    while True:
                        if ch in temp2:
                            temp2.remove(ch)
                        else:
                            break
                st=''
                for h in temp2:
                    st+=h
                temp[j]=st#after removing chars the letters are combined againto form list of words
                #print(temp[j])
            for word in temp:
                if word_dict.get(word,-1)==-1:
                    word_dict[word]=1
                else:
                    word_dict[word]+=1
    return word_dict
                

#find the word occured most of the times
def most_occured_word(word_dict):
    best_word_cnt=0
    for i in word_dict:
        if word_dict[i]>best_word_cnt:
            best_word_cnt=word_dict[i]
            best_word=i
    return best_word,best_word_cnt

def create_time_dict(file):
    g = open(file,encoding="utf8")
    d1={}
    for i in g.readlines():
        j=i.split("-")[0]
        j=j.split(",")
        if len(j)==2:
            if j[0].count('/')==2:
                time1=j[1].split()
                time2=time1[0].split(':')
                if j[0] not in d1:
                    d1[j[0]]={}

                    if not time2[0] in d1[j[0]]:
                        d1[j[0]][time2[0]] = 1
                    else:
                        d1[j[0]][time2[0]] += 1
                else:
                    if not time2[0] in d1[j[0]]:
                        d1[j[0]][time2[0]] = 1
                    else:
                        d1[j[0]][time2[0]] += 1

    for i in d1:
        for j in range(0,25):
            j=str(j)
            if j in d1[i]:
                continue
            else:
                d1[i][j] = 0
    g.close()
    return d1


#MOST ACTIVE TIME OF A PARTICULAR DAY
def most_active_time(date,d1):
    plt.clf()
    if date not in d1:
        return
    ti=[]
    li=[]
    for i in range(5):
        i=str(i)
        ti.append(i)
        li.append(d1[date][i])
    plt.bar(ti,li,label='Night',color='k')
    ti=[]
    li=[]
    for i in range(5,12):
        i=str(i)
        ti.append(i)
        li.append(d1[date][i])
    plt.bar(ti,li,label='Morning',color='c')
    ti=[]
    li=[]
    for i in range(12,17):
        i=str(i)
        ti.append(i)
        li.append(d1[date][i])
    plt.bar(ti,li,label='Afternoon',color='#FFD700')
    ti=[]
    li=[]
    for i in range(17,21):
        i=str(i)
        ti.append(i)
        li.append(d1[date][i])
    plt.bar(ti,li,label='Evening',color='#FF7F50')
    ti=[]
    li=[]
    for i in range(21,24):
        i=str(i)
        ti.append(i)
        li.append(d1[date][i])
    plt.bar(ti,li,color='k')
    plt.xlabel('time')
    plt.ylabel('no of messages')
    plt.title('MOST ACTIVE TIME\nOF '+date)
    plt.legend()
    #plt.savefig('static//images//plot3.png')
    # plt.show()


def upload(file):
    with open(file, "r+",encoding="utf8") as f:
    #f = file.decode('UTF-8')
        months={1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
        results=[]
        date,dates,msglog,admins=create_lists(f)
        m_dates,active_day = most_active_day(dates,months)
        max_month,max_month_msg = most_active_month(date,months)
        max_month,max_month_msg = most_active_month(date,months)
        
        plt_num_msgsperday(date)
        #   fig1.show()
        users_cnt=num_users(msglog)
        participants=[]
        for i in users_cnt:
            participants.append(i)
        mxuser,nmsg = most_active_user(users_cnt)
        if len(admins)==0:
            group_chat=False
        else:
            group_chat=True
        
        plot_num_msgs_per_user(users_cnt)
        # fig2.show()
        word_dict=create_word_dict(users_cnt)
        best_word,best_word_cnt = most_occured_word(word_dict)
        time_dict=create_time_dict(file)
        a=random.randint(1,30)
        b=random.randint(1,12)
        yr=[2019,2020]
        c=random.choice(yr)
        input_date=str(a)+"/"+str(b)+"/"+str(c)
        #most_active_time(input_date,time_dict)
        # if fig3!=None:
        #     fig3.show()

        # x=input("Enter something!")
        res_dict={"Most active date":active_day,"Number of messages on the most active day":dates[m_dates],"Most active month":months[max_month],
            "Number of messages in the most active month":max_month_msg,"Number of participants":len(users_cnt),"Most active user":mxuser,
            "Number of messages by the most active user":nmsg,"Group Chat":group_chat,"Most used word":best_word,"Most used word count":best_word_cnt,}
        # res_dict={"Most active date":active_day,"Number of messages on the most active day":dates[m_dates],"Most active month":months[max_month],
        #     "Number of messages in the most active month":max_month_msg,"Number of participants":users_cnt,"Participants":participants,"Most active user":mxuser,
        #     "Number of messages by the most active user":nmsg,"Group Chat":group_chat,"Admins":admins,"Most used word":best_word,"Most used word count":best_word_cnt,}
        # results.append(res_dict)
    f.close()
    return res_dict


# upload("C:/Users/Admin/Desktop/Tanisha-p/Chat2.txt")  
# print(jsonres)
# fig1.show()
# fig2.show()
# if fig3!=None:
#     fig3.show()
