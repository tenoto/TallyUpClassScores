#!/usr/bin/env python

"""
1. 
"""

__file__    = 'tallyup.py'
__author__  = 'Teruaki Enoto'
__date__    = '2020 August 7'
__version__ = '0.01'

import os 
import argparse
import statistics
import pandas as pd 

"""
for student in student_sample:
  if len(student.scores) == 0:
    student.median_score = 0
  else:
    student.median_score = statistics.median(student.scores)
  if student.review_flag:
    student.reviewer_score = 5
  else:
    student.reviewer_score = 0
  student.total_score = student.quiz_score + student.reviewer_score + student.median_score + student.enoto_score

  if student.id == 2:
    print("%s Quiz=%d Median=%d Enoto=%d Review=%d Total=%d" % (student.name, student.quiz_score, student.median_score, student.enoto_score, student.reviewer_score, student.total_score))
"""

class Student():	
	def __init__(self,name,student_id):
		self.name = name
		self.id = student_id
		self.teacher_score = 0
		self.mutual_scores = []
		self.mutual_comments = []
		self.mutual_median_score = 0
		self.has_reviewed = False
		self.reviewed_score = 0
		self.total_score = 0

	def show(self,flag_detail=False):
		print("ID=%03d (%s): teacher=%d, median=%d, reviewed=%d, total=%d" % (self.id,self.name,
			self.teacher_score,self.mutual_median_score,self.reviewed_score,self.total_score))
		if flag_detail:
			print("ID=%03d (%s): scores=%s" % (self.id,self.name,self.mutual_scores))
			print("ID=%03d (%s): comments=%s" % (self.id,self.name,self.mutual_comments))			

	def set_mutual_median_score(self):
		if len(self.mutual_scores) == 0:
			self.mutual_median_score = 0
		else:
			self.mutual_median_score = statistics.median(self.mutual_scores)

	def sum_score(self):
		self.total_score = self.teacher_score
		self.total_score += self.mutual_median_score
		self.total_score += self.reviewed_score

def set_score(csvfile,number_of_targets=3):
	if not os.path.exists(csvfile):
		print("Error: file %s does not exits." % csvfile)
		exit()	
	df = pd.read_csv(csvfile)  
	print("csvfile: %s" % csvfile)

	# Initialization
	student_sample = []
	for index, row in df.iterrows():
		student = Student(row['Name'],row['ID'])
		student.teacher_score = row['teacher_score']
		if row["target_ID_1"] != "":
			student.has_reviewed = True
			student.reviewed_score = 5
		student_sample.append(student)

	# Put scores
	colname_target = ["target_ID_%d" % (i+1) for i in range(number_of_targets)]
	colname_score = ["target_score_%d" % (i+1) for i in range(number_of_targets)]
	colname_comment = ["target_comment_%d" % (i+1) for i in range(number_of_targets)]	

	for index, row in df.iterrows():
		print("... adding ID=%d inputs ..." % row["ID"])
		for i in range(number_of_targets):
			for student in student_sample:
				if student.id == int(row[colname_target[i]]):
					student.mutual_scores.append(row[colname_score[i]])
					student.mutual_comments.append(row[colname_comment[i]])

	# Finalization
	for student in student_sample:
		student.set_mutual_median_score()
		student.sum_score()

	for student in student_sample:
		student.show(flag_detail=True)

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

	set_score(args.csvfile)

if __name__=="__main__":
	main()