from django.db import models
from datetime import datetime,time,timedelta
#from praktomat.checker.tests import AnonymityChecker, LineCounter
    
class Task(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	publication_date = models.DateTimeField()
	submission_date = models.DateTimeField()
	
	def __unicode__(self):
		return self.title
		
	def solutions(self,user):
		"""get solutions of the specified user"""
		return self.solution_set.filter(author=user)
		
	def checker(self):
		return self.AnonymityChecker_set.all() + self.LineCounter_set.all()
		
	def expiered(self):
		"""docstring for expiered"""
		return submission_date + datetime.timedelta(hour=1) > datetime.now()
   
class MediaFile(models.Model):
    task = models.ForeignKey(Task)
    media_file = models.FileField(upload_to='upload/admin/')    

    def __unicode__(self):
	    return self.media_file.name