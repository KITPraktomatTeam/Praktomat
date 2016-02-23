#!/usr/bin/python
# Checks whether we're running in daemon-mode
def application(environ, start_response):
    status = '200 OK'

    if not environ['mod_wsgi.process_group']:
      output = 'EMBEDDED MODE'
    else:
      output = 'DAEMON MODE'

    response_headers = [('Content-Type', 'text/plain'),
                        ('Content-Length', str(len(output)))]

    start_response(status, response_headers)

    return [output]
