import numpy as np
"""

This script uses recursion to calculate the longest path lengths of prerequisite courses in my biophysics program
based on the courses I have already taken and the ones I am yet to take. It is basically a linked list with extra steps.

"""

my_courses = [{'name':'PHY 473',
				'hours':3,
				'prereqs':['PHY 371','PHY 472'],
				'taken': False},
				{'name':'PHY 472',
				'hours':3,
				'prereqs':['CHM 341'],
				'taken':False},
				{'name':'PHY 371',
				'hours':3,
				'prereqs':['CHM 341'],
				'taken':False},
				{'name':'PHY 312',
				'hours':3,
				'prereqs':['PHY 201','PHY 202','PHY 241'],
				'taken':False},
				{'name':'CHM 341',
				'hours': 3,
				'prereqs':['CHM 116','CHM 233','MAT 265','PHY 112'],
				'taken':False},
				{'name':'PHY 314',
				'hours':3,
				'prereqs':['PHY 201','PHY 202','PHY 241'],
				'taken':False},
				{'name':'BIO 312',
				'hours':3,
				'prereqs':[],
				'taken':False},
				{'name':'BIO 353',
				'hours':3,
				'prereqs':['BIO 181','BIO 182','CHM 116','BIO 282'],
				'taken':False},
				{'name':'PHY 201',
				'hours':3,
				'prereqs':['MAT 267','PHY 131','PHY 132'],
				'taken': False},
				{'name':'CHM 233',
				'hours':3,
				'prereqs':['CHM 116'],
				'taken':False},
				{'name':'PHY 241',
				'hours':3,
				'prereqs':['PHY 131'],
				'taken':False},
				{'name':'PHY 202',
				'hours':1,
				'prereqs':['MAT 267','PHY 131','PHY 132'],
				'taken':False},
				{'name':'CHM 116',
				'hours':4,
				'prereqs':['CHM 114'],
				'taken':False},
				{'name':'PHY 131',
				'hours':3,
				'prereqs':['MAT 266','PHY 121','MAT 267'],
				'taken':True},
				{'name':'PHY 132',
				'hours':1,
				'prereqs':[],
				'taken':True},
				{'name':'MAT 267',
				'hours':3,
				'prereqs':['MAT 266'],
				'taken':True},
				{'name':'CHM 114',
				'hours':4,
				'prereqs':[],
				'taken':True},
				{'name':'BIO 182',
				'hours':4,
				'prereqs':['BIO 181'],
				'taken':False},
				{'name':'PHY 122',
				'hours':1,
				'prereqs':[],
				'taken':True},
				{'name':'PHY 121',
				'hours':3,
				'prereqs':['MAT 265','MAT 266'],
				'taken':True},
				{'name':'BIO 181',
				'hours':4,
				'prereqs':[],
				'taken':True},
				{'name':'MAT 266',
				'hours':3,
				'prereqs':['MAT 265'],
				'taken':True},
				{'name':'MAT 265',
				'hours':3,
				'prereqs':[],
				'taken':True}]

class course:
	def __init__(self,name,hours,prereqs,taken):
		self.name = name
		self.dept,self.number = name.split()
		self.hours = hours
		self.prereqs = prereqs
		self.taken = taken
	def __str__(self):
		return f'--- {self.name} ---\nHours: {self.hours}\nPrerequisites: {", ".join([prereq.name for prereq in self.prereqs])}\nTaken: {self.taken}'

	def convert_prereqs_to_references(self):
		ref_list = []
		for course_name in self.prereqs:
			for my_course in my_courses:
				if my_course.name == course_name:
					ref_list.append(my_course)
		self.prereqs = ref_list
	def find_paths(self,_course):
		paths = []
		for prereq in _course.prereqs:
			if not prereq.taken: 
				for sub_path in self.find_paths(prereq):
					paths.append([_course.name]+ sub_path)
			else: paths.append([_course.name])
		return paths
	def find_longest_path(self):
		temp_paths = self.find_paths(self) if not self.taken else []
		self.paths = reduce_paths(temp_paths)
		self.longest_path = max([len(path) for path in self.paths]) if len(self.paths) else 0

#sort paths by length and eliminate any paths that are entirely contained in a longer path
def reduce_paths(temp_paths):
	reduced_paths = []
	temp_paths.sort(key=len,reverse=True)
	for i in range(len(temp_paths)):
		temp_path = temp_paths.pop()
		if not np.any([np.all([(_course in other_path) for _course in temp_path]) for other_path in temp_paths]):
			reduced_paths.append(temp_path)
	return reduced_paths

my_courses = [course(*course_params.values()) for course_params in my_courses]
[my_course.convert_prereqs_to_references() for my_course in my_courses]
[my_course.find_longest_path() for my_course in my_courses]

print_courses = lambda my_courses: [print(my_course) for my_course in my_courses]

all_paths = []
for my_course in my_courses:
	for course_path in my_course.paths:
		all_paths.append(course_path)
all_paths = reduce_paths(all_paths)


#print paths
print('PREREQUISITE PATHS\n')
for path in all_paths:
	print('----------------------------')
	print(f'Path length: {len(path)}: {" --> ".join(path[::-1])}')


#print totals
print('\n### TOTAL ###')
print(f'Courses: {len(my_courses)}')
print(f'Hours: {sum([my_course.hours for my_course in my_courses])}\n\n\n')


