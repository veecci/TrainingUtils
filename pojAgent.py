import urllib, urllib2
import cookielib
from Tkinter import *
import tkMessageBox
import time
import sys

inf = 100000
filename = sys.argv[1]
problemID = filename[3:7]
username = sys.argv[2]

def getID(str):
    pat = 'user_id=' + username + '>'
    cnt = 0
    for i in range(str.find(pat), 0, -1):
        if (str[i] == 't' and str[i + 1] == 'd' and str[i + 2] == '>'):
            cnt += 1
        if (cnt == 3):
            id = ''
            for j in range(i + 3, inf):
                if (str[j] == '<'):
                    break
                id = id + str[j]
            return id

def getStatus(str):
    beg = str.find('Result:</b>')
    beg = str.find('<font color=', beg)
    ret = ''
    for i in range(beg, inf):
        if (str[i] == '>'):
            for j in range(i + 1, inf):
                if (str[j] == '<'): break
                ret = ret + str[j]
            return ret



posturl = 'http://poj.org/login'
data = {'user_id1':sys.argv[2], 'password1':sys.argv[3]}
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
try:
    req = urllib2.Request(posturl, urllib.urlencode(data))
except urllib2.HTTPError, e:
    print e.code
resp = urllib2.urlopen(req)

file_object = open(filename + '.cc')
try:
     source = file_object.read()
finally:
     file_object.close()

posturl = 'http://poj.org/submit?problem_id=' + problemID
data = {
    'problem_id':problemID,
    'language':'4',
    'source':source,
    'submit':'Submit'}

req = urllib2.Request(posturl, urllib.urlencode(data))
resp = urllib2.urlopen(req)
html_str = resp.read()

id = getID(html_str)

print "id=", id

statusCode = -1
while (statusCode == -1):
    geturl = 'http://poj.org/showsource?solution_id=' + id
    # print "get: ", geturl
    req = urllib2.urlopen(geturl)
    status = getStatus(req.read())
    print status
    if (status == 'Waiting' or status == 'Compiling' or status == 'Running & Judging'):
        time.sleep(1)
    else:
        break

#time.sleep(2)

#window = Tk()
#window.wm_withdraw()
#tkMessageBox.showinfo(title=filename + ' RESULT:', message=status)