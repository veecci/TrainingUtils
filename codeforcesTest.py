__author__ = 'vici'
import os, sys, urllib2

filename = sys.argv[1]
filepath = sys.argv[2]
file_object = open(filepath + '/cid')

try: contestID = file_object.read()[0:-1]
finally: file_object.close()

def getSamples(str):
    ret = []
    pos = str.find('Sample test(s)')
    while (pos != -1):
        pos = str.find('Input</div><pre>', pos)
        if (pos == -1): break
        endPos = str.find('</pre></div>', pos)
        ret.append(str[pos + 16 : endPos].replace('<br />', '\n'))
        pos = str.find('Output</div><pre>', endPos)
        endPos = str.find('</pre></div>', pos)
        ret.append(str[pos + 17 : endPos].replace('<br />', '\n'))
        pos = endPos
    return ret

def adjustOutput(str):
    ret = ''
    newLine = 1
    for i in xrange(len(str) - 1, -1, -1):
        if (str[i] == '\n'): newLine = 1
        elif (str[i] != ' '): newLine = 0
        if (newLine and str[i] == ' '): continue
        ret = str[i] + ret
    return ret

if (contestID[-1] == 'p'):
    url = 'http://codeforces.com/problemset/problem/' + contestID[0:-1] + '/' + filename
else:
    url = 'http://codeforces.com/contest/' + contestID[0:-1] + '/problem/' + filename

req = urllib2.urlopen(url)
samples = getSamples(req.read())
#print samples

accepted = 1

for i in xrange(0, len(samples), 2):
    fileObject = open('CFTest.in', 'w')
    fileObject.write(samples[i])
    fileObject.close()
    output = os.popen('g++ ' + filename + '.cc -o ' + 'CFTest.out && ./' + 'CFTest.out < ' + 'CFTest.in').read()
    output = adjustOutput(output)
    if (output[-1] == '\n' and samples[i + 1][-1] != '\n'): output = output[0: -1]
    if (cmp(output, samples[i + 1]) != 0):
        status = 'Wrong #' + str(i / 2 + 1) + '\n'
        status += samples[i + 1] + '\n---------------\nYour output:\n' + output + '\n'
        print status
        accepted = 0

if (accepted):
    print 'All Tests Passed.'

