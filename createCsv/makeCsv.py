# -*- coding: utf-8 -*-

import sys
import os
import datetime
import numpy as np
import csv
import xlwt
import datetime

# file global value
logFile = "./makeCsv.log"
home_path = ""
fileList = []

# data global value
userId = ""
userName = ""
workDay = []
dayType = []
attendance = []
chuqinTime = []
endTime = []
workTime = []
otherTime = []

def echoLog(*info):
    logInfo = ""
    # msg create
    for s in info:
        logInfo = logInfo + s
    logInfo = logInfo + '\n'

    print(logInfo)
    #fp = open(logFile, 'a', encoding="utf-8")
    #fp.write(logInfo)
    #fp.flush()
    #fp.close()

def chkInput():
    global home_path
    # no path input 
    if len(sys.argv) == 1:
        #home_path = sys.path[0]
        home_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    # has path input
    else:
        home_path = sys.argv[1]
        if not os.path.isdir(home_path):
            echoLog('input a wrong path:', home_path)
            exit(2)
    echoLog('work path is ', home_path)

def getFileInfo():
    global fileList
    for f in os.listdir(home_path):
        suffix = os.path.splitext(f)[1]
        if suffix == ".txt":
            fileList.append(f)
    echoLog('file list is:', "\n".join(fileList))

def dataClean():
    global userId
    global userName
    global workDay
    global dayType
    global attendance
    global chuqinTime
    global endTime
    global workTime
    global otherTime

    userId = ""
    userName = ""
    workDay = []
    dayType = []
    attendance = []
    chuqinTime = []
    endTime = []
    workTime = []
    otherTime = []

def parasData(f):
    global home_path
    global fileList
    global userId
    global userName
    global workDay
    global dayType
    global attendance
    global chuqinTime
    global endTime
    global workTime
    global otherTime

    path = home_path + '\\' + f
    lines = np.loadtxt(path,delimiter=",",encoding='SJIS',dtype=str)
    for line in lines:
        data = str(line).split()
        # all data set
        userId = data[0]
        userName = data[1] + ' ' + data[2]

        workDay.append(data[3][0:4] + '年' + data[3][4:6] + '月' + data[3][6:8] + '日')
        dayType.append(data[5])
        if data[5] == "出勤日":
            attendance.append(data[7])
            if data[7] == "出勤":
                chuqinTime.append(data[8])
                endTime.append(data[9])
                workTime.append(data[13])
                otherTime.append(data[14])
            else:
                chuqinTime.append('')
                endTime.append('')
                workTime.append('')
                otherTime.append('')
        else:
            attendance.append('')
            chuqinTime.append('')
            endTime.append('')
            workTime.append('')
            otherTime.append('')

def sendData():
    global home_path
    global userId
    global userName
    global workDay
    global dayType
    global attendance
    global chuqinTime
    global endTime
    global workTime
    global otherTime

    path = home_path + '\\勤務表_' + userName + '_' + workDay[0][0:4] + workDay[0][5:7] +'.xls'
    if os.path.exists(logFile):
        os.remove(logFile)

    workbook =  xlwt.Workbook(encoding = 'ascii')
    worksheet = workbook.add_sheet('勤務表')
    style = xlwt.XFStyle() # 初始化样式
    style1 = xlwt.XFStyle() # 初始化样式
    style2 = xlwt.XFStyle() # 初始化样式

    font = xlwt.Font() # 为样式创建字体
    font.name = 'Times New Roman' 
    font.bold = True # 黑体
    #font.underline = False # 下划线
    #font.italic = False # 斜体字

    pattern = xlwt.Pattern() # Create the Pattern
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    pattern.pattern_fore_colour = 49 # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...

    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN
    borders.left_colour = 0
    borders.right_colour = 0
    borders.top_colour = 0
    borders.bottom_colour = 0

    style.font = font       # 加粗

    style1.borders = borders  # 加框线
    style1.pattern = pattern # 加背景色

    style2.borders = borders  # 加框线

    data = workDay[0][5:7] + '月出勤表'
    worksheet.write(0, 0, data, style)

    worksheet.write(1, 0, '社員番号', style1)
    worksheet.write(1, 1, userId, style2)
    worksheet.write(2, 0, '社員氏名', style1)
    worksheet.write(2, 1, userName, style2)

    worksheet.write(4, 0, '年月日', style1)
    worksheet.write(4, 1, '出勤/休日', style1)
    worksheet.write(4, 2, '勤務区分', style1)
    worksheet.write(4, 3, '出勤', style1)
    worksheet.write(4, 4, '退勤', style1)
    worksheet.write(4, 5, '休憩時間', style1)
    worksheet.write(4, 6, '実働時間', style1)
    worksheet.write(4, 7, '時間外', style1)
    """
    echoLog(str(workDay))
    echoLog(str(dayType))
    echoLog(str(attendance))
    echoLog(str(chuqinTime))
    echoLog(str(endTime))
    echoLog(str(workTime))
    echoLog(str(otherTime)) """
    col_hours = 0
    col_seconds = 0
    for i, v in enumerate(workDay):
        worksheet.write(i + 5, 0, v, style2)
        worksheet.write(i + 5, 1, dayType[i], style2)
        if(dayType[i] == '出勤日'):
            worksheet.write(i + 5, 2, attendance[i], style2)
            if(attendance[i] == '出勤'):
                worksheet.write(i + 5, 3, chuqinTime[i], style2)
                worksheet.write(i + 5, 4, endTime[i], style2)
                worksheet.write(i + 5, 5, '1:00', style2)
                worksheet.write(i + 5, 6, workTime[i], style2)
                worksheet.write(i + 5, 7, otherTime[i], style2)

                col_seconds = col_seconds + int(workTime[i][3:])
                if col_seconds > 60:
                    col_seconds = col_seconds - 60
                    col_hours = col_hours + 1 + int(workTime[i][0:2])
                else:
                    col_hours = col_hours + int(workTime[i][0:2])
            else:
                worksheet.write(i + 5, 3, '', style2)
                worksheet.write(i + 5, 4, '', style2)
                worksheet.write(i + 5, 5, '', style2)
                worksheet.write(i + 5, 6, '', style2)
                worksheet.write(i + 5, 7, '', style2)
        else:
            worksheet.write(i + 5, 2, '', style2)
            worksheet.write(i + 5, 3, '', style2)
            worksheet.write(i + 5, 4, '', style2)
            worksheet.write(i + 5, 5, '', style2)
            worksheet.write(i + 5, 6, '', style2)
            worksheet.write(i + 5, 7, '', style2)

    worksheet.write(37, 4, '勤務時間合計:')
    if col_seconds < 10:
        my_work = str(col_hours) + ':0' + str(col_seconds)
    else:
        my_work = str(col_hours) + ':' + str(col_seconds)
    worksheet.write(37, 6, my_work)
    worksheet.col(0).width = 4555
    workbook.save(path) # 保存文件

def main():
    chkInput()
    getFileInfo()

    for f in fileList:
        dataClean()
        parasData(f)
        sendData()


if __name__ == "__main__":
    # clear old log
    if os.path.exists(logFile):
        os.remove(logFile)
    
    echoLog('start at: \t\t', str(datetime.datetime.now()))
    main()
    echoLog('end at: \t\t', str(datetime.datetime.now()))