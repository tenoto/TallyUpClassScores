#!/usr/bin/env python

__file__    = 'tallyup.py'
__author__  = 'Teruaki Enoto'
__date__    = '2020 December 7'
__version__ = '0.02'

import os 
import math
import argparse
import statistics
import pandas as pd 

MAXIMUM_NUMBER_OF_STUDENT_ID = 224
NUMBER_OF_REVIEW_TARGETS = 6
REVIEW_POINT = 5 

class Student():	
	def __init__(self,student_id):
		self.id = student_id	
		self.name = 'N/A'
		self.received_review_scores = []
		self.received_review_comments = []
		self.received_median_score = 0
		self.reviewer_ids = []
		self.has_review = False
		self.review_participate_socre = 0

	def print(self,flag_detail=True):
		message  = "ID=%d (%s): " % (self.id,self.name)
		message += "mean=%d " % self.received_median_score
		message += "review=%d " % self.review_participate_socre		
		message += "scores=%s " % self.received_review_scores
		message += "reviewer=%s " % self.reviewer_ids 
		message += "comments=%s " % self.received_review_comments
		print(message)

	def dump(self):
		dump  = '%d;' % self.id
		dump += '%d;' % self.received_median_score
		dump += '%d;' % self.review_participate_socre
		for i in range(len(self.received_review_comments)):
			dump += '%s;' % self.received_review_comments[i]
		dump += '\n'
		return dump

def generate_score_file(csvfile,number_of_targets=NUMBER_OF_REVIEW_TARGETS):
	if not os.path.exists(csvfile):
		print("Error: file %s does not exits." % csvfile)
		exit()	
	df = pd.read_csv(csvfile)  
	print("csvfile: %s" % csvfile)

	# Initialization
	student_sample = [Student(i) for i in range(1,MAXIMUM_NUMBER_OF_STUDENT_ID+1)]

	# main body
	for index, row in df.iterrows():
		for student in student_sample:
			if student.id == int(row['ID']):
				student.name = row['Name']
				student.has_review = True
				for i in range(1,NUMBER_OF_REVIEW_TARGETS+1):
					target_id = int(row["target_ID_%d" % i])
					target_score = row["target_score_%d" % i]
					target_comment = row["target_comment_%d" % i]

					if target_id == 0:
						break 

					for target_student in student_sample:
						if target_student.id == target_id:
							target_student.reviewer_ids.append(student.id)							
							target_student.received_review_comments.append(target_comment)
							try:
								target_student.received_review_scores.append(int(target_score))
							except:
								pass

	# calculate median 						
	for student in student_sample:
		if len(student.received_review_scores) == 0:
			student.received_median_score = 0
		else:
			student.received_median_score = int(math.ceil(statistics.median(student.received_review_scores)))

	# review 
	for student in student_sample:
		if student.has_review:
			student.review_participate_socre = REVIEW_POINT 	

	# modify comments
	for student in student_sample:
		for i in range(len(student.received_review_comments)):
			comment = str(student.received_review_comments[i])
			comment = comment.replace('\n','')
			comment = comment.replace('\r','')
			comment = comment.replace(',','、')			
			comment = comment.replace('"','~')						
			student.received_review_comments[i] = comment

	# print
	for student in student_sample:
		student.print()

	# dump
	f = open('2020A_midterm_evaluation_summary_public.csv','w')
	for student in student_sample:
		f.write(student.dump())
	f.close()


def get_parser():
	"""
	Creates a new argument parser.
	"""
	parser = argparse.ArgumentParser('tallyup.py',
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="""
Tally up a student score file.
		"""
		)
	version = '%(prog)s ' + __version__
	parser.add_argument('--version', '-v', action='version', version=version,
		help='show version of this command.')
	parser.add_argument('--csvfile', '-i', type=str, required=True, 
		help='input csv file.')
	return parser

def main(args=None):
	parser = get_parser()
	args = parser.parse_args(args)
	generate_score_file(args.csvfile)

if __name__=="__main__":
	main()