import unittest
import sys
sys.path.insert(0, 'esgetfamily')
import main


class Test01Requirements(unittest.TestCase):

    def test01(self):
        from elasticsearch import Elasticsearch
        es_db = Elasticsearch()
        self.assertTrue(es_db.ping(), msg="Elasticsearch Connection made.")


class Test02ParentChild(unittest.TestCase):

    def setUp(self):
        from elasticsearch import Elasticsearch

        self.es_db = Elasticsearch()

        self.parent_index = "parents"
        self.parent_type = "pars"
        self.child_type = "childs"

        # Creating mapping
        mapping = {
            "mappings": {
                self.parent_type: {
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "text"},
                        "age": {"type": "integer"}
                    }
                },
                self.child_type: {
                    "_parent": {
                        "type": self.parent_type
                    },
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "text"}
                    }
                }
            }
        }

        self.es_db.indices.create(index=self.parent_index, ignore=400,
                                  body=mapping)

        # Indexing Parents
        self.es_db.index(index=self.parent_index, doc_type=self.parent_type,
                         body={u"id": 1, u"name": 'Example1', u"age": 1}, id=1)

        self.es_db.index(index=self.parent_index, doc_type=self.parent_type,
                         body={u"id": 2, u"name": 'Example2', u"age": 1}, id=2)

        # Indexing Children
        self.es_db.index(index=self.parent_index, doc_type=self.child_type,
                         body={u"id": 1, u"name": 'Child1'}, id=1, parent=1)

        self.es_db.index(index=self.parent_index, doc_type=self.child_type,
                         body={u"id": 2, u"name": 'Child2'}, id=2, parent=1)

        self.es_db.index(index=self.parent_index, doc_type=self.child_type,
                         body={u"id": 1, u"name": 'Child1'}, id=1, parent=2)

        self.es_db.index(index=self.parent_index, doc_type=self.child_type,
                         body={u"id": 2, u"name": 'Child2'}, id=2, parent=2)

        self.singleparents = self.es_db.get(index=self.parent_index,
                                            doc_type=self.parent_type, id=1)
        self.singleresult = main.parent_child(self.es_db, self.singleparents,
                                              self.child_type)

        self.multipleparents = [self.es_db.get(index=self.parent_index,
                                               doc_type=self.parent_type,
                                               id=1), self.es_db.get(
            index=self.parent_index, doc_type=self.parent_type, id=2)]

        self.multipleresult = main.parent_child(self.es_db,
                                                self.multipleparents,
                                                self.child_type)

    def test01_singlekeys(self):
        for r in self.singleresult:
            success = (self.singleresult[r]['child'] and self.singleresult[r][
                'parent'])

        self.assertTrue(success, msg="Test Passed")

    def test02_multiplekeys(self):
        for r in self.multipleresult:
            success = (self.multipleresult[r]['child'] and
                       self.multipleresult[r]['parent'])

        self.assertTrue(success, msg="Test Passed")

    def test03_singleparent(self):

        for r in self.singleresult:
            number_of_children = len(self.singleresult[r]['child'])

        self.assertEqual(number_of_children, 2, msg="Test Passed for Single "
                                                    "Parent")

    def test04_singleparentquery(self):
        query = {
            "match": {
                "id": 1
            }
        }
        result = main.parent_child(self.es_db, self.singleparents,
                                   self.child_type, query)
        for r in self.singleresult:
            number_of_children = len(result[r]['child'])

        self.assertEqual(number_of_children, 1, msg="Test Passed for Single "
                                                    "Parent with query")

    def test05_multipleparents(self):
        number_of_children = 0
        for r in self.multipleresult:
            number_of_children += len(self.multipleresult[r]['child'])

        self.assertEqual(number_of_children, 4, msg="Test Passed for "
                                                    "multiple parents")

    def test06_multipleparentquery(self):
        number_of_children = 0
        query = {
            "match": {
                "id": 1
            }
        }
        result = main.parent_child(self.es_db, self.multipleparents,
                                   self.child_type, query)
        for r in self.multipleresult:
            number_of_children += len(result[r]['child'])

        self.assertEqual(number_of_children, 2, msg="Test Passed for "
                                                    "multiple parents with "
                                                    "query")

    def tearDown(self):
        self.es_db.delete(index=self.parent_index,
                          doc_type=self.parent_type, id=1)
        self.es_db.delete(index=self.parent_index,
                          doc_type=self.parent_type, id=2)

        self.es_db.delete(index=self.parent_index,
                          doc_type=self.child_type, id=1, parent=1)
        self.es_db.delete(index=self.parent_index,
                          doc_type=self.child_type, id=2, parent=1)

        self.es_db.delete(index=self.parent_index,
                          doc_type=self.child_type, id=1, parent=2)
        self.es_db.delete(index=self.parent_index,
                          doc_type=self.child_type, id=2, parent=2)


if __name__ == "__main__":
    unittest.main()
