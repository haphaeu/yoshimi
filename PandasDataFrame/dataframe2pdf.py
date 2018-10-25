# -*- coding: utf-8 -*-
"""

DataFrame to PDF

Save the contents of a pandas DataFrame into a PDF file.


[1] https://stackoverflow.com/questions/51973991/saving-pandas-dataframe-into-pdf-file-format-without-pdfkit
[2] https://stackoverflow.com/questions/50807744/apply-css-class-to-pandas-dataframe-using-to-html

Created on Mon Oct 15 15:31:04 2018
@author: rarossi
"""

import pandas as pd
from PyQt4.QtGui import QTextDocument, QPrinter, QApplication
import sys
import os
app = QApplication(sys.argv)


# Read the DataFrame
df = pd.read_table('00_45m/Results.txt')


# create a basic CSS style for the table
with open('_tmp_df_style.css', 'w') as f:
    f.write('''/* includes alternating gray and white with on-hover color */

.mystyle {
    font-size: 8pt;
    font-family: Arial;
    border: 1px solid silver;
    border-collapse: collapse;

}

.mystyle td, th {
    padding: 5px;
}
''')


# Create a html file
html_string = '''
<html>
  <head><title>HTML Pandas Dataframe with CSS</title></head>
  <link rel="stylesheet" type="text/css" href="_tmp_df_style.css"/>
  <body>
    {table}
  </body>
</html>.
'''
with open('_tmp_results.html', 'w') as f:
    f.write(html_string.format(table=df.to_html(
                    classes='mystyle',
                    index=False,
                    float_format='%.1f',
                    # Case by case specific formatting:
                    formatters={'Max UR Line1': lambda x: '%.2f' % x})))


# Create a document and print it to pdf
doc = QTextDocument()
location = '_tmp_results.html'
html = open(location).read()
doc.setHtml(html)
printer = QPrinter()
printer.setOutputFileName('results.pdf')
printer.setOutputFormat(QPrinter.PdfFormat)
printer.setPageSize(QPrinter.A3)
printer.setOrientation(QPrinter.Landscape)
printer.setPageMargins(10, 10, 10, 10, QPrinter.Millimeter)
doc.print_(printer)

# Clean up
os.remove('_tmp_df_style.css')
os.remove('_tmp_results.html')
