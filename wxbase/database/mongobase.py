from pymongo import MongoClient
from flask import logging
from datetime import datetime


class MongoBase(object):

    def __init__(self, config):
        self.db = self.init_db(config)
        self.logger = logging.getLogger(__name__)

    def init_db(self, config):
        client = MongoClient(
            'mongodb://{0}:{1}@{2}:{3}'.format(config['db']['user'],
                                               config['db']['password'],
                                               config['db']['host'],
                                               config['db']['port']))
        self._db = client[config['db']['database']]
        return self._db

    def find_by_condition(self, collection, condition):
        try:
            cursor = self.db[collection].find(condition)
        except Exception as ex:
            self.logger.error(ex)
            return False, None
        else:
            result = list(cursor)
            for i in result:
                i['id'] = str(i.pop('_id'))

            return True, result

    def create(self, collection, data):
        data['createdDate'] = datetime.utcnow()
        data['lastModifiedDate'] = datetime.utcnow()
        try:
            result = self.db[collection].insert_one(data)
        except Exception as ex:
            self.logger.error(ex)
            return False
        else:
            return {'id': str(result.inserted_id)}

    def update(self, collection, filter, data, upsert=False):
        if filter.get('id'):
            from bson import ObjectId
            filter['_id'] = ObjectId(filter.pop('id'))

        if data.get('$set'):
            data['$set'].update({'lastModifiedDate': datetime.utcnow()})
        else:
            data.update({'$set': {'lastModifiedDate': datetime.utcnow()}})

        try:
            result = self.db[collection].update_one(filter, data, upsert)
        except Exception as ex:
            self.logger.error(ex)
            return False, None
        else:
            return (True,
                    result.modified_count if result.modified_count else None)

