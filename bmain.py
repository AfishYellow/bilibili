import requests
import re
import os
import sys
import json
from tkinter.messagebox import *
import tkinter as tk
import time


module_path2 = os.path.dirname(os.path.realpath(sys.argv[0]))
secondpath = '\\date\\'

def writefile(str,filename):
    path = module_path2+secondpath+filename
    f = open(path,'w')
    f.write(str)
    f.close()
def writedic(dic,filename):
    path = module_path2 + secondpath + filename
    f = open(path,'w+')
    js = json.dumps(dic)
    f.write(js)
    f.close()
def readfile(filename):
    path = module_path2 + secondpath + filename
    try:
        f = open(path,'r')
    except FileNotFoundError:
        open(path,'w+')
        f = open(path, 'r')
        print("e")
    return f.read()
def readdic(filename):
    path = module_path2 + secondpath + filename
    f = open(path,'r')
    js = f.read()
    dic = json.loads(js)
    f.close()
    return  dic

percent  = '0%'
def save_html(url):
    '''
    url:对应视频的url链接
    保存对应视频的html源码文件
    '''
    res = requests.get(url)
    res.encoding = "utf-8"
    name = url.split('/')[-1]
    with open("{}.html".format(name),"w", encoding='utf-8') as fp:
        fp.write(res.text)
 
def handel_data(file, start=1,startPlan=1,endPlan=-1):
    '''
    file: html文件
    start: 选集起始 默认为第1集
    end: 选集结束 默认为最后1集
    '''
    with open("{}".format(file),"r",encoding="utf-8") as fp:
        data = fp.read()
    # print(data)
    # 得到播放列表所有选集信息
    pageList = re.findall(r"<script>window.__INITIAL_STATE__=(.*?)</script>",data,re.MULTILINE)
 
    # 得到page part duration 对应选集集数 选集名字 选集时长(second)
    try:
        pages = re.findall(r'{"cid":.*?,"page":(.*?),"from":"vupload","part":(.*?),"duration":(\d*),"vid":.*?,"weblink":.*?,"dimension":.*?}', pageList[0])
    except IndexError:
        tk.messagebox.showinfo(message='bv号输入有误')
        return
    # if endPlan == -1:
    #     total_seconds = sum(int(page[-1]) for page in pages[start-1:start]) + int(pages[-1][-1])
    # else:
    total_seconds = sum(int(page[-1]) for page in pages[startPlan-1:start])

    if endPlan == -1:
        total_seconds_plan = sum(int(page[-1]) for page in pages[startPlan-1:endPlan]) + int(pages[-1][-1])
    else:
        total_seconds_plan = sum(int(page[-1]) for page in pages[startPlan-1:endPlan])



    left_seconds=total_seconds_plan-total_seconds
    left_seconds_triple=left_seconds/2.5

    hour = int(total_seconds / 60 // 60)
    minute = int((total_seconds - hour * 60 * 60) // 60)
    second = int(total_seconds - hour * 60 * 60 - minute * 60)
    # 计划时间
    hourPlan = int(total_seconds_plan / 60 // 60)
    minutePlan = int((total_seconds_plan - hourPlan * 60 * 60) // 60)
    secondPlan = int(total_seconds_plan - hourPlan * 60 * 60 - minutePlan * 60)
    percent = str(round(total_seconds/total_seconds_plan*100,2))

    # 剩下学习时长
    hourLeft = int(left_seconds / 60 // 60)
    minuteLeft = int((left_seconds - hourLeft * 60 * 60) // 60)
    secondLeft = int(left_seconds - hourLeft * 60 * 60 - minuteLeft * 60)

    # 倍数播放后学习时长剩余
    hourLeftTriple = int(left_seconds_triple / 60 // 60)
    minuteLeftTriple = int((left_seconds_triple - hourLeftTriple * 60 * 60) // 60)
    secondLeftTriple = int(left_seconds_triple - hourLeftTriple * 60 * 60 - minuteLeftTriple * 60)



    # print(f'已看总时长为:{hour:0>2d}:{minute:0>2d}:{second:0>2d}')
    # print(f'计划总时长为:{hourPlan:0>2d}:{minutePlan:0>2d}:{secondPlan:0>2d}')
    # print(f'剩余总时长为:{hourLeft:0>2d}:{minuteLeft:0>2d}:{secondLeft:0>2d}')
    # print('目前已完成'+percent+"%")

    total_seconds_State.set(f'已看总时长为:{hour:0>2d}:{minute:0>2d}:{second:0>2d}')
    total_seconds_plan_State.set(f'计划总时长为:{hourPlan:0>2d}:{minutePlan:0>2d}:{secondPlan:0>2d}')
    total_seconds_left_State.set(f'剩余总时长为:{hourLeft:0>2d}:{minuteLeft:0>2d}:{secondLeft:0>2d}')
    total_seconds_left_triple_State.set(f'倍速后时长为:{hourLeftTriple:0>2d}:{minuteLeftTriple:0>2d}:{secondLeftTriple:0>2d}')
    percentState.set('学习进度：' + percent+"%")

    localtime = time.localtime(time.time()+left_seconds_triple)


    plan_time_State.set(f'预计完成时间:{localtime.tm_hour:0>2d}:{localtime.tm_min:0>2d}:{localtime.tm_sec:0>2d}')
    #print ("本地时间为 :", localtime.tm_hour)

 
def get_filelist():
    dirs = os.listdir()
    filelist = []
    for d in dirs:
        if os.path.isfile(d):
            filelist.append(d)
    return filelist
def sumbit(self):
        bv = eBvId.get()
        if(bv=='') :
            tk.messagebox.showinfo(message='请输入bv号')
            return
        start = int(eBegin.get())
        startPlan=int(eBeginPlan.get())
        endPlan = int(eEndPlan.get())
        date = {'start': start, 'startPlan': startPlan, 'endPlan': endPlan,'bvId':bv}
        writedic(dic=date, filename='last.date')
        url = 'https://www.bilibili.com/video/' + bv
        file_name = url.split('/')[-1] + '.html'
        if file_name not in get_filelist():
            save_html(url)
        # if end=='':
        #     handel_data(file_name, start)
        # else:
        handel_data(file_name,start,startPlan,endPlan)
def plus(self):
    defaultBegin.set(int(defaultBegin.get())+1)
    sumbit(self)
def reduce(self):
    defaultBegin.set(int(defaultBegin.get())-1)
    sumbit(self)



def write():

    info = readfile('last.date')
    # print(info)
    if(info==""):
        return
    info = eval(info)  # 将存储的Logindate.txt文件转为字典格式

    if info:
        defaultBegin.set(str(info['start']))
        defaultBeginPlan.set(str(info['startPlan']))
        defaultEndPlan.set(str(info['endPlan']))
        defaultBvId.set(str(info['bvId']))
        # defaultEndPlan.set



root = tk.Tk()
root.title('bilibili视频进度计算')
root.geometry('600x500')
# root.after(0,write())

defaultBegin = tk.StringVar()
defaultBeginPlan = tk.StringVar()
defaultEndPlan = tk.StringVar()
defaultBvId = tk.StringVar()


bvId = tk.Label(root, text='Bv号:', justify=tk.RIGHT, width=80)
bvId.place(x=10, y=50, width=100, height=20)
eBvId = tk.Entry(root,width=100,textvariable=defaultBvId)
eBvId.place(x=130, y=50, width=200, height=20)

begin = tk.Label(root, text='目前集数:', justify=tk.RIGHT, width=80)
begin.place(x=10, y=80, width=100, height=20)
eBegin = tk.Entry(root, width=100,textvariable=defaultBegin)
eBegin.place(x=130, y=80, width=200, height=20)

eBegin.setvar("1")


# end = tk.Label(root, text='结束集数:', justify=tk.RIGHT, width=80)
# end.place(x=10, y=110, width=100, height=20)
# eEnd = tk.Entry(root, textvariable=defaultEndPlan, width=100)
# eEnd.place(x=130, y=110, width=200, height=20)


beginPlan = tk.Label(root, text='计划开始集数:', justify=tk.RIGHT, width=80)
beginPlan.place(x=10, y=110, width=100, height=20)
eBeginPlan = tk.Entry(root, width=100,textvariable=defaultBeginPlan)
eBeginPlan.place(x=130, y=110, width=200, height=20)
# eBeginPlan.setvar("1")

endPlan = tk.Label(root, text='计划结束集数:', justify=tk.RIGHT, width=80)
endPlan.place(x=10, y=140, width=100, height=20)
eEndPlan = tk.Entry(root, textvariable=defaultEndPlan, width=100)
eEndPlan.place(x=130, y=140, width=200, height=20)



startLogin=tk.Button(root,text='开始计算',command=lambda:sumbit(1))
startLogin.place(x=210,y=210,width=200,height=200)



total_seconds_State = tk.StringVar()
total_seconds_State.set('请开始计算')
lable_total_seconds_State = tk.Label(root, textvariable=total_seconds_State, justify=tk.RIGHT, width=80,bg='green',fg='white')
lable_total_seconds_State.place(x=30,y=250,width=150)

total_seconds_plan_State = tk.StringVar()
total_seconds_plan_State.set('请开始计算')
lable_total_seconds_plan_State = tk.Label(root, textvariable=total_seconds_plan_State, justify=tk.RIGHT, width=80,bg='green',fg='white')
lable_total_seconds_plan_State.place(x=30,y=275,width=150)

total_seconds_left_State = tk.StringVar()
total_seconds_left_State.set('请开始计算')
lable_total_seconds_left_State = tk.Label(root, textvariable=total_seconds_left_State, justify=tk.RIGHT, width=80,bg='green',fg='white')
lable_total_seconds_left_State.place(x=30,y=300,width=150)

percentState = tk.StringVar()
percentState.set('请开始计算')
lablePercentState = tk.Label(root, textvariable=percentState, justify=tk.RIGHT, width=80,bg='green',fg='white')
lablePercentState.place(x=30,y=325,width=150)

total_seconds_left_triple_State = tk.StringVar()
total_seconds_left_triple_State.set('请开始计算')
lable_total_seconds_left_triple_State = tk.Label(root, textvariable=percentState, justify=tk.RIGHT, width=80,bg='green',fg='white')
lable_total_seconds_left_triple_State.place(x=30,y=350,width=150)


total_seconds_left_triple_State = tk.StringVar()
total_seconds_left_triple_State.set('请开始计算')
lable_total_seconds_left_triple_State = tk.Label(root, textvariable=total_seconds_left_triple_State, justify=tk.RIGHT, width=80,bg='green',fg='white')
lable_total_seconds_left_triple_State.place(x=30,y=350,width=150)

plan_time_State = tk.StringVar()
plan_time_State.set('请开始计算')
lable_plan_time_State = tk.Label(root, textvariable=plan_time_State, justify=tk.RIGHT, width=80,bg='green',fg='white')
lable_plan_time_State.place(x=30,y=375,width=150)

eBegin.bind( "<Return>", sumbit)
root.bind_all('<Control-d>', plus )
root.bind_all('<Control-a>', reduce )


if __name__ == "__main__":
    write()
    root.mainloop()

    #root.bind('<Return>', sumbit())
    # while True:
    #     bv = input("请输入BV号：")
    #     start = int(input("输入视频起始集："))
    #     end = input("输入视频结束集：")
    #     url = 'https://www.bilibili.com/video/' + bv
    #     file_name = url.split('/')[-1] + '.html'
    #     if file_name not in get_filelist():
    #         save_html(url)
    #     if end=='':
    #         handel_data(file_name, start)
    #     else:
    #         handel_data(file_name,start,int(end))
    #     isContinue = input("是否继续？(y/n)：").lower()
    #     if isContinue == 'n':
    #         print("Bye~")
    #         break