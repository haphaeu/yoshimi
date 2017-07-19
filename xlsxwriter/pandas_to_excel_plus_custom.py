# -*- coding: utf-8 -*-
"""

Playing with pandas.DataFrame.to_excel plus some customisation in the spreadsheet.

Created on Wed Jul 19 08:05:12 2017

@author: rarossi
"""


import pandas as pd
import xlsxwriter.utility as xlutil


def into_xl():
    """Creates an excel spreadsheet with results."""
    # Filter out wave direction
    df = pd.read_table('results.txt').groupby(['WaveHs', 'WaveTp']).max().reset_index()
    writer = pd.ExcelWriter('Results.xlsx')
    for i, col in enumerate(df.columns[3:]):
        pv = df.pivot(index='WaveHs', columns='WaveTp', values=col).fillna('na')
        pd.DataFrame(data=[col]).to_excel(writer, sheet_name='Results',  # overkill =P
                                          header=False, index=False, startrow=i*(len(pv)+3))
        pv.to_excel(writer, sheet_name='Results', index_label='Hs\Tp', startrow=1+i*(len(pv)+3))

    workbook = writer.book
    worksheet = writer.sheets['Results']

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})
    bold_borders = workbook.add_format({'bold': True, 'border': True})
    borders = workbook.add_format({'border': True})
    italic = workbook.add_format({'italic': True})

    # Light red fill with dark red text.
    red = workbook.add_format({'bg_color':   '#FFC7CE',
                               'font_color': '#9C0006'})
    # Light yellow fill with dark yellow text.
    yellow = workbook.add_format({'bg_color':   '#FFEB9C',
                                  'font_color': '#9C6500'})
    # Green fill with dark green text.
    green = workbook.add_format({'bg_color':   '#C6EFCE',
                                 'font_color': '#006100'})
    # Blank fill with black text.
    blank = workbook.add_format({'bg_color':   'white',
                                 'font_color': 'black'})

    # Write cells for user input of systems limitations
    limits_col = len(pv.columns) + 2
    worksheet.write(1, limits_col, "AHC System's Limitations", bold)
    worksheet.write(2, limits_col, "Amplitude [m]")
    worksheet.write(2, limits_col+3, "Note: this is amplitude, half of the displacement.", italic)
    worksheet.write(3, limits_col, "Velocity [m/s]")
    worksheet.write(4, limits_col, "Acceleration [m/s²]")
    worksheet.write(2, limits_col+2, 1, yellow)
    worksheet.write(3, limits_col+2, 1, yellow)
    worksheet.write(4, limits_col+2, 1, yellow)

    # Apply a conditional format to the tables.
    height = len(pv)  # height of table
    gap = 3  # gap between tables
    for i in range(3):
        top_rw = 2+i*(height+gap)
        target = xlutil.xl_range_abs(top_rw, 1, top_rw+height-1, len(pv.columns))
        limit = xlutil.xl_rowcol_to_cell(2+i, limits_col+2, row_abs=True, col_abs=True)
        worksheet.conditional_format(target, {'type': 'cell', 'criteria': '==',
                                              'value': '"na"', 'format': blank})
        worksheet.conditional_format(target, {'type': 'cell', 'criteria': '>',
                                              'value': limit, 'format': red})
        worksheet.conditional_format(target, {'type': 'cell', 'criteria': '<=',
                                              'value': limit, 'format': green})

    # Finally create an overall weather window table
    worksheet.write(6, limits_col, "Operability Window", bold)
    worksheet.write(7, limits_col, "Hs\Tp", bold_borders)
    for i, hs in enumerate(pv.index.values):
        rw = 7+i+1
        worksheet.write(rw, limits_col, hs, bold_borders)
        for j, tp in enumerate(pv.columns.values):
            cl = limits_col+j+1
            worksheet.write(7, cl, tp, bold_borders)
            worksheet.write(rw, cl, do_formula(i, j, limits_col, height, gap), borders)
    # and apply green-red formating
    target = xlutil.xl_range_abs(7+1, limits_col+1, 7+height, limits_col+len(pv.columns))
    worksheet.conditional_format(target, {'type': 'cell', 'criteria': '==',
                                          'value': 'TRUE', 'format': green})
    worksheet.conditional_format(target, {'type': 'cell', 'criteria': '==',
                                          'value': 'FALSE', 'format': red})

    writer.save()

def do_formula(i, j, limits_col, height, gap):
    return '=IF({3}="na", "na", AND({3} <= {0}, {4} <= {1}, {5} <= {2}))'.format(
            xlutil.xl_rowcol_to_cell(2, limits_col+2, row_abs=True, col_abs=True),
            xlutil.xl_rowcol_to_cell(3, limits_col+2, row_abs=True, col_abs=True),
            xlutil.xl_rowcol_to_cell(4, limits_col+2, row_abs=True, col_abs=True),
            xlutil.xl_rowcol_to_cell(2+0*(height+gap)+i, 1+j),
            xlutil.xl_rowcol_to_cell(2+1*(height+gap)+i, 1+j),
            xlutil.xl_rowcol_to_cell(2+2*(height+gap)+i, 1+j))

if __name__ == '__main__':
    into_xl()
