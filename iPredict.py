from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm, Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer, SimpleField
from time import sleep


ACCESS_ID ='access id'
SECRET_KEY = 'secret key'
HOST = 'mechanicalturk.sandbox.amazonaws.com'
 
mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)
 
title = 'Sports questions'
description = ('Answer questions about your knowledge of sports')
keywords = 'sports, transcription, question'

title2 = 'Sports prediction'
description2 = ('Answer questions and make a prediction')
keywords2 = 'sports, prediction, question'
 
ratings =[('Nothing','-2'),
         ('A little','-1'),
         ('Some','0'),
         ('A lot','1'),
         ('Everything','2')]
         
yesNo = [('No', '0'),
        ('Yes','1')]
        
        
tweet = 'Team A and Team B'

def get_all_reviewable_hits(mtc):
    page_size = 50
    hits = mtc.get_reviewable_hits(page_size=page_size)
    print "Total results to fetch %s " % hits.TotalNumResults
    print "Request hits page %i" % 1
    total_pages = float(hits.TotalNumResults)/page_size
    int_total= int(total_pages)
    if(total_pages-int_total>0):
        total_pages = int_total+1
    else:
        total_pages = int_total
    pn = 1
    while pn < total_pages:
        pn = pn + 1
        print "Request hits page %i" % pn
        temp_hits = mtc.get_reviewable_hits(page_size=page_size,page_number=pn)
        hits.extend(temp_hits)
    return hits
 
#---------------  BUILD OVERVIEW 1 -------------------
 
overview = Overview()
overview.append_field('Title', 'How much do you know about...')
 
#---------------  BUILD QUESTION 1 -------------------
 
qc1 = QuestionContent()
qc1.append_field('Title','...NBA?')
 
fta1 = SelectionAnswer(min=1, max=1,style='radiobutton',
                      selections=ratings,
                      type='text',
                      other=False)
 
q1 = Question(identifier='design',
              content=qc1,
              answer_spec=AnswerSpecification(fta1),
              is_required=True)
              
#---------------  BUILD QUESTION 2 -------------------
 
qc2 = QuestionContent()
qc2.append_field('Title','...NFL?')
 
fta2 = SelectionAnswer(min=1, max=1,style='radiobutton',
                      selections=ratings,
                      type='text',
                      other=False)
 
q2 = Question(identifier='design',
              content=qc2,
              answer_spec=AnswerSpecification(fta2),
              is_required=True)
 
#---------------  BUILD TWEET INFO -------------------
#---------------  BUILD QUESTION 3 -------------------

qc3 = QuestionContent()
tweet = tweet + '\nAre there teams mentioned?'
qc3.append_field('Title', value= tweet)
 
fta3 = SelectionAnswer(min=1, max=1,style='dropdown',
                      selections=yesNo,
                      type='text',
                      other=False)
 
q3 = Question(identifier='design',
              content=qc3,
              answer_spec=AnswerSpecification(fta3),
              is_required=True)
 
 #---------------  BUILD QUESTION 4 -------------------
 
qc4 = QuestionContent()
qc4.append_field('Title','If there are teams, enter first team. Otherwise, enter N/A.')
 
fta4 = FreeTextAnswer()
 
q4 = Question(identifier="team1",
              content=qc4,
              answer_spec=AnswerSpecification(fta4),
              is_required=True)

 #---------------  BUILD QUESTION 5 -------------------
 
qc5 = QuestionContent()
qc5.append_field('Title','If there are teams, enter second team. Otherwise, enter N/A')
 
fta5 = FreeTextAnswer()
 
q5 = Question(identifier="team2",
              content=qc5,
              answer_spec=AnswerSpecification(fta5),
              is_required=True)
			  
			  
#---------------  BUILD QUESTION 6 -------------------
 
qc6 = QuestionContent()
qc6.append_field('Title','If there are teams, enter sport they play. Otherwise, enter N/A')
 
fta6 = FreeTextAnswer()
 
q6 = Question(identifier="sport",
              content=qc6,
              answer_spec=AnswerSpecification(fta6),
              is_required=True)
 
#--------------- BUILD THE QUESTION FORM -------------------
 
question_form1 = QuestionForm()
question_form1.append(overview)
question_form1.append(q1)
question_form1.append(q2)
question_form1.append(q3)
question_form1.append(q4)
question_form1.append(q5)
question_form1.append(q6)
 
#--------------- CREATE THE HIT -------------------
 
hit1 = mtc.create_hit(questions=question_form1,
               max_assignments=1,
               title=title,
               description=description,
               keywords=keywords,
               duration = 60*5,
               reward=0.05)

hit1_id=hit1[0].HITId

#WAIT UNTIL ENOUGH RESPONSES HAVE BEEN GIVEN

while True:
    assignments1 = mtc.get_assignments(hit1_id)
    num1 = int(assignments1.NumResults)
    if num1 < 1:
        print 'Not done1'
        continue
    else:
        break
    
print 'Done1'


#---------------  BUILD OVERVIEW 2 -------------------
 
overview2 = Overview()
overview2.append_field('Title', 'How much do you know about...')
 
#---------------  BUILD QUESTION 1 -------------------
 
qc7 = QuestionContent()
sport = 'NBA'
question = '...' + sport + '?'
qc7.append_field('Title',value=question)
 
fta7 = SelectionAnswer(min=1, max=1,style='radiobutton',
                      selections=ratings,
                      type='text',
                      other=False)
 
q7 = Question(identifier='design',
              content=qc7,
              answer_spec=AnswerSpecification(fta7),
              is_required=True)
 
#---------------  BUILD TWEET INFO -------------------
#---------------  BUILD QUESTION 3 -------------------

qc8 = QuestionContent()
team1 = 'Team A'
team2 = 'Team B'
teams = [(str(team1),'0'), (str(team2),'1')]
predictionTeams = team1 + ' vs ' + team2 + '\n\nWho will win?'
qc8.append_field('Title', value= predictionTeams)
 
fta8 = SelectionAnswer(min=1,max=1,style='radiobutton',
                      selections=teams,
                      type='text',
                      other=False)
 
q8 = Question(identifier='design',
              content=qc8,
              answer_spec=AnswerSpecification(fta8),
              is_required=True)
 
#--------------- BUILD THE QUESTION FORM -------------------
 
question_form2 = QuestionForm()
question_form2.append(overview2)
question_form2.append(q7)
question_form2.append(q8)
 
#--------------- CREATE THE HIT -------------------
 
hit2 = mtc.create_hit(questions=question_form2,
               max_assignments=1,
               title=title2,
               description=description2,
               keywords=keywords2,
               duration = 60*5,
               reward=0.05)

hit2_id=hit2[0].HITId

#WAIT UNTIL ENOUGH RESPONSES HAVE BEEN GIVEN

while True:
    assignments2 = mtc.get_assignments(hit2_id)
    num2 = int(assignments2.NumResults)
    if num2 < 1:
        print 'Not done2'
        continue
    else:
        break
    
print 'Done2'


