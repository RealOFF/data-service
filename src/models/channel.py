from pymongo.write_concern import WriteConcern

from pymodm import MongoModel, fields

class Channel(MongoModel):
    name = fields.CharField()
    last_date = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'Channels'
