import os
import io
import re
from PIL import Image
import pdf2image
import fitz #pip install PyMuPDF Pillow
from bs4 import BeautifulSoup as bs
import requests
import pdfkit

def pdf_downloader(Pth, url, printAsImage):
    NoOfPages = ''
    base = 'https://www.sec.gov/Archives/'
    lst = os.path.split(url)
    rtxt = re.sub('.txt', '',lst[1])
    rminus = re.sub('-', '', rtxt)
    index_url = base+'/'+lst[0]+'/'+rminus+'/'+rtxt+'-index.html'
    pth = Pth + '/' + 'PDF_DATA'
    if not os.path.exists(pth):
        os.mkdir(pth)
    r = requests.get(index_url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = bs(r.content,"html.parser")
    table = soup.find_all("table")[0]
    tr = table.findAll('tr')
    atag = tr[1].find('a')['href']
    splitPth = os.path.split(atag)
    fileName = pth+ '/'+ splitPth[1]
    link = 'https://www.sec.gov/'+atag
    url = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
    htmltext = url.text
    splitpth = os.path.split(splitPth[0])
    pdfPth = pth+'/'+splitpth[1]+'.pdf'
    with open(fileName, 'w', encoding='utf8') as fp:
        fp.write(htmltext)
    pdfkit.from_file(fileName, pdfPth) # .from_url and .from_string also exist
    os.remove(fileName)
    
    pdf_file = fitz.open(pdfPth)  
    NoOfPages = len(pdf_file)
    if printAsImage == 'yes':
        pth = Pth+'/'+'PDF_IMAGES'
        if not os.path.exists(pth):
            os.mkdir(pth)
        try:
            pages = convert_from_path(pdfPth)
            for e, page in enumerate(pages):
                image_name = pth + '/' + splitpth[1]+'-'+ str(e)+'.jpg'
                page.save(image_name, 'JPEG')
        except:
            pass
    else: 
        pass
    
    return NoOfPages
    
Pth = '10-K'
chunk_urls = ['edgar/data/1019272/0001521536-12-000031.txt',
 'edgar/data/1041009/0001144204-12-009085.txt']
printAsImage = 'No'
for url in chunk_urls:
    print(pdf_downloader(Pth, url, printAsImage))
    

