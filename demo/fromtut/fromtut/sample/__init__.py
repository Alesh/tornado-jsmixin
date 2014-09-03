import tornado.web

class Comment(object):
    __jsx__ = 'Comment.jsx'

class CommentList(object):
    __jsx__ = 'CommentList.jsx'
    __required__ = [Comment]

class CommentForm(object):
    __jsx__ = 'CommentForm.jsx'

class CommentBox(tornado.web.RequestHandler):
    __jsx__ = 'CommentBox.jsx'
    __required__ = [CommentList, CommentForm]

    def get(self):
        if not hasattr(self.application, 'comments'):
            self.application.comments = list()
        self.write(dict(comments=self.application.comments))

    def post(self):
        if not hasattr(self.application, 'comments'):
            self.application.comments = list()
        self.application.comments.append(dict(
            author = self.get_argument('author'), 
            text = self.get_argument('text')))
        self.write(dict(comments=self.application.comments))


    @classmethod
    def onRegister(cls, application):
        application.handlers[0][1].append(tornado.web.URLSpec('/comments.json', cls))
