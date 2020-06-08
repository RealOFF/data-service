from pymongo.write_concern import WriteConcern

from pymodm import MongoModel, fields

class Message(MongoModel):
    url = fields.CharField()
    text = fields.CharField()
    date = fields.DateTimeField()
    channel = fields.CharField()
    tags = fields.ListField()
    salary = fields.DictField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'Messages'
