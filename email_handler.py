__author__ = 'alex'

from gmail import Gmail
import datetime
import re


class EmailHandler():

    def __init__(self, username, password ):
        self.g = Gmail()
        self.g.login(username, password)

    def logout(self):
        self.g.logout()

    def get_sent_mail(self):
        return self.g.sent_mail()


    def store_emails(self, start_date , store_at):
        '''
            Download the emails and store them in a plain text file separated by "===" string

        '''
        all_emails = []
        for message in self.get_sent_mail().mail(after=start_date):
            message.fetch()
            for line in message.body.split('\r\n'):
                #do some cleaning before storing the emails
                if "-------- Original Message --------" in line:
                    break
                if "---------- Forwarded message ----------" in line:
                    break
                line = re.sub("\d+", "", line)
                line = re.sub('<[^>]*>', '', line)
                if line and line[0] != '>' and line[0] != '<' : #ignore quoting previous email or http links
                    all_emails.append(line)
            all_emails.append("="*30)
        #save the emails
        f = open(store_at,"wr+")
        f.write('\n'.join(all_emails))
        f.close()
        print "Done getting and storing emails"

