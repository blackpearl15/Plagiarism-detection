from django.http import HttpResponse
from django.shortcuts import render,redirect
import difflib
from difflib import SequenceMatcher,Differ
import requests
import os
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from bs4 import BeautifulSoup
import PyPDF2
import docx2txt
from django.template import RequestContext
from reportlab.pdfgen import canvas
from django.shortcuts import render
import io


def report(t1,t2,t3,t4):
    from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.lib.pagesizes import A4, landscape, portrait
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, Flowable, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas

    doc1 =[]
    pdfmetrics.registerFont(TTFont('Timesbd', 'timesbd.ttf',))
    pdfmetrics.registerFont(TTFont('c','Georgia.ttf',))
    pdfmetrics.registerFont(TTFont('cb','Georgiab.ttf',))

    doc1.append(Spacer(1,-60))
    doc1.append(Spacer(1,20))
    doc1.append(Paragraph('PLAGIARISM REPORT',ParagraphStyle(name='p',fontName='Timesbd',textColor= 'rgb(0,0,134)',fontSize=24,alignment=TA_CENTER)))
    doc1.append(Spacer(1,30))
    
    def addp(doc):
        doc1.append(Paragraph('PLAG SCORE:',ParagraphStyle(name='q',fontName='Timesbd',textColor='rgb(0,0,134)',fontSize=16,alignment=TA_CENTER)))
        doc.append(Spacer(1,10))
        doc1.append(Paragraph(t1,ParagraphStyle(name='r',fontName='Timesbd',fontSize=16,textColor='rgb(204,0,0)',alignment=TA_CENTER)))

        doc.append(Spacer(1,30))
        doc1.append(Paragraph('INPUT 1',ParagraphStyle(name='s',fontName='Timesbd',fontSize=16,textColor= 'rgb(0,0,134)',alignment=TA_CENTER)))
        doc.append(Spacer(1,10))
        doc1.append(Paragraph(t2,ParagraphStyle(name='t',fontName='c',textColor='rgb(0,0,0)',fontSize=12,alignment=TA_CENTER)))

        doc.append(Spacer(1,25))
        doc1.append(Paragraph('INPUT 2',ParagraphStyle(name='u',fontName='Timesbd',textColor= 'rgb(0,0,134)',fontSize=16,alignment=TA_CENTER)))
        doc.append(Spacer(1,10))
        doc1.append(Paragraph(t3,ParagraphStyle(name='v',fontName='c',textColor= 'rgb(0,0,0)',fontSize=12,alignment=TA_CENTER)))

        doc.append(Spacer(1,25))
        doc1.append(Paragraph('MATCHED DATA',ParagraphStyle(name='w',fontName='Timesbd',textColor= 'rgb(0,0,134)',fontSize=16,alignment=TA_CENTER)))
        doc1.append(Spacer(1,10))
        doc1.append(Paragraph(t4,ParagraphStyle(name='x',fontName='cb',fontSize=12,textColor= 'rgb(180,0,0)',alignment=TA_CENTER)))
        return doc

    doc1=addp(doc1)
    SimpleDocTemplate('media\Plag_Report.pdf',title='Plag_Report',pagesize=A4).build(doc1)
    return doc1

    



def genrep(request):
    fs=FileSystemStorage()
    filename="Plag_Report.pdf"
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            response=HttpResponse(pdf,content_type='application/pdf')
            response['Content-Disposition']='inline; filename="Plag_Report.pdf"'
            return response
    else:
        return HttpResponse("error hai")


def dowrep(request):
    fs=FileSystemStorage()
    filename="Plag_Report.pdf"
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            response=HttpResponse(pdf,content_type='application/pdf')
            response['Content-Disposition']='attachment; filename="Plag_Report.pdf"'
            return response
    else:
        return HttpResponse("error hai")




def index(request):
    return render ( request, 'index.html')

def result(request):
    txt1 = request.POST.get('sa',"-1")
    txt2 = request.POST.get('sb',"-1")

    djtext1 = request.POST.get('linkkesathcode',"-1")
    djtext2 = request.POST.get('linkname',"-1")


    state1 = request.POST.get('x1','off')
    print(state1)
 
    if(txt1 != "-1" and txt2 != "-1"):
        common=""
        matcher = SequenceMatcher(a=txt1,b=txt2)
        matches = matcher.get_matching_blocks()
        for match in matches:
            common +=  txt1[match.a:match.a + match.size]
        seq = SequenceMatcher(a=txt1,b=txt2)
        x = 100*(seq.ratio())
        
        x = round(x, 2)
        rat = ""
        rat = str(x)
        print(common)

        report(rat,txt1,txt2,common)
        params= { 'hero': 'YOUR PLAGIARISM SCORE' , 'answer': rat}
        return render(request, 'result.html',params)

    elif djtext1 != "-1" and djtext2 != "-1":

        # print(djtext1)
        
        r = requests.get(djtext2)
        htmlContent = r.content 

        soup = BeautifulSoup(htmlContent, 'html.parser')
        code = soup.find(class_="code")
        res =""
        for item in code.stripped_strings:
            res = res + item
        
        print(res)
        # print(djtext1)
        ans=""       
        ans = djtext1.replace("\n", "")
        
        
        common=""
        matcher = difflib.SequenceMatcher(None, res, ans)
        matches = matcher.get_matching_blocks()
        for match in matches:
            common +=  res[match.a:match.a + match.size]
        seq = SequenceMatcher(a=res, b=ans)

        x = 100*(seq.ratio())

        x = round(x, 2)
        rat = ""
        rat = str(x)
        
        if(x==100.0):
            common = ans
        
        report(rat,ans,res,common)


        params= { 'hero': 'YOUR PLAGIARISM SCORE' , 'answer': rat}
        return render(request, 'result.html',params)
    
    elif request.method == 'POST' and state1 =='on':
        chara1 = request.FILES['f1']
        chara2 = request.FILES['f2']
        
        chara1kaname = chara1.name
        chara2kaname = chara2.name
        ans = ""
        if(chara1kaname[-1] == 'f'):
            a = PyPDF2.PdfFileReader(chara1)
            b=a.getNumPages()
            
            for i in range(1,b):
                ans += a.getPage(i).extractText()

        elif(chara2kaname[-1] == 'x'):
            a = docx2txt.process(chara1)
            ans = a

        

        resu = ""
        if(chara2kaname[-1] == 'f'):
            c = PyPDF2.PdfFileReader(chara2)
            d=c.getNumPages()
            
            for i in range(1,d):
                resu += c.getPage(i).extractText()

        elif(chara2kaname[-1] == 'x'):
            c = docx2txt.process(chara2)
            resu = c

        common=""
        matcher = difflib.SequenceMatcher(None, resu, ans)
        matches = matcher.get_matching_blocks()
        for match in matches:
            common +=  txt1[match.a:match.a + match.size]
        seq = SequenceMatcher(a=resu, b=ans)

        x = 100 * (seq.ratio())
        x = round(x, 2)
        rat = ""
        rat = str(x)

        if(x==100.0):
            common = ans

        report(rat,resu,ans,common)


        params= { 'hero': 'YOUR PLAGIARISM SCORE' , 'answer': rat}
        return render(request,'result.html',params)
