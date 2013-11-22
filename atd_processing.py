__author__ = 'alex'

import requests
from collections import Counter
from lxml import objectify
from xml.etree import ElementTree


class Error:


    """ AtD Error Object
    These are to be returned in a list by checkText()
    Available properties are: string, description, precontext, type, url
    and suggestions.

    Look at http://www.afterthedeadline.com/api.slp for more information."""
    def __init__(self, e):
        self.string = e.find('string').text
        self.description = e.find('description').text
        self.precontext = e.find('precontext').text
        self.type = e.find('type').text
        if not e.find('url') is None:
            self.url = e.find('url').text
        else:
            self.url = ""
        if not e.find('suggestions') is None:
            self.suggestions = map(lambda o: o.text,
                                   e.find('suggestions').findall('option'))
        else:
            self.suggestions = []
    def __str__(self):
        return "%s (%s)" % (self.string, self.description)


if __name__ == "__main__":
    '''
        Some simple script to test a different backend than the LanguageTool
        Using After The Dark - AtD as grammar server


        Error class was copied from the excellent after_the_dark python wrapper
        https://bitbucket.org/miguelventura/after_the_deadline
        By  Miguel Ventura


    '''
    messages_str = open("myemails.txt", "r+").readlines()
    payload = {'data': "\n".join(messages_str)}
    r = requests.post('http://127.0.0.1:1049/checkDocument?', data=payload)

    e = ElementTree.fromstring(r.content)
    errs = e.findall('message')
    if len(errs) > 0:
        raise Exception('Server returned an error: %s' % errs[0].text)

    errors_list=  map(lambda err: Error(err), e.findall('error'))
    problems_counter = Counter()
    print errors_list

    for e in errors_list:
        problems_counter[e.string +" -- " + e.description +"--" +  e.type] += 1

    f = open("results_atd.txt","w+")
    #store 100 most comment errors
    for item in problems_counter.most_common(300):
        try:
            f.write("%s %d \n" % item)
        except:
            pass
    f.close()
