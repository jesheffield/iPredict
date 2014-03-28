from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm, Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer, SimpleField
from time import sleep


ACCESS_ID ='access id'
SECRET_KEY = 'key'
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
		 
ratings2 = [('Nothing','1'),
		 ('A little','2'),
		 ('Some','3'),
		 ('A lot','4'),
		 ('Everything','5')]
		 
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
 
q1 = Question(identifier='nba',
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
 
q2 = Question(identifier='nfl',
			  content=qc2,
			  answer_spec=AnswerSpecification(fta2),
			  is_required=True)
 
#---------------  BUILD TWEET INFO -------------------
#---------------  BUILD QUESTION 3 -------------------

qc3 = QuestionContent()
#tweet = tweet + '\nAre there teams mentioned?'
qc3.append_field('Title', value= tweet)
 
fta3 = SelectionAnswer(min=1, max=1,style='dropdown',
					  selections=yesNo,
					  type='text',
					  other=False)
 
q3 = Question(identifier='teams',
			  content=qc3,
			  answer_spec=AnswerSpecification(fta3),
			  is_required=True)
 
 #---------------  BUILD QUESTION 4 -------------------
 
qc4 = QuestionContent()
tweet = tweet + '\n\n\nIf there are teams, enter first team. Otherwise, enter N/A.'
qc4.append_field('Title',value = tweet)
 
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
qc6.append_field('Title','If there are teams, enter league they play in. Otherwise, enter N/A')
 
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
#question_form1.append(q3)
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
		#print 'Not done1'
		continue
	else:
		break
	
print 'Done1'



#Get data from hit1

teamsArray = ['A', 'B']
timesTeamGiven=[3, 5]
sportsArray = ['NBA']
timesSportGiven = [5]

assignments1 = mtc.get_assignments(hit1_id)
answerNum=0
teamsIter = 0
sportsIter = 0
for assignment in assignments1:
	#print "Answers of the worker %s" % assignment.WorkerId
	for question_form_answer in assignment.answers[0]:
		for value in question_form_answer.fields:
			answerNum=answerNum+1
			#print "Answer %s:" % answerNum
			if answerNum == 3 or answerNum == 4:
				teamsIter = 0
				if value not in teamsArray:
					teamsArray.append(value)
					timesTeamGiven.append(1)
				else:
					for y in teamsArray:
						if y==value:
							break
						else:
							teamsIter = teamsIter+1
					#print 'Location is %s' % teamsIter
					timesTeamGiven[teamsIter-1] = timesTeamGiven[teamsIter-1] + 1
			elif answerNum == 5:
				if value not in sportsArray:
					sportsArray.append(value)
					timesSportGiven.append(1)
				else:
					for y in sportsArray:
						if y==value:
							break
						else:
							sportsIter = sportsIter+1
					#print 'Location is %s' % sportsIter
					timesSportGiven[sportsIter-1] = timesSportGiven[sportsIter-1] + 1
			#print "%s" % value

	#print "-------------------------"

print teamsArray
print timesTeamGiven
print sportsArray
print timesSportGiven

tempTeamArray = teamsArray
tempTeamNum = timesTeamGiven
tempSportArray = sportsArray
tempSportNum = timesSportGiven

tempArray = zip(tempTeamArray, tempTeamNum)
tempArray.sort(key=lambda x:x[1])
tempArray2=zip(tempSportArray, tempSportNum)
tempArray2.sort(key=lambda x:x[1])

tempTeams = [x[0] for x in tempArray]
tempTeams.reverse()
tempSports = [x[0] for x in tempArray2]
tempSports.reverse()

print '\n\nOrdered Teams: '
print tempTeams
print 'Ordered Sports: '
print tempSports

if len(tempTeams) < 2:
	print 'Not enough teams. No game to predict.'
elif tempTeams[0]  == 'N/A' or tempTeams[1] == 'N/A':
	print 'Not enough teams. No game to predict.'
else:
	team1 = tempTeams[0]
	team2 = tempTeams[1]
	#---------------  BUILD OVERVIEW 2 -------------------
	
	overview2 = Overview()
	overview2.append_field('Title', 'How much do you know about...')
	
	#---------------  BUILD QUESTION 1 -------------------
	
	qc7 = QuestionContent()
	sport = 'NBA'
	question = '...' + sport + '?'
	qc7.append_field('Title',value=question)
	
	fta7 = SelectionAnswer(min=1, max=1,style='radiobutton',
						selections=ratings2,
						type='text',
						other=False)
	
	q7 = Question(identifier='nba',
				content=qc7,
				answer_spec=AnswerSpecification(fta7),
				is_required=True)
	
	#---------------  BUILD TWEET INFO -------------------
	#---------------  BUILD QUESTION 3 -------------------
	
	qc8 = QuestionContent()
	teams = [(str(team1),'0'), (str(team2),'1')]
	predictionTeams = team1 + ' vs ' + team2 + '\n\nWho will win?'
	qc8.append_field('Title', value= predictionTeams)
	
	fta8 = SelectionAnswer(min=1,max=1,style='radiobutton',
						selections=teams,
						type='text',
						other=False)
	
	q8 = Question(identifier='prediction',
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
			continue
		else:
			break
	
	print 'Done2'
	
	#Get data from hit2

	teamsArray2 = [team1, team2]
	teamPredicts =[0, 0]
	
	assignments2 = mtc.get_assignments(hit2_id)
	answerNum=0
	
	knowledgeValue = 0
	
	
	for assignment in assignments2:
		#print "Answers of the worker %s" % assignment.WorkerId
		for question_form_answer in assignment.answers[0]:
			for value in question_form_answer.fields:
				answerNum=answerNum+1
				#print "Answer %s:" % answerNum
				if answerNum == 1:
					knowledgeValue = int(value)
				elif answerNum == 2:
					if value == 0:
					    teamPredicts[0] = teamPredicts[0] + knowledgeValue
					else:
						teamPredicts[1] = teamPredicts[1] + knowledgeValue
				#print "%s" % value
	
		#print "-------------------------"
	
	print teamsArray2
	print teamPredicts
	
	predictionArray = zip(teamsArray2, teamPredicts)
	predictionArray.sort(key=lambda x:x[1])
	
	predictedTeams = [x[0]for x in predictionArray]
	predictedTeams.reverse()
	
	print '\n\nThe prediction of the crowd is: '
	print str(predictedTeams[0])+ ' will win!'