__author__ = 'alex'

from check_grammar import GrammarChecker
from email_handler import EmailHandler
import datetime
import re
import ConfigParser
from collections import Counter
import time


if __name__ == "__main__":

    EMAILS_FILE = "myemails.txt"

    #load configuration
    config = ConfigParser.RawConfigParser()
    config.read('emailgrammar.cfg')
    login = config.get("Gmail Credentials",'login')
    password = config.get("Gmail Credentials",'password')
    dates = config.get("Gmail Credentials",'get_emails_starting').split('-')
    start_date=datetime.date(int(dates[0]),int(dates[1]), int(dates[2]) )
    language = config.get("LanguageTool",'language')
    server_url = config.get("LanguageTool",'server_url')

    #get the emails
    e_handler = EmailHandler(login, password)
    e_handler.store_emails(start_date, EMAILS_FILE)
    e_handler.logout()

    #check the grammar and store the results
    gcheck = GrammarChecker(server_url, language)
    messages_str = open(EMAILS_FILE, "r+").readlines()
    new_message = []
    c = Counter()
    lin_sep = "="*30
    for m in messages_str:
        if lin_sep not in m and m != "\n" and m != "\r":
            new_message.append(m)
        elif lin_sep in m:
            joined_message = "\n".join(new_message)
            if len(joined_message) < 6: #empty messages
                continue
            gcheck.post_check(joined_message)
            try:
                problems_list = gcheck.getFilteredProblemList()
            except:
                print "Error occurred while checking this email: \n\n %s" % m
                continue
            #if something wrong with the message and too many mistakes(e.g. another language)
            #just ignore it
            if len(new_message)/2.5< len(problems_list):
                new_message = []
                continue
            for e in problems_list:
                error_word = e['context'][int(e['contextoffset']):int(e['contextoffset']) + int(e['errorlength'])]
                c[error_word] += 1
            new_message = []
            #if grammar checker is not using local instance of LanguageTool
            #we are limited to 20 request per ip
            #hence we need to sleep abit each request
            if 'localhost' not in server_url:
                time.sleep(4)

    f = open("results.txt","w+")
    #store 100 most comment errors
    for item in c.most_common(100):
        f.write("%s %d \n" % item)
    f.close()




