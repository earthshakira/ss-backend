import falcon
import falcon_jsonify
import mongoengine as mongo
import settings

mongo.connect(host=settings.MONGO)
print(settings.MONGO)
print("Mongo Connected!")

api = falcon.API(middleware=[
    falcon_jsonify.Middleware(help_messages=settings.DEBUG),
])
