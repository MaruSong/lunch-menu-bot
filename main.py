# this file controls the whole procedure

import pickle 
import datetime
import calendar
import os
import logging
import parser
import pdfminer
import request
import send_message
import zulip

logging.basicConfig(filename = 'logfile.log', level=logging.DEBUG, format = '%(asctime)s - %(message)s')
logging.info("\n")

# Weekend exception
my_date = datetime.date.today()
dow = calendar.day_name[my_date.weekday()]
if dow == "Sunday" or dow == "Saturday":
    logging.info('No lunch on %s', dow)
    exit()

today = datetime.datetime.today()
# to make h/m/s 0
int_today = datetime.datetime.strptime('{}/{}/{}'.format(today.day, today.month, today.year),\
                                       '%d/%m/%Y')
menufile = 'menu_data/' + int_today.strftime("%s") + '.pickle'

try:
    with open(menufile, 'rb') as f:
        menu = pickle.load(f)
    if menu[1] == ' ' and menu[2] == ' ' and menu[3] == ' ':
        logging.info('Menu blocks of today are empty. \
                      Probably institute cafeteria is closed today.')
        exit()
    try:
        logging.info('Zulip message has been sent during the first try')
        send_message.send_message(menu)
    except (zulip.ConfigNotFoundError):
        logging.info('zuliprc not found')
        exit()
    logging.info('%s has been deleted', menufile)
    os.remove(menufile)
    exit()
except (FileNotFoundError):
    logging.info("Today's menufile not found")

    logging.info('run request.py')
    try:
        request.request('cookie.dat')
    except (AssertionError):
        logging.info('Wrong cookie')
        exit()
    except (FileNotFoundError):
        logging.info('cookie.dat not found')
        exit()

    logging.info('run parser.py')
    try:
        parser.parser()
    except (pdfminer.pdfparser.PDFSyntaxError):
        logging.info('Wrong PDF file')
        exit()

# Repeat the procedure after executing request.py and parser.py
try:
    with open(menufile, 'rb') as f:
        menu = pickle.load(f)
    if menu[1] == ' ' and menu[2] == ' ' and menu[3] == ' ':
        logging.info('Menu blocks of today are empty. \
                      Probably institute cafeteria is closed today.')
        exit()
    try:
        logging.info('Zulip message has been sent during the first try')
        send_message.send_message(menu)
    except (zulip.ConfigNotFoundError):
        logging.info('zuliprc not found')
        exit()
    logging.info('%s has been deleted', menufile)
    os.remove(menufile)
    exit()
except (FileNotFoundError):
    logging.info("Today's menufile still not found. Today is probably a holiday")
