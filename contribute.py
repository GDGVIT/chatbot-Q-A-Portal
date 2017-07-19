def contribute():
    import pymongo
    import os
    db = pymongo.MongoClient(os.environ['DB_Link'])['chatbot-learn']
    ques = db['ques']
    contr = []
    for i in db.ques.aggregate([{'$group': {'_id': '$submitted by', 'count': {'$sum': 1}}}]):
        contr.append(i)

    return sorted(contr,key= lambda p:p['count'],reverse=True)
