from typing import Set
from pandas.core.construction import is_empty_data
import requests
import json
import os
import pandas as pd
from pathlib import Path
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import resolve1
import glob
import shutil
import toolz
import os
from datetime import datetime
from dateparser.search import search_dates
from itertools import groupby
import numpy as np
import sys

url = ['http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2022%20du%2023%20mars%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2023%20du%2024%20mars%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2024%20du%2025%20mars%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2025%20%20du%2026%20mars%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20N%C2%B031%20du%2001%20avril%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2032%20DU%2002%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communique%2033%20du%2003%20avril%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2034%20DU%2004%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2035%20DU%2005%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2036%20DU%2006%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2037%20DU%2007%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2038%20DU%2008%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2039%20DU%2009%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2040%20DU%2010%20AVRIL%202020_1.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2041%20DU%2011%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2042%20DU%2012%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2043%20DU%2013%20Avril%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2044%20DU%2014%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2045%20DU%2015%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2046%20DU%2016AVRIL%202020%20pdf.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2047%20DU%2017%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2048%20DU%2018%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2049%20DU%2019%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2050%20DU%2020%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2051%20DU%2021%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2052%20DU%2022%20AVRIL%202020%281%29.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2053%20DU%2023%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2054%20DU%2024%20AVRIL%202020_0.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2055%20DU%2025%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2056%20DU%2026%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2057%20DU%2027%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2058%20DU%2028%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2059%20DU%2029%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2060%20DU%2030%20AVRIL%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A961.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20de%20presse%20num%C3%A9ro%2062%20covid19.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2063%20DU%2003%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20N%C2%B064%20du%2004%20mai%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2065%20DU%2005%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2066%20DU%2006%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2071%20DU%2011%20MAI%202020.pdf.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2072%20DU%2012%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2073%20DU%2013%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2074%20DU%2014%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNUQUE%2075%20DU%2015%20MAI%202020%20.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2076%20DU%2016%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2077%20DU%2017%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2078%20DU%2018%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2079%20DU%2019%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2080%20DU%2020%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2081%20DU%2021%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2082%20DU%2022%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2083%20DU%2023%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2085%20DU%2025%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2086%20DU%2026%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2087%20DU%2027%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2088%20DU%2028%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2090%20DU%2030%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2091%20DU%2031%20MAI%202020%281%29.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2092%20DU%2002%20JUIN%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2093%20DU%2003%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2094%20DU%2003%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2095%20DU%2004%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2096%20DU%2005%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2097%20DU%2006%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2098%20DU%2007%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%2099%20DU%2008%20MAI%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20100%20DU%2009%20JUIN%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20102%20DU%2011%20MAI%202020.pdf.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20103%20DU%2012%20MAI%202020_0.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20104%20DU%2013%20JUIN%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20105%20DU%2014%20JUIN%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20106%20DU%2015%20JUIN%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20107%20DU%2016%20JUIN%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20108%20DU%2017%20JUIN%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20109%20DU%2018%20JUIN%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20110%20DU%2019%20JUIN%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20117%20DU%2026%20JUIN%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20118%20DU%2027%20JUIN%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20119%20DU%2028%20JUIN%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20120%20DU%2029%20JUIN%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20121%20DU%2030%20JUIN%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20122%20DU%2001%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20123%20DU%2002%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20124%20DU%2003%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20125%20DU%2004%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20126%20DU%2005%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20127%20DU%2006%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20128%20DU%2007%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20129%20DU%2008%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20130%20DU%2009%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20131%20DU%2010%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20132%20DU%2011%20JUILLET.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20133%20du%2012%20juillet%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20134%20du%2013%20juillet%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20135%20DU%2014%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20136%20DU%2015%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20137%20DU%2016%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20138%20DU%2017%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20139%20DU%2018%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/communuqu%C3%A9%20140%20du%2019%20juillet%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20141%20DU%2020%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20142%20DU%2021%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20143%20DU%2022%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20144%20DU%2023%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20145%20DU%2024%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/communiqu%C3%A9%20n%C2%B0146%20du%2025%20juillet.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20147%20du%2026%20juillet%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20148.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9149_covid19.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20151%20DU%2030%20JUILLET%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20152_covid19.pdf',
        'http://www.sante.gouv.sn/sites/default/files/communique%20no%20153%20covid-19.pdf',
        'http://www.sante.gouv.sn/sites/default/files/communiqu%C3%A9%20154%20covid-19.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20155%20DU%2003%20AOUT%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20156%20DU%2004%20AOUT%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20157%20Du%2005%20aout%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communique%20158%20du%2006%20aout%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20159%20du%2007%20Aout%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20160%20du%2008%20Aout%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20161.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20162%20du%2010%20Aout%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20163%20du%2011%20Aout%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20164%20du%2012%20Aout%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20165%20du%2013%20Aout%202020_20200813093753%281%29.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20166%20du%2014%20Aout%202020_20200814095030.pdf',
        'http://www.sante.gouv.sn/sites/default/files/communiqu%C3%A9%20167%20covid19.pdf',
        'http://www.sante.gouv.sn/sites/default/files/com166covid19.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20169%20du%2017%20Aout%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20170%20du%2018%20Aout%202020%20%282%29.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20171%20du%2019%20aout%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20172%20du%2020%20aout%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20173%20du%2021%20aout%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20174%20DU%2022%20AOUT%202020%281%29.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20175%20DU%2023%20AOUT%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20176%20du%2024%20aout%202020%281%29.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20177%20du%2025%20aout%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20178.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20178.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20180_Covid-19sn.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20181%20DU%2029%20AOUT%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20182%20DU%2030%20AOUT%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20183.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20184_covid-19.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20185%20covid19.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20186covid19.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9187_covid19.pdf',
        'http://www.sante.gouv.sn/sites/default/files/Communiqu%C3%A9%20188_Covid-19.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20189%20DU%2006%20SEPTEMBRE%202020.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQU%C3%89%20190_COVID19.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20191_Covid19_0.pdf',
        'https://sante.sec.gouv.sn/sites/default/files/COMMUNIQUE%20161.pdf',
        'https://sante.sec.gouv.sn/sites/default/files/Communiqu%C3%A9%20162%20du%2010%20Aout%202020.pdf',
        'https://sante.sec.gouv.sn/sites/default/files/Communiqu%C3%A9%20163%20du%2011%20Aout%202020.pdf',
        'https://sante.sec.gouv.sn/sites/default/files/Communiqu%C3%A9%20164%20du%2012%20Aout%202020.pdf',
        'https://sante.sec.gouv.sn/sites/default/files/Communiqu%C3%A9%20165%20du%2013%20Aout%202020_20200813093753%281%29.pdf',
        'https://sante.sec.gouv.sn/sites/default/files/Communiqu%C3%A9%20166%20du%2014%20Aout%202020_20200814095030.pdf',
        'https://sante.sec.gouv.sn/sites/default/files/communiqu%C3%A9%20167%20covid19.pdf',
        'https://sante.sec.gouv.sn/sites/default/files/com166covid19.pdf',

    'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20378%20DU%2014%20MARS%202021.pdf',
        'http://www.sante.gouv.sn/sites/default/files/COMMUNIQUE%20378.pdf'
      ]
# DOWNLOAD PDF FILES 
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
           'AppleWebKit/537.36 (KHTML, like Gecko) '\
           'Chrome/75.0.3770.80 Safari/537.36'}
for i in url:
    try:
      print ('Starting to Download!')
      r = requests.get(i, headers=headers)
      #r.status_code
      filename = i.split('/')[-1]
      with open(filename, 'wb') as out_file:
        out_file.write(r.content)
      print("Download complete!")
      r.raise_for_status()
    except Exception as e:
      print(e)

# MOVE ALL DOWNLOADED PDF FILES TO PDF FOLDER
for f in glob.glob('*.pdf'):
    shutil.move(f, 'PDF')

# LISTING ALL PDF FILES NAME IN PDF FOLDER
entries = os.listdir('PDF')
#print(entries)

import pdf2image
import pytesseract
from pytesseract import Output, TesseractError
import re
import datefinder
import dateparser

tabJson = []
tab_month = []
# READING ALL DOWNLOADED PDF FILES IN PDF FOLDER
for pdf_path in entries:
  try:
    images = pdf2image.convert_from_path('PDF/'+pdf_path)
    pil_im = images[0] # assuming that we're interested in the first page only
    ocr_dict = pytesseract.image_to_data(pil_im, lang='eng', output_type=Output.DICT)
    text1 = " ".join(ocr_dict['text'])
  
    file = open('PDF/'+pdf_path, 'rb')
    parser = PDFParser(file)
    document = PDFDocument(parser)
# This will give you the count of pages
    if resolve1(document.catalog['Pages'])['Count'] > 1:
      pil_im1 = images[1]
      ocr_dict1 = pytesseract.image_to_data(pil_im1, lang='eng', output_type=Output.DICT)
      text2 = " ".join(ocr_dict1['text'])
    else:
        text2 = ''
  # ocr_dict now holds all the OCR info including text and location on the image
    text = text1 + text2
    #print(text)

    day = re.search("(lundi|mardi|Mercredi|mércredi|jeudi|vendredi|samedi|dimanche)",text,re.IGNORECASE)
    
    word = r"\W*([\w]+)"
    n = 3
    groups = re.search(r'{}\W*{}{}'.format(word*n,str(day.group(0)),word*n), text, re.IGNORECASE).groups()
    date_input = str(groups[n:][0])+'-'+str(groups[n:][1]).lower()+'-'+str(groups[n:][2])
    if len(str(groups[n:][0])) < 2:
          daily = '0'+str(groups[n:][0])
    else:
          daily = str(groups[n:][0])
    #print('***********DATE INPUT***********', daily)
    if str(groups[n:][1]).lower() == 'janvier':
          month = '01'
    if str(groups[n:][1]).lower() == 'février':
          month = '02'
    if str(groups[n:][1]).lower() == 'mars':
          month = '03'
    if str(groups[n:][1]).lower() == 'avril':
          month = '04'
    if str(groups[n:][1]).lower() == 'mai':
          month = '05'
    if str(groups[n:][1]).lower() == 'juin':
          month = '06'
    if str(groups[n:][1]).lower() == 'juillet':
          month = '07'
    if str(groups[n:][1]).lower() == 'août':
          month = '08'
    if str(groups[n:][1]).lower() == 'septembre':
          month = '09'
    if str(groups[n:][1]).lower() == 'octobre':
          month = '10'
    if str(groups[n:][1]).lower() == 'novembre':
          month = '11'
    if str(groups[n:][1]).lower() == 'décembre':
          month = '12'
    date = daily+'/'+month+'/'+str(groups[n:][2])
    #print(date)
  except Exception as e:
        print(e)

# COLLECTING DATAS
  cas_positifs = re.search(r'(\w+\s+){0,3}sont revenus positifs(\w+\s+){0,3}', text, re.IGNORECASE)
  if cas_positifs:
    #print(cas_positifs.group(0))
    pos_num = str(cas_positifs.group(0))
    cas_positifs_nums = [int(s) for s in pos_num.split() if s.isdigit()]
    if cas_positifs_nums == []:
          cas_positifs_nums = [0]
    #print(cas_positifs_nums)
  else: cas_positifs_nums = [0]

  cas_importes = re.search(r'(\w+\s+){0,3}cas importés(\w+\s+){0,3}', text, re.IGNORECASE)
  if cas_importes:
    #print(cas_importes.group(0))
    imp_num = str(cas_importes.group(0))
    cas_importes_nums = [int(s) for s in imp_num.split() if s.isdigit()]
    if cas_importes_nums == []:
          cas_importes_nums = [0]
    #print(cas_importes_nums)
  else: cas_importes_nums = [0]

  cas_contacts = re.search(r'(\w+\s+){0,3}cas contacts(\w+\s+){0,3}', text, re.IGNORECASE)
  if cas_contacts:
    #print(cas_contacts.group(0))
    cont_num = str(cas_contacts.group(0))
    cas_contacts_nums = [int(s) for s in cont_num.split() if s.isdigit()]
    if cas_contacts_nums == []:
          cas_contacts_nums = [0]
    #print(cas_contacts_nums)
  else: cas_contacts_nums = [0]

  tests_realises = re.search(r'(\w+\s+){0,3}tests réalisés(\w+\s+){0,3}', text, re.IGNORECASE)
  if tests_realises:
    #print(tests_realises.group(0))
    test_num = str(tests_realises.group(0))
    if tests_realises.group(0) is not None:
      cas_test_nums = [int(s) for s in test_num.split() if s.isdigit()]
      if cas_test_nums == []:
          cas_test_nums = [0]
    #else: cas_test_nums = [0]
    #print(cas_test_nums)
  else: cas_test_nums = [0]

  sous_traitement = re.search(r'(\w+\s+){0,3}sous traitement(\w+\s+){0,3}', text, re.IGNORECASE)
  if sous_traitement:
    #print(sous_traitement.group(0))
    trait_num = str(sous_traitement.group(0))
    cas_sous_traitement_nums = [int(s) for s in trait_num.split() if s.isdigit()]
    if cas_sous_traitement_nums == []:
          cas_sous_traitement_nums = [0]
    #print(cas_sous_traitement_nums)
  else: cas_sous_traitement_nums = [0]

  contacts_suivis = re.search(r'(\w+\s+){0,3}contacts suivis(\w+\s+){0,3}', text, re.IGNORECASE)
  if contacts_suivis:
    #print(contacts_suivis.group(0))
    suivi_num = str(contacts_suivis.group(0))
    cas_contacts_suivis_nums = [int(s) for s in suivi_num.split() if s.isdigit()]
    if cas_contacts_suivis_nums == []:
          cas_ccontacts_suivis_nums = [0]
    #print(cas_contacts_suivis_nums)
  else: cas_contacts_suivis_nums = [0]

  cas_communautaires = re.search(r'(\w+\s+){0,12} communautaire(\w+\s+){0,3}', text, re.IGNORECASE)
  if cas_communautaires:
    #print(cas_communautaires.group(0))
    comm_num = str(cas_communautaires.group(0))
    cas_communautaires_nums = [int(s) for s in comm_num.split() if s.isdigit()]
    if cas_communautaires_nums == []:
          cas_communautaires_nums = [0]
    #print(cas_communautaires_nums)
  else: cas_communautaires_nums = [0]

  cas_gueris = re.search(r'(\w+\s+){0,6}négatifs et déclarés guéris(\w+\s+){0,3}', text, re.IGNORECASE)
  if cas_gueris:
    #print(cas_gueris.group(0))
    gueris_num = str(cas_gueris.group(0))
    cas_gueris_nums = [int(s) for s in gueris_num.split() if s.isdigit()]
    #print(cas_gueris_nums)
  else: cas_gueris_nums = [0]

  cas_deces = re.search(r'(\w+\s+){0,10}décès(\w+\s+){0,10}', text, re.IGNORECASE)
  if cas_deces:
    #print(cas_deces.group(0))
    deces_num = str(cas_deces.group(0))
    cas_deces_nums = [int(s) for s in deces_num.split() if s.isdigit()]
    if cas_deces_nums == []:
            cas_deces_nums = [0]
    #else: cas_deces_nums = [0]
    #print(cas_deces_nums)
  else: cas_deces_nums = [0]

  # SEARCHING FOR DIFFERENT LOCAL IN SENEGAL
  expression = r"(?i)(?:\bDakar\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Dakar)"
  expression1 = r"(?i)(?:\bThiès\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Thiès)"
  expression2 = r"(?i)(?:\bTouba\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Touba)"
  expression3 = r"(?i)(?:\bDiourbel\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Diourbel)"
  expression4 = r"(?i)(?:\bFatick\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Fatick)"
  expression5 = r"(?i)(?:\bKaolack\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Kaolack)"
  expression6 = r"(?i)(?:\bKaffrine\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Kaffrine)"
  expression7 = r"(?i)(?:\bKolda\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Kolda)"
  expression8 = r"(?i)(?:\bTamba\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Tamba)"
  expression9 = r"(?i)(?:\bZiguinchor\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Ziguinchor)"
  expression10 = r"(?i)(?:\bSaint-Louis\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Saint-Louis)"
  expression11 = r"(?i)(?:\bMatam\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Matam)"
  expression12 = r"(?i)(?:\bSédhiou\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Sédhiou)"
  expression13 = r"(?i)(?:\bKédougou\D{0,20})([0-9][0-9,]*)[^.,]|([0-9][0-9,]*)[^.,](?:\D{0,20}Kédougou)"

  nbCasDkr = re.findall(expression, text)
  if nbCasDkr == []:
    nb_cas_dakar = [0]
  else:
    dkr_str = str(nbCasDkr)
    nb_cas_dakar = re.findall(r'\d+',dkr_str)

  nbCasTh = re.findall(expression1, text)
  if nbCasTh == []:
    nb_cas_thies = [0]
  else:
    th_str = str(nbCasTh)
    nb_cas_thies == re.findall(r'\d+',th_str)

  nbCasTb = re.findall(expression2, text)
  if nbCasTb == []:
    nb_cas_touba = [0]
  else:
    tb_str = str(nbCasTb)
    nb_cas_touba = re.findall(r'\d+',tb_str)
  
  nbCasDbl = re.findall(expression3, text)
  if nbCasDbl == []:
    nb_cas_diourbel = [0]
  else:
    dbl_str = str(nbCasDbl)
    nb_cas_diourbel = re.findall(r'\d+',dbl_str)

  nbCasFtk = re.findall(expression4, text)
  if nbCasFtk == []:
    nb_cas_fatick = [0]
  else:
    ftk_str = str(nbCasFtk)
    nb_cas_fatick = re.findall(r'\d+',ftk_str)

  nbCasKlk = re.findall(expression5, text)
  if nbCasKlk == []:
    nb_cas_kaolack = [0]
  else:
    klk_str = str(nbCasKlk)
    nb_cas_kaolack = re.findall(r'\d+',klk_str)

  nbCasKfr = re.findall(expression6, text)
  if nbCasKfr == []:
    nb_cas_kaffrine = [0]
  else:
    kfr_str = str(nbCasKfr)
    nb_cas_kaffrine = re.findall(r'\d+',kfr_str)

  nbCasKld = re.findall(expression7, text)
  if nbCasKld == []:
    nb_cas_kolda = [0]
  else:
    kld_str = str(nbCasKld)
    nb_cas_kolda = re.findall(r'\d+',kld_str)

  nbCasTmb = re.findall(expression8, text)
  if nbCasTmb == []:
    nb_cas_tamba = [0]
  else:
    tmb_str = str(nbCasTmb)
    nb_cas_tamba = re.findall(r'\d+',tmb_str)

  nbCasZig = re.findall(expression9, text)
  if nbCasZig == []:
    nb_cas_ziguinchor = [0]
  else:
    zig_str = str(nbCasZig)
    nb_cas_ziguinchor = re.findall(r'\d+',zig_str)

  nbCasSl = re.findall(expression10, text)
  if nbCasSl == []:
    nb_cas_saintl = [0]
  else:
    sl_str = str(nbCasSl)
    nb_cas_saintl = re.findall(r'\d+',sl_str)

  nbCasMtm = re.findall(expression11, text)
  if nbCasMtm == []:
    nb_cas_matam = [0]
  else:
    mtm_str = str(nbCasMtm)
    nb_cas_matam = re.findall(r'\d+',mtm_str)

  nbCasSdh = re.findall(expression12, text)
  if nbCasSdh == []:
    nb_cas_sedhiou = [0]
  else:
    sdh_str = str(nbCasSdh)
    nb_cas_sedhiou = re.findall(r'\d+',sdh_str)

  nbCasKdg = re.findall(expression13, text)
  if nbCasKdg == []:
    nb_cas_kedougou = [0]
  else:
    kdg_str = str(nbCasKdg)
    nb_cas_kedougou = re.findall(r'\d+',kdg_str)
  
  # PUTTING DATA IN JSON OBJECT
  json_data = {}
  json_data[pdf_path] = {
    'date' : date,
    'casPositifs' : cas_positifs_nums[0],
    'casImportes' : cas_importes_nums[0],
    'casContacts' : cas_contacts_nums[0],
    'testRealises': cas_test_nums[0],
    'sousTraitement': cas_sous_traitement_nums[0],
    #'casContactSuivis': cas_contacts_suivis_nums[0],
    'casCommunautaires': cas_communautaires_nums[0],
    'casGueris': cas_gueris_nums[0],
    'deces' : cas_deces_nums[0],
    'localites': [{
      'Dakar' : int(nb_cas_dakar[0]),
      'Thies' : int(nb_cas_thies[0]),
      'Diourbel' : int(nb_cas_diourbel[0]),
      'Fatick' : int(nb_cas_fatick[0]),
      'Kaolack' : int(nb_cas_kaolack[0]),
      'Kaffrine' : int(nb_cas_kaffrine[0]),
      'Touba' : int(nb_cas_touba[0]),
      'Kolda' : int(nb_cas_kolda[0]),
      'Tamba': int(nb_cas_tamba[0]),
      'Ziguinchor': int(nb_cas_ziguinchor[0]),
      'Saint-Louis': int(nb_cas_saintl[0]),
      'Matam': int(nb_cas_matam[0]),
      'Sedhiou': int(nb_cas_sedhiou[0]),
      'Kedougou': int(nb_cas_kedougou[0])
    }]
  }
  tabJson.append(json_data[pdf_path])
print('FILES CREATED', tabJson)
  
  
#res  = set(tabJson)
# GROUP ALL OBJECTS HAVING SAME MONTH
values = set(map(lambda x:x['date'][3:12], tabJson))
newlist = [[y for y in tabJson if y['date'][3:12]==x] for x in values]

#newlistss = [newlist[0]['date']]
#for e in newlist:
  #if e not in newlistss:
    #newlistss.append(e)
    
# CREATING JSON OBJECTS TO DUMP ON JSON FILE FOR EACH MONTH
#print('=========MONTH========', tab_month)
for i in newlist:
      toto = i[0]['date'][3:12]
      txtFile = toto.replace('/', '-')
      if txtFile:
        with open(str(txtFile)+'.json', 'w', encoding='utf-8') as f:
          json.dump(i, f, ensure_ascii=False, indent=4)
        f.close()
# MOVE ALL JSON FILE IN JSON FOLDER
for f in glob.glob('*.json'):
    shutil.move(f, 'JSON')
#IL NE RESTE QU'A TRADUIRE LES TEXTES PRINT DANS LA CONSOLE EN JSON AVEC LES CHAMPS ENUMERES DANS LE DOCUMENT DU PROF
print('-----------ACQUISITION ENDED SUCCESSFULLY-----------')
