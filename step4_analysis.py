"""
Task:
1. to mongo db
2. quary and anayts
"""

from pymongo import MongoClient
import os
import pprint
import json

client = MongoClient("mongodb://localhost:27017")
db = client.taipei
collection = db.city

def mongo_insert():
	'''啟動mongo, 並且創建collection，以及輸入檔案'''
	client = MongoClient("mongodb://localhost:27017")
	db = client.taipei
	collection = db.city
	os.system('mongoimport --db taipei --collection city --drop --file taipei_taiwan.osm.json')

def print_result(cursor):
    for document in cursor:
        pprint.pprint(document)


if __name__ == "__main__":

	 mongo_insert()

    # 第一名貢獻者
    pipeline = [ { "$group" : { "_id" : "$Created.user",
                            "count" : { "$sum" : 1 } } },
             { "$sort" : { "count" : -1 } },
             { "$limit" : 5 } ]

	cursor = collection.aggregate(pipeline)
	print_result(cursor)

	# Node Way 數量
	pipeline = [{ "$group":{ "_id": "$type",
                         "count": { "$sum" : 1 }  } }]
	cursor = collection.aggregate(pipeline)
	print_result(cursor)

	# 多少個文檔
	print(collection.find().count())

	# 台北有幾家7-Eleven
	pipeline = [ { "$match" : { "Daily.operator" : "7-Eleven" } },
            { "$group" : { "_id" : "7-Eleven",
                            "count" : { "$sum" : 1 } } } ] 
	cursor = collection.aggregate(pipeline)
	print_result(cursor)


	# 台北前十大的店舖
	pipeline = [ { "$match" : { "Tour.shop" : { "$exists" : 1 }, 'Tour.shop':{'$ne':None}} },
                            { "$group" : { "_id" : "$Tour.shop",
                                           "count" : { "$sum" : 1 } } },
                            { "$sort" : { "count" : -1} },
                            { "$limit" : 10 } ]
	cursor = collection.aggregate(pipeline)
	print_result(cursor)

	# 台北前10大餐廳
	pipeline = [ { "$match" : { "Tour.cuisine":{'$ne':None}}},
                { "$group" : { "_id" : "$Tour.cuisine",
                            "count" : { "$sum" : 1 } } },
                { "$sort" : { "count" : -1 } },
                { "$limit" : 10 } ]
	cursor = collection.aggregate(pipeline)
	print_result(cursor)

	# 台北最常見的營業時間
	pipeline = [ {'$match':{'Tour.opening_hours':{'$ne':None}}},
             { "$group" : { "_id" : "$Tour.opening_hours",
                           "count": {"$sum": 1 }}},
             { "$sort" : { "count" : -1 }},
             { "$limit" : 5 }] 
	cursor = collection.aggregate(pipeline)
	print_result(cursor)

	# 書店常見營業時間
	pipeline = [ {'$match':{'Tour.shop':'books'}},
             { "$group" : { "_id" : "$Tour.opening_hours",
                            "count" : { "$sum" : 1 } } },
                { "$sort" : { "count" : -1 } },
                { "$skip" : 1 },
                { "$limit" : 1 } ] 
	cursor = collection.aggregate(pipeline)
	print_result(cursor)

	# 台北前十大自然景物
	pipeline = [ { "$group" : { "_id" : "$Tour.natural",
                           "count": {"$sum": 1 }}},
             { "$sort" : { "count" : -1 }},
             { "$skip" : 1 },
             { "$limit" : 10 }] 
	cursor = collection.aggregate(pipeline)
	print_result(cursor)

	# 台北前十大宗教
	pipeline = [{"$match":{"Daily.religion":{"$exists":1}}},
            {"$group":{"_id":"$Daily.religion", 
                       "count":{"$sum":1}}}, 
            {"$sort":{"count": -1}}, 
            {"$limit":5}]
	cursor = collection.aggregate(pipeline)
	print_result(cursor)

	# 最多宗教的路
	pipeline = [{"$match":{"Daily.religion":{"$exists":1},
                       "Address.street":{"$ne":None}}},
            {"$group":{"_id":"$Address.street",
                      'count':{"$sum":1}}},
            {"$sort":{"count": -1}}, 
            {"$limit":10}]
	cursor = collection.aggregate(pipeline)
	print_result(cursor)

	# 猜想最多的便利超商，會跟學校有很大關係
	pipeline = [{"$match":{ "Tour.shop" : { "$exists" : 1 }, 'Address.street':{'$ne':None}}},
            {"$group":{"_id":"$Address.street",
                      'count':{"$sum":1}}},
            {"$sort":{"count": -1}}, 
            {"$limit":10}]
	cursor = collection.aggregate(pipeline)
	print_result(cursor)