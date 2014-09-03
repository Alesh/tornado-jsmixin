import os.path
import jsmixin
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    """ Main page handler """
    def get(self):
        self.render("index.html")


class Application(tornado.web.Application, jsmixin.ReactMixin):
    """ Application class """
    def __init__(self, **settings):
        root_path = os.path.dirname(__file__)
        settings.setdefault('template_path', os.path.join(root_path, 'templates'))
        settings.setdefault('static_path', os.path.join(root_path, 'statics'))
        tornado.web.Application.__init__(self, [
            (r"/index.html", MainHandler), (r"/", MainHandler)
        ], **settings)
        jsmixin.ReactMixin.__init__(self)
        self.registerFile(os.path.join(self.settings['static_path'], 'jquery.js'), 'jquery')
        self.buildBundle()
