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
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    
class Permalink(Handler):
    def get(self, blog_id):
        s = Blog.get_by_id(int(blog_id))
        self.render("front.html", blogs=[s])
    
class NewPost(Handler):
    def render_newpost(self, subject="", content="", error=""):
        self.render("newpost.html", subject=subject, content=content, error=error)
    def get(self):
        self.render_newpost()
        
    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        
        if subject and content:
            b = Blog(subject=subject, content=content)
            b_key = b.put() # Key('Blog', id)      
            self.redirect("/blog/%d" % b_key.id())
        else:
            error = "we need both a title and some content!"
            self.render_newpost(subject=subject, content=content, error=error)

class BlogFront(Handler):
    def render_front(self):
        blogs = db.GqlQuery("select * from Blog ORDER BY created desc limit 10")
        self.render("front.html", blogs=blogs)
        
    def get(self):
        self.render_front()
        
class MainPage(Handler):
  def get(self):
      self.write('Main Page')

app = webapp2.WSGIApplication([ ('/', MainPage),
                                ('/blog', BlogFront),
                                ('/blog/newpost', NewPost),
                                ('/blog/(\d+)', Permalink)], 
                                debug=True)