__author__ = 'alex'

import requests
from lxml import etree
from lxml import objectify

class GrammarChecker():

    USELESS_RULES = ["WHITESPACE_RULE", "EN_UNPAIRED_BRACKETS", "EN_QUOTES", 'COMMA_PARENTHESIS_WHITESPACE']
    USELESS_CATEGORY = ["Capitalization"]

    def __init__(self, url, lang='en-US'):
        self.url = url
        self.language = lang
        self.problemsXML = None
        self.text = None

    def post_check(self,text=None):
        payload = {'language': self.language, 'text': text}
        r = requests.post(self.url, data=payload)
        if r.status_code == 200:
            self.problemsXML = r.content
        else:
            self.problemsXML = None

    def getFilteredProblemList(self):
        problem_list = []
        if self.problemsXML:
            root = objectify.fromstring(self.problemsXML)
            if hasattr(root, 'error'):
                for e in root.error:
                    if e.attrib['category'] not in self.USELESS_CATEGORY and e.attrib['ruleId'] not in self.USELESS_RULES \
                        and e.attrib['errorlength'] != '2' and e.attrib['replacements'] != '':
                        if "gmail" not in e.attrib['context'].lower() and u'\ufffd' not in e.attrib['context']:
                            problem_list.append(e.attrib)
        return problem_list

