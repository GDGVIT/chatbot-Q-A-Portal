# Tornado libraries
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPServer
from tornado.gen import coroutine, sleep

# other libraries
from motor import MotorClient
import os
import env

db = MotorClient(env.DB_Link)['chatbot-learn']
ques = db['ques']


class MainHandler(RequestHandler):
    @coroutine
    def get(self):
        ques_count = db.ques.count()
        try:
            old_response = self.get_query_argument('response')
            response = "your answer was submitted successfully, try another"
        except:
            response = ''
        self.render('index.html', ques_count=ques_count, response=response)

    @coroutine
    def post(self):
        ques_type = self.get_argument('ques_type').lower()
        ques = self.get_argument("ques").rstrip('?').strip()
        ans = self.get_argument("ans")

        check_inside = yield db.ques.find_one({'ques': ques})
        if check_inside is not None:
            self.write('such a question exist')
        elif len(ques) < 10 or len(ans) < 10:
            self.write('your answer or question is too short..please try again')
        else:
            yield db.ques.update({'question': ques},
                                 {"$set": {'question': ques, 'answer': ans,
                                  'type': ques_type}}, upsert=True)
            self.redirect('/?response=True')


settings = dict(
    db=db,
    debug=True
)

app = Application(
    handlers=[
        (r'/', MainHandler)
    ],
    template_path=os.path.join(os.path.dirname(__file__), "template"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    **settings)

if __name__ == "__main__":
    server = HTTPServer(app)
    server.listen(os.environ.get("PORT", 5000))
    IOLoop.current().start()
