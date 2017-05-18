import cherrypy
from jinja2 import Environment, FileSystemLoader
import urllib.request as urllib2,json
import redis
import threading,time
import ast,os

env = Environment(loader=FileSystemLoader('templates'))
conn = redis.Redis('localhost',charset="utf-8", decode_responses=True)
url = "https://www.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json"    
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib2.Request(url,headers=headers)
PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')

print (PATH)
print (PATH)

def thread():
	with urllib2.urlopen(req) as url:
		data = json.loads(url.read().decode())
	conn.hmset("nifty", data)
	threading.Timer(300, thread).start()

class Root:
	@cherrypy.expose
	def index(self):
		tmpl = env.get_template('index.html')
		data = conn.hgetall("nifty")
		data = ast.literal_eval(data['data'])
		return tmpl.render(data=data)

config = {
    '/static':{
    'tools.staticdir.on': True,
    'tools.staticdir.dir': PATH
    }
}

cherrypy.tree.mount(Root(), '/', config = config)
cherrypy.engine.start()
thread()



