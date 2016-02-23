# From http://www.obeythetestinggoat.com/how-to-log-exceptions-to-stderr-in-django.html
import logging

class ExceptionLoggingMiddleware(object):

    def process_exception(self, request, exception):
        logging.exception('Exception handling request for ' + request.path)

