from django.http import HttpResponse
from django.shortcuts import render,redirect
from difflib import SequenceMatcher,Differ
import requests
from django.core.files.storage import FileSystemStorage
from bs4 import BeautifulSoup
import PyPDF2


def index(request):
    return render ( request, 'index.html')

def result(request):
    txt1 = request.POST.get('sa',"-1")
    txt2 = request.POST.get('sb',"-1")

    djtext1 = request.POST.get('linkkesathcode',"-1")
    djtext2 = request.POST.get('linkname',"-1")



    chara1 = request.FILES['fileup1',"-1"]
    chara2 = request.FILES['fileup2',"-1"]
    
    pdftxt1=chara1.name
    pdftxt2=chara2.name
    # print(pdftxt1)
    # print(pdftxt2)
    if(txt1 != "-1" and txt2 != "-1"):
        if(txt1 != "" and txt2 != ""):
            seq = SequenceMatcher(a=txt1,b=txt2)
            ans = 100*(seq.ratio())
            print(ans)
            params= { 'hero': 'Changed' , 'answer': ans}
            return render(request, 'result.html',params)
        else:
            return redirect('/')
    elif(djtext1 != "-1" and djtext2 != "-1"):

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
        print(rat*100)


        params= { 'hero': 'Changed' , 'answer': rat}
        return render(request, 'result.html',params)
    
    elif(pdftxt1 != "-1" and pdftxt2 != "-1"):
        a = PyPDF2.PdfFileReader(pdftxt1)
        c = PyPDF2.PdfFileReader(pdftxt2)

        b=a.getNumPages()
        ans = ""
        for i in range(1,b):
            ans += a.getPage(i).extractText()

        d=c.getNumPages()
        resu = ""
        for i in range(1,c):
            resu += c.getPage(i).extractText()
        
        seq = SequenceMatcher(a=resu, b=ans)

        rat = seq.ratio()
        print(rat*100)


        params= { 'hero': 'Changed' , 'answer': rat}
        return render(request, 'result.html',params)
