from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from flask import logging
from datetime import datetime
from bson import ObjectId


class MongoBase(object):

    def __init__(self, config):
        self.mongo = self.init_db(config)
        self.logger = logging.getLogger(__name__)

    def init_db(self, config):
        client = MongoClient(
            'mongodb://{0}:{1}@{2}:{3}'.format(config['db']['user'],
                                               config['db']['password'],
                                               config['db']['host'],
                                               config['db']['port']))
        self._db = client[config['db']['database']]
        return self._db

    def find_by_condition(self, collection, condition, page=1, limit=0):
        skip = (page - 1) * limit
        try:
            cursor = self.mongo[collection].find(condition,
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

    def find_by_id(self, collection, entity_id, page=1, limit=0):
        skip = (page - 1) * limit
        try:
            entity_id = ObjectId(entity_id)
        except Exception as ex:
            self.logger.error(ex)
            return False, None

        try:
            cursor = self.mongo[collection].find_one({'_id': entity_id},
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
            result = self.mongo[collection].insert_one(data)
        except Exception as ex:
            self.logger.error(ex)
            return False
        else:
            return {'id': str(result.inserted_id)}

    def update(self, collection, filter_query, data, upsert=False):
        if filter_query.get('id'):
            filter_query['_id'] = ObjectId(filter_query.pop('id'))

        if data.get('$set'):
            data['$set'].update({'lastModifiedDate': datetime.utcnow()})
        else:
            data.update({'$set': {'lastModifiedDate': datetime.utcnow()}})

        try:
            result = self.mongo[collection].update_one(filter_query, data,
                                                       upsert=upsert)
        except Exception as ex:
            self.logger.error(ex)
            return False, None
        else:
            modified_count = result.modified_count
            upserted_id = result.upserted_id
            if modified_count:
                if modified_count == 1:
                    return True, {'id': modified_count}
                else:
                    return True, None

            if upserted_id:
                return True, {'id': str(upserted_id)}

    def remove(self, collection, entity_id):
        try:
            entity_id = ObjectId(entity_id)
        except Exception as ex:
            self.logger.error(ex)
            return False, None

        try:
            result = self.mongo[collection].delete_one({'_id': entity_id})
        except Exception as ex:
            self.logger.error(ex)
            return False, None
        else:
            if result.deleted_count == 1:
                return True, {'id': str(entity_id)}
            else:
                return True, None

    def bulk_update(self, collection, data):
        try:
            result = self.mongo[collection].bulk_write(data)
        except BulkWriteError as bwe:
            self.logger.error(bwe.details)
            return True, None
        except Exception as ex:
            self.logger.error(ex)
            return False, None
        else:
            upserted = result.bulk_api_result.get('upserted')
            if upserted:
                for i in upserted:
                    i['_id'] = str(i['_id'])

            return True, result.bulk_api_result


