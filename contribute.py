def contribute():
    import pymongo
    db = pymongo.MongoClient('mongodb://chatbot-learn:qwerty1234@ds135592.mlab.com:35592/chatbot-learn')['chatbot-learn']
    ques = db['ques']
    contr = []
    for i in db.ques.aggregate([{'$group': {'_id': '$submitted by', 'count': {'$sum': 1}}}]):
        contr.append(i)

    return sorted(contr,key= lambda p:p['count'],reverse=True)
