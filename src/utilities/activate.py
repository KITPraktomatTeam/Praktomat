from accounts.models import User
from django.core.exceptions import ObjectDoesNotExist

def activate(matfilename):
	f=open(matfilename,'r')
	matnummers=f.readlines()
	for matnummer in [int(nr) for nr in matnummers]:
		#print "ImportingMatnummer: %d\t" % matnummer
		try:
			user = User.objects.get(mat_number=matnummer)
			user.is_active = True
			user.save()
		except ObjectDoesNotExist:
			print "not found: %d" % matnummer
			
#		print user.username
	f.close()

