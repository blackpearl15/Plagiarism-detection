from django.http import HttpResponse
from django.shortcuts import render,redirect
from difflib import SequenceMatcher,Differ
import requests
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from bs4 import BeautifulSoup
import PyPDF2
import docx2txt
from django.template import RequestContext


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
        seq = SequenceMatcher(a=txt1,b=txt2)
        rat = 100*(seq.ratio())
        print(rat)
        rat = round(rat, 2)
        params= { 'hero': 'YOUR PLAGARISM SCORE' , 'answer': rat}
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
        
        print(ans)
        seq = SequenceMatcher(a=res, b=ans)

        rat = 100*(seq.ratio())
        rat = round(rat, 2)
        print(rat*100)


        params= { 'hero': 'YOUR PLAGARISM SCORE' , 'answer': rat}
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

        
        seq = SequenceMatcher(a=resu, b=ans)

        rat = 100 * (seq.ratio())
        rat = round(rat, 2)
        print(rat*100)


        params= { 'hero': 'YOUR PLAGARISM SCORE' , 'answer': rat}
        return render(request,'result.html',params)
