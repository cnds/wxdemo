from pymongo import MongoClient
from flask import logging
from datetime import datetime
from bson import ObjectId


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

    def find_by_condition(self, collection, condition, skip=0, limit=0):
        try:
            cursor = self.db[collection].find(condition,
                                              skip=skip, limit=limit)
        except Exception as ex:
            self.logger.error(ex)
            return False, None
        else:
            result = list()
            for i in cursor:
                i['id'] = str(i.pop('_id'))
                result.append(i)

            return True, result

    def find_by_id(self, collection, entity_id, skip=0, limit=0):
        try:
            entity_id = ObjectId(entity_id)
        except Exception as ex:
            self.logger.error(ex)
            return False, None

        try:
            cursor = self.db[collection].find_one({'_id': entity_id},
                                                  skip=skip, limit=limit)
        except Exception as ex:
            self.logger.error(ex)
            return False, None
        else:
            if cursor is None:
                return True, None

        result = dict(cursor)
        result['id'] = str(result.pop('_id'))
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

    def update(self, collection, filter_query, data, upsert=False):
        if filter_query.get('id'):
            from bson import ObjectId
            filter_query['_id'] = ObjectId(filter_query.pop('id'))

        if data.get('$set'):
            data['$set'].update({'lastModifiedDate': datetime.utcnow()})
        else:
            data.update({'$set': {'lastModifiedDate': datetime.utcnow()}})

        try:
            result = self.db[collection].update_one(filter_query, data, upsert)
        except Exception as ex:
            self.logger.error(ex)
            return False, None
        else:
            return (True,
                    result.modified_count if result.modified_count else None)

