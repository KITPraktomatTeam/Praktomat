from accounts.models import User
from django.core.exceptions import ObjectDoesNotExist

def activate(matfilename):
    with open(matfilename, 'r') as f:
        matnummers=f.readlines()
        for matnummer in [int(nr) for nr in matnummers]:
            #print "ImportingMatnummer: %d\t" % matnummer
            try:
                user = User.objects.get(mat_number=matnummer)
                user.is_active = True
                user.save()
            except ObjectDoesNotExist:
                print("not found: %d" % matnummer)
