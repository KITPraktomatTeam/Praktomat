# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test import RequestFactory
#from django.urls import Resolver404

from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler

#from myapp.wsgi import my_wsgi_app
# since praktomat.wsgi is not a module, we simulate that it is a module.

def my_wsgi_loader():
    import sys
    import os
    from os.path import join, dirname
    MODULE_NAME = "praktomat"
    MODULE_PATH = join(settings.PRAKTOMAT_PATH,"wsgi","praktomat.wsgi")
    #print ("DEBUG: MODULE_PATH=",MODULE_PATH)
    PY2 = sys.version_info[0] == 2
    PY3 = sys.version_info[0] == 3
    if PY2 :
       import imp
       mymodule = imp.load_source(MODULE_NAME, MODULE_PATH)
       return mymodule.application
    if PY3 :
       import importlib.machinery
       import importlib.util
       loader = importlib.machinery.SourceFileLoader(MODULE_NAME, MODULE_PATH)
       spec = importlib.util.spec_from_loader(MODULE_NAME, loader)
       mymodule = importlib.util.module_from_spec(spec)
       loader.exec_module(mymodule)
       return mymodule.application


class PraktomatMyWsgiTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_praktomat_WSGIHandler_createable(self):
        application=my_wsgi_loader()  # returns a WSGIHandler
        self.assertTrue( isinstance(application, WSGIHandler) , msg="%s : not a WSGIHandler created"%(str(self)) )
        response=application.get_response(RequestFactory().get('/'))
        self.assertEqual(response.status_code , 301 , msg="%s : WSGIHandler : Status was %s != 301 \n %s" %(str(self),response.status_code,str(response)) )
        self.assertIn("tasks", response.get('Location') , msg="%s : WSGIHandler response : Forward was wrong \n %s" %(str(self),str(response)) )

    def test_praktomat_favicon_from_root(self):
        application=my_wsgi_loader()  # returns a WSGIHandler
        self.assertTrue( isinstance(application, WSGIHandler) , msg="%s : not a WSGIHandler created"%(str(self)) )
        response=application.get_response(RequestFactory().get('/favicon.ico'))
        self.assertEqual(response.status_code , 301 , msg="%s : WSGIHandler : Status was %s != 301 \n %s" %(str(self),response.status_code,str(response)) )
        self.assertIn("/static/favicon.ico", response.get('Location') , msg="%s : WSGIHandler response : Forward was wrong \n %s" %(str(self),str(response)) )

    def test_praktomat_favicon_from_app(self):
        application=my_wsgi_loader()  # returns a WSGIHandler
        self.assertTrue( isinstance(application, WSGIHandler) , msg="%s : not a WSGIHandler created"%(str(self)) )
        response=application.get_response(RequestFactory().get('/tasks/favicon.ico'))
        self.assertEqual(response.status_code , 301 , msg="%s : WSGIHandler : Status was %s != 301 \n %s" %(str(self),response.status_code,str(response)) )
        self.assertIn("/static/favicon.ico", response.get('Location') , msg="%s : WSGIHandler response : Forward was wrong \n %s" %(str(self),str(response)) )

## If you want to use the following test case, than you have to install django_webtest and webtest.
#from webtest import TestApp
#from django_webtest import WebTest
#class PraktomatWsgiTest(WebTest):
    #def setUp(self):
        #pass

    #def tearDown(self):
        #pass

    #def test_wsgi_root(self):
        #res = self.app.get('/')
        #self.assertEqual(res.status_int , 301 , msg="%s : Running WSGI : Status was %s != 301 \n %s" %(str(self),res.status_int,str(res)) )
        #self.assertIn("tasks", res.headers['Location'] , msg="%s : WSGI response : Forward was wrong \n %s" %(str(self),str(res)) )
        #self.assertTrue(True)
