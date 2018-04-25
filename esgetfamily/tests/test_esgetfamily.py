import unittest


class TestRequirements(unittest.TestCase):

    def test01(self):
        try:
            from elasticsearch import Elasticsearch
        except ImportError:
            self.assert_(False, "Elasticsearch not installed")


class Test01SingleParent(unittest.TestCase):

    def setUp(self):
        from elasticsearch import Elasticsearch

        try:
            self.es_db = Elasticsearch()
        except:
            self.assertFalse("Elasticsearch Connection can't be made.")

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

        # Indexing Parent
        self.es_db.index(index=self.parent_index, doc_type=self.parent_type,
                         body={u"id": 1, u"name": 'Example', u"age": 1}, id=1)

        # Indexing Children
        self.es_db.index(index=self.parent_index, doc_type=self.child_type,
                         body={u"id": 1, u"name": 'Child1'}, id=1, parent=1)

        self.es_db.index(index=self.parent_index, doc_type=self.child_type,
                         body={u"id": 2, u"name": 'Child2'}, id=2, parent=1)

        import esgetfamily
        self.parents = self.es_db.get(index=self.parent_index,
                                      doc_type=self.parent_type, id=1)
        self.result = esgetfamily.parent_child(self.es_db, self.parents,
                                               self.child_type)

    def test01_keys(self):
        for r in self.result:
            if self.result[r]['child'] and self.result[r]['parent']:
                success = True
            else:
                success = False

        if success:
            self.assertTrue("Test Passed")
        else:
            self.assertFalse("Test Failed")

    def test02_children(self):

        for r in self.result:
            number_of_children = len(self.result[r]['child'])

        if number_of_children == 2:
            self.assertTrue("Test Passed")
        else:
            self.assertFalse("Test Failed")

    def test03_query(self):
        import esgetfamily
        query = {
            "match": {
                "id": 1
            }
        }
        result = esgetfamily.parent_child(self.es_db, self.parents,
                                          self.child_type, query)
        for r in self.result:
            number_of_children = len(result[r]['child'])

        if number_of_children == 1:
            self.assertTrue("Test Passed")
        else:
            self.assertFalse("Test Failed")

    def tearDown(self):
        self.es_db.delete(index=self.parent_index,
                          doc_type=self.parent_type, id=1)

        self.es_db.delete(index=self.parent_index,
                          doc_type=self.child_type, id=1, parent=1)
        self.es_db.delete(index=self.parent_index,
                          doc_type=self.child_type, id=2, parent=1)


class Test02MultipleParent(unittest.TestCase):

    def setUp(self):
        from elasticsearch import Elasticsearch

        try:
            self.es_db = Elasticsearch()
        except:
            self.assertFalse("Elasticsearch Connection can't be made.")

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

        import esgetfamily
        self.parents = [self.es_db.get(index=self.parent_index,
                                       doc_type=self.parent_type, id=1),
                        self.es_db.get(index=self.parent_index,
                                       doc_type=self.parent_type, id=2)]
        self.result = esgetfamily.parent_child(self.es_db, self.parents,
                                               self.child_type)

    def test01_keys(self):
        for r in self.result:
            if self.result[r]['child'] and self.result[r]['parent']:
                success = True
            else:
                success = False

        if success:
            self.assertTrue("Test Passed")
        else:
            self.assertFalse("Test Failed")

    def test02_children(self):
        number_of_children = 0
        for r in self.result:
            number_of_children += len(self.result[r]['child'])

        if number_of_children == 4:
            self.assertTrue("Test Passed")
        else:
            self.assertFalse("Test Failed")

    def test03_query(self):
        import esgetfamily
        number_of_children = 0
        query = {
            "match": {
                "id": 1
            }
        }
        result = esgetfamily.parent_child(self.es_db, self.parents,
                                          self.child_type, query)
        for r in self.result:
            number_of_children += len(result[r]['child'])

        if number_of_children == 2:
            self.assertTrue("Test Passed")
        else:
            self.assertFalse("Test Failed")

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
