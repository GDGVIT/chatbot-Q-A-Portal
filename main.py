# Tornado libraries
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPServer

# other libraries
from pymongo import MongoClient
import os
import env

db = MongoClient(env.DB_Link)['chatbot-learn']
ques = db['ques']

class MainHandler(RequestHandler):
    def get(self):
        ques_count = db.ques.count()
        self.render('index.html', ques_count = ques_count)

    def post(self):
        ques = self.get_argument("ques")
        ans = self.get_argument("ans")

        if db.ques.find_one({'ques':ques}) != None :
             self.write('such a question exist')

        else :
            db.ques.update({'ques': ques},
                            {"$set": {'question':ques,
                                      'answer': ans}}, upsert=True)




settings = dict(
    db=db,
    debug=True
)

app = Application(
    handlers=[
        (r'/',MainHandler)
    ],
    template_path=os.path.join(os.path.dirname(__file__), "template"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    **settings)

if __name__=="__main__":
    server = HTTPServer(app)
    server.listen(8555)
    IOLoop.current().start()