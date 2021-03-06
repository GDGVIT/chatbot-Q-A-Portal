# Tornado libraries
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPServer
from tornado.gen import coroutine, sleep

# other libraries
from motor import MotorClient
import os

db = MotorClient(os.environ['DB_Link'])['chatbot-learn']
ques = db['ques']


class IndexHandler(RequestHandler):
    def get(self):
        if self.get_cookie('user') == None:
            self.render('login.html')
        else:
            self.redirect('/node')


class LoginHandler(RequestHandler):
    @coroutine
    def post(self):
        username = self.get_argument('username')
        self.set_cookie('user', str(username))
        self.redirect('/node')


class MainHandler(RequestHandler):
    @coroutine
    def get(self):
        user = self.get_cookie('user')
        # pre_ques =yield db.ques.find().to_list(None)
        try:
            old_response = self.get_query_argument('response')
            response = "your answer was submitted successfully, try another"
        except:
            response = ''
        self.render('index.html', response=response, user=user)

    @coroutine
    def post(self):
        user = self.get_cookie('user')
        ques_type = self.get_argument('ques_type').lower()
        ques_n = "ques"
        ans_n = "ans"
        if ques_type in ['places', 'chapters', 'food']:
            ques_n = "ques1"
            ans_n = "ans1"
        ques = self.get_argument(ques_n).rstrip('?').strip().lower()
        ans = self.get_argument(ans_n).lower()
        check_inside = yield db.ques.find_one({'question': ques})
        if check_inside is not None:
            self.write('such a question exist')
        elif len(ques) < 2:
            self.write('your answer or question is too short..please try again')
        elif ques_type in ['places', 'food', 'chapters']:
            rating = self.get_argument('rating')
            yield db.ques.update({'question': ques},
                                 {"$set": {'question': ques, 'answer': ans,
                                           'rating': rating,
                                           'type': ques_type, 'submitted by': user}}, upsert=True)

            self.redirect('/node?response=True')
        else:
            yield db.ques.update({'question': ques},
                                 {"$set": {'question': ques, 'answer': ans,
                                           'type': ques_type, 'submitted by': user}}, upsert=True)

            self.redirect('/node?response=True')


class LogoutHandler(RequestHandler):
    @coroutine
    def get(self):
        if bool(self.get_cookie('user')):
            self.clear_cookie('user')
            self.redirect('/')

class ContributorHandling(RequestHandler):
    def get(self):
        import json
        from contribute import contribute
        contributors_list = contribute()
        self.render("contributors.html",contributors_list=contributors_list)


settings = dict(
    db=db,
    debug=True
)

app = Application(
    handlers=[
        (r'/', IndexHandler),
        (r'/node', MainHandler),
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler),
        (r'/contributor', ContributorHandling)
    ],
    template_path=os.path.join(os.path.dirname(__file__), "template"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    **settings)

if __name__ == "__main__":
    server = HTTPServer(app)
    server.listen(os.environ.get("PORT", 5000))
    IOLoop.current().start()
