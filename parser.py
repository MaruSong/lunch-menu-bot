from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
import pickle 
import datetime
import calendar

def parser():
    # monday = 0, ..., friday = 4
    Day_coord = {0:[223, 78], 1:[318, 78], 2:[414, 78],
                3:[510, 78], 4:[605, 78]}
    
    # y length of menu pdf file
    ylength = 841.92
    
    fp = open('menu_data/menu.pdf', 'rb')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    laparams.word_margin = 0.1 # default 0.1
    laparams.line_margin = 0.1 # default 0.5
    # small char_margin in order to prevent unexpected text chunks
    # e.g. a chunk with MO and MenuI of MO together
    laparams.char_margin = 0.05 # default 2.0
    
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PDFPage.get_pages(fp)
    for p, page in enumerate(pages):
    
        menuI = {0:'', 1:'', 2:'', 3:'', 4:''}
        menuII = {0:'', 1:'', 2:'', 3:'', 4:''}
        special = {0:'', 1:'', 2:'', 3:'', 4:''}
        week = {'week':''}
    
        interpreter.process_page(page)
        layout = device.get_result()
        for ele in layout:
            if isinstance(ele, LTTextBox):
    
                # parse week
                if ((ele.y0 > ylength - (120 + 60) and ele.y1 < ylength - 120) and
                    (ele.x0 > 30 and ele.x1 < 30 + 300)):
                    week['week'] += ele.get_text().replace(' \n', ' ').replace('\n', ' ')
    
                # parse menu
                for day in Day_coord.keys():
                    if (ele.y0 > ylength - (Day_coord[day][0] + Day_coord[day][1]) and
                        ele.y1 < ylength - Day_coord[day][0]):
                        # MenuI
                        if (ele.x0 > 82 and ele.x1 < 82 + 150):
                            menuI[day] += ele.get_text().replace(' \n', ' ').replace('\n', ' ')
                        # MenuII
                        elif (ele.x0 > 232 and ele.x1 < 232 + 150):
                            menuII[day] += ele.get_text().replace(' \n', ' ').replace('\n', ' ')
                        # Special
                        elif (ele.x0 > 374 and ele.x1 < 374+185):
                            special[day] += ele.get_text().replace(' \n', ' ').replace('\n', ' ')
    
        final = [menuI, menuII, special]
    
        # ['day', 'month', 'year']
        day_from = week['week'].split()[1].split('.')
        day_to = week['week'].split()[3].split('.')
        if day_from[2] == '':
            day_from[2] = day_to[2]
    
        # convert day_... to datetime format
        datetime_from = datetime.datetime.strptime('{}/{}/20{}'.format(day_from[0], day_from[1], day_from[2]),\
                                                   '%d/%m/%Y')
        datetime_to = datetime.datetime.strptime('{}/{}/20{}'.format(day_to[0], day_to[1], day_to[2]),\
                                                 '%d/%m/%Y')
    
        weekday = datetime_from.weekday() - 1
        today = datetime_from
        while weekday < datetime_to.weekday():
            weekday += 1
            if menuI[weekday] == ' ' and menuII[weekday] == ' ' and special[weekday] == ' ':
                continue
            final = [today.strftime("%d-%b-%Y"), menuI[weekday], menuII[weekday], special[weekday]]
            with open('menu_data/' + today.strftime("%s") + '.pickle', 'wb') as f:
                    pickle.dump(final, f, pickle.HIGHEST_PROTOCOL)
            today += datetime.timedelta(days = 1)

    fp.close()

# a standalone run prints the position and the texts of textboxes
if __name__ == "__main__":
    fp = open('menu_data/menu.pdf', 'rb')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    laparams.word_margin = 0.1 # default 0.1
    laparams.line_margin = 0.1 # default 0.5
    laparams.char_margin = 0.05 # default 2.0
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PDFPage.get_pages(fp)
    
    for page in pages:
        interpreter.process_page(page)
        layout = device.get_result()
        for ele in layout:
            if isinstance(ele, LTTextBox):
                x0, x1, y0, y1, text = \
                        ele.x0, ele.x1, ele.y0, ele.y1, ele.get_text()
                print('position: %r text: %s' % ((x0, x1, y0, y1), text))
