import sys, os
#http://blog.oscarcp.com/?p=167
sys.path.insert(0, '/home/peeptree/.pythonbrew/pythons/Python-2.7.3/lib')
sys.path.insert(1,'/home/peeptree/.pythonbrew/venvs/Python-2.7.3/prod0/bin')
sys.path.insert(0,'/home/peeptree/.pythonbrew/venvs/Python-2.7.3/prod0/lib/python2.7/site-packages')
INTERP = '/home/peeptree/.pythonbrew/venvs/Python-2.7.3/prod0/bin/python'
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())
sys.path.insert(0,'/home/peeptree/svoregistry.com/svoregistry')
os.environ['DJANGO_SETTINGS_MODULE'] = 'svoregistry.settings'
import django.core.handlers.wsgi #@UnresolvedImport
application = django.core.handlers.wsgi.WSGIHandler()


#def application(environ, start_response):
#    import django
#    start_response('200 OK', [('Content-type', 'text/plain')])
#    return [str(sys.version_info) + '\n' + str(django.VERSION) + '\n' + message + '\n' + str(application)]