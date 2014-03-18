import os
import webapp2
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        
class Blog(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    permalink = obj.key().id()
    
class Permalink(MainPage):
        def get(self, blog_id):
            s = Blog.get_by_id(int(blog_id))
            self.render("front.html", blogs=[s])
    
class Newpost(Handler):
    if subject and content:
            b = Blog(subject=subject, content=content)
            b_key = b.put() # Key('Blog', id)      
            self.redirect("/blog/%d" % b_key.id())

class MainPage(Handler):
    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
        self.render("front.html", title=title, art=art, error = error)
        
    def get(self):
        self.render_front()
        
    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")
        if title and art:
            a = Art(title = title, art = art)
            a.put()
            self.redirect("/")
        else:
            error = "we need both a title and some artwork!"
            self.render_front(title, art, error)

app = webapp2.WSGIApplication([ ('/blog', MainPage),
                                ('/blog/newpost', NewPost),
                                ('/blog/(\d+)', Permalink)], 
                                debug=True)