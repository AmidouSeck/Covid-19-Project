from typing import Set
from pandas.core.construction import is_empty_data
import requests
import json
import os
#ßimport PyPDF2
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
  

    regions=['Dakar','Thiés','Diourbel','Fatick','Kaolack','Kaffrine','Touba','Kolda','Tamba','Ziguinchor','Saint-Louis','Matam','Sédhiou']
    regions_dict = {}
    for region in regions:
        result = re.search(f"(.?({region}).?,|.?({region}).?;|\d+.a.*?({region}))",text,re.IGNORECASE)
        #result = re.search(f".*?({region}).*?,|.*?({region}).*?;",text,re.IGNORECASE)
        chiffre = 0
        if result is None:
            chiffre = 0
        else:
            result_chiffre = re.search("((\d+))",result.group(0))
            if result_chiffre is not None:
                chiffre = int(result_chiffre.group(0))
                regions_dict[region] = chiffre
    print('AAAAAAAAAAAAA',regions_dict)



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
  cas_dakar = re.search(r'(\w+\s+){0,30}Dakar(\w+\s+){0,30}', text, re.IGNORECASE)
  if cas_dakar:
    #print(cas_dakar.group(0))
    dakar_num = str(cas_dakar.group(0))
    cas_dakar_nums = [int(s) for s in dakar_num.split() if s.isdigit()]
    if cas_dakar_nums == []:
      cas_dakar_nums = [0]
    #else: cas_deces_nums = [0]
    #print(cas_dakar_nums)
  else: cas_dakar_nums = [0]

  cas_thies = re.search(r'(\w+\s+){0,30}Thiès(\w+\s+){0,30}', text, re.IGNORECASE)
  if cas_thies:
    print(cas_thies.group(0))
    thies_num = str(cas_thies.group(0))
    cas_thies_nums = [int(s) for s in thies_num.split() if s.isdigit()]
    if cas_thies_nums == []:
      cas_thies_nums = [0]
    #else: cas_deces_nums = [0]
    #print(cas_thies_nums)
  else: cas_thies_nums = [0]

  cas_kolda = re.search(r'(\w+\s+){0,30}Kolda(\w+\s+){0,30}', text, re.IGNORECASE)
  if cas_kolda:
    #print(cas_kolda.group(0))
    kolda_num = str(cas_kolda.group(0))
    cas_kolda_nums = [int(s) for s in kolda_num.split() if s.isdigit()]
    if cas_kolda_nums == []:
      cas_kolda_nums = [0]
    #else: cas_deces_nums = [0]
    #print(cas_kolda_nums)
  else: cas_kolda_nums = [0]

  cas_louga = re.search(r'(\w+\s+){0,30}Louga(\w+\s+){0,30}', text, re.IGNORECASE)
  if cas_louga:
    #print(cas_louga.group(0))
    louga_num = str(cas_louga.group(0))
    cas_louga_nums = [int(s) for s in louga_num.split() if s.isdigit()]
    if cas_louga_nums == []:
      cas_louga_nums = [0]
    #else: cas_deces_nums = [0]
    #print(cas_louga_nums)
  else: cas_louga_nums = [0]

  cas_touba = re.search(r'(\w+\s+){0,30}Touba(\w+\s+){0,30}', text, re.IGNORECASE)
  if cas_touba:
    #print(cas_touba.group(0))
    touba_num = str(cas_touba.group(0))
    cas_touba_nums = [int(s) for s in touba_num.split() if s.isdigit()]
    if cas_touba_nums == []:
      cas_touba_nums = [0]
    #else: cas_deces_nums = [0]
    #print(cas_touba_nums)
  else: cas_touba_nums = [0]

  cas_diourbel = re.search(r'(\w+\s+){0,30}Diourbel(\w+\s+){0,30}', text, re.IGNORECASE)
  if cas_diourbel:
    #print(cas_diourbel.group(0))
    diourbel_num = str(cas_diourbel.group(0))
    if cas_diourbel.group(0) is not None:
      cas_diourbel_nums = [int(s) for s in diourbel_num.split() if s.isdigit()]
      if cas_diourbel_nums == []:
            cas_diourbel_nums = [0]
    #else: cas_deces_nums = [0]
    #print(cas_diourbel_nums)
  else: cas_diourbel_nums = [0]

  cas_fatick = re.search(r'(\w+\s+){0,30}Fatick(\w+\s+){0,30}', text, re.IGNORECASE)
  if cas_fatick:
    #print(cas_fatick.group(0))
    fatick_num = str(cas_fatick.group(0))
    if cas_fatick.group(0) is not None:
      cas_fatick_nums = [int(s) for s in fatick_num.split() if s.isdigit()]
      if cas_fatick_nums == []:
            cas_fatick_nums = [0]
    #else: cas_deces_nums = [0]
    #print(cas_fatick_nums)
  else: cas_fatick_nums = [0]

  cas_matam = re.search(r'(\w+\s+){0,30}Matam(\w+\s+){0,30}', text, re.IGNORECASE)
  if cas_matam:
    #print(cas_matam.group(0))
    matam_num = str(cas_matam.group(0))
    if cas_matam.group(0) is not None:
      cas_matam_nums = [int(s) for s in matam_num.split() if s.isdigit()]
      if cas_matam_nums == []:
            cas_matam_nums = [0]
    #else: cas_deces_nums = [0]
    #print(cas_matam_nums)
  else: cas_matam_nums = [0]

  cas_kaolack = re.search(r'(\w+\s+){0,30}Kaolack(\w+\s+){0,30}', text, re.IGNORECASE)
  if cas_kaolack:
    #print(cas_kaolack.group(0))
    kaolack_num = str(cas_kaolack.group(0))
    if cas_kaolack.group(0) is not None:
      cas_kaolack_nums = [int(s) for s in kaolack_num.split() if s.isdigit()]
      if cas_kaolack_nums == []:
            cas_kaolack_nums = [0]
    #else: cas_deces_nums = [0]
    #print(cas_kaolack_nums)
  else: cas_kaolack_nums = [0]

  cas_kaffrine = re.search(r'(\w+\s+){0,30}Kaffrine(\w+\s+){0,30}', text, re.IGNORECASE)
  if cas_kaffrine:
    #print(cas_kaffrine.group(0))
    kaffrine_num = str(cas_kaffrine.group(0))
    if cas_kaffrine.group(0) is not None:
      cas_kaffrine_nums = [int(s) for s in kaffrine_num.split() if s.isdigit()]
      if cas_kaffrine_nums == []:
            cas_kaffrine_nums = [0]
    #else: cas_deces_nums = [0]
    #print(cas_kaffrine_nums)
  else: cas_kaffrine_nums = [0]

  cas_tamba = re.search(r'(\w+\s+){0,30}Tamba(\w+\s+){0,30}', text, re.IGNORECASE)
  if cas_tamba:
    #print(cas_tamba.group(0))
    tamba_num = str(cas_tamba.group(0))
    if cas_tamba.group(0) is not None:
      cas_tamba_nums = [int(s) for s in tamba_num.split() if s.isdigit()]
      if cas_tamba_nums == []:
            cas_tamba_nums = [0]
    #else: cas_deces_nums = [0]
    #print(cas_tamba_nums)
  else: cas_tamba_nums = [0]

  cas_ziguinchor = re.search(r'(\w+\s+){0,30}Ziguinchor(\w+\s+){0,30}', text, re.IGNORECASE)
  if cas_ziguinchor:
    #print(cas_ziguinchor.group(0))
    ziguinchor_num = str(cas_ziguinchor.group(0))
    if cas_ziguinchor.group(0) is not None:
      cas_ziguinchor_nums = [int(s) for s in ziguinchor_num.split() if s.isdigit()]
      if cas_ziguinchor_nums == []:
            cas_ziguinchor_nums = [0]
    #else: cas_deces_nums = [0]
    #print(cas_ziguinchor_nums)
  else: cas_ziguinchor_nums = [0]

  cas_saintlouis = re.search(r'(\w+\s+){0,30}Saint-Louis(\w+\s+){0,30}', text, re.IGNORECASE)
  if cas_saintlouis:
    #print(cas_saintlouis.group(0))
    saintlouis_num = str(cas_saintlouis.group(0))
    if cas_saintlouis.group(0) is not None:
      cas_saintlouis_nums = [int(s) for s in saintlouis_num.split() if s.isdigit()]
      if cas_saintlouis_nums == []:
            cas_saintlouis_nums = [0]
    #else: cas_deces_nums = [0]
    #print(cas_saintlouis_nums)
  else: cas_saintlouis_nums = [0]

  cas_sedhiou = re.search(r'(\w+\s+){0,30}Sédhiou(\w+\s+){0,30}', text, re.IGNORECASE)
  if cas_sedhiou:
    #print(cas_sedhiou.group(0))
    sedhiou_num = str(cas_sedhiou.group(0))
    if cas_sedhiou.group(0) is not None:
      cas_sedhiou_nums = [int(s) for s in sedhiou_num.split() if s.isdigit()]
      if cas_sedhiou_nums == []:
            cas_sedhiou_nums = [0]
    #else: cas_deces_nums = [0]
    #print(cas_sedhiou_nums)
  else: cas_sedhiou_nums = [0]
  
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
      'Dakar' : cas_dakar_nums[0],
      'Thies' : cas_thies_nums[0],
      'Diourbel' : cas_diourbel_nums[0],
      'Fatick' : cas_fatick_nums[0],
      'Kaolack' : cas_kaolack_nums[0],
      'Kaffrine' : cas_kaffrine_nums[0],
      'Touba' : cas_touba_nums[0],
      'Kolda' : cas_kolda_nums[0],
      'Tamba': cas_tamba_nums[0],
      'Ziguinchor': cas_ziguinchor_nums[0],
      'Saint-Louis': cas_saintlouis_nums[0],
      'Matam': cas_matam_nums[0],
      'Sedhiou': cas_sedhiou_nums[0]
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