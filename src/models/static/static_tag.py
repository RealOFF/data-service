from pymongo.write_concern import WriteConcern

from pymodm import MongoModel, fields

class StaticTag(MongoModel):
    name = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'StaticTags'