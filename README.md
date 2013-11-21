===========
EmailGrammar
============

Will check the grammar of your SENT messages in a Gmail account.
Just experimental project testing some ideas. Very raw and needs some extra work to be more useful (check TODO section)
Based on PyGmail lib and LanguageTool server


### Prerequisites:

Download and start your own instance of LanguageTool server for grammar checking
run as :
    java -cp languagetool-server.jar org.languagetool.server.HTTPServer --port 8081

or either use the demo server at https://languagetool.org:8081/ (will be slow , because of 20req/min per IP)



the python requirements are in email_grammar.req:
argparse==1.2.1
lxml==3.2.3
pygmail==0.0.5.4
requests==2.0.1
wsgiref==0.1.2


Fill in all the necessary configuration options in emailgrammar.cfg.
and run
    python start_processing.py

The process to get the email takes a while if it's more that couple of months of emails to download.


##TODO:

1)LanguageTool grammar checker is not perfect as such will flag brands,places,names as errors
What can be improved is to download the gmail contacts and remove them from the list of errors.
Also get a brands databases to filter them out from the errors list
2)Languages , EN_US and EN_GB are quite different and if you mix them around in your email you going to get false positive.
  again we can check for the other one in the end.

