# Elasticsearch: Get Family - Python

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/plotlabs/esgetfamily-python/blob/master/LICENSE.txt) [![Build Status](https://travis-ci.org/plotlabs/esgetfamily-python.svg?branch=master)](https://travis-ci.org/plotlabs/esgetfamily-python) [![CodeFactor](https://www.codefactor.io/repository/github/plotlabs/esgetfamily-python/badge)](https://www.codefactor.io/repository/github/plotlabs/esgetfamily-python) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://www.plotlabs.io/) [![PyPI](https://img.shields.io/pypi/v/esgetfamily.svg)](https://pypi.org/project/esgetfamily/)

_This package returns the parent and its children together. This is compatible with elasticsearch version >=5.0.0,<6.0.0._

```python
from elasticsearch import Elasticsearch  
import esgetfamily

def get_es_object():  
    es = Elasticsearch(elastic_cred)  
    return es  

es_db = get_es_object()  
```

> **For single parent:**

```python
parents = es_db.get(index=parent_index, doc_type=parent_type, id=parent_id)  
final = esgetfamily.parent_child(es_db, parents, child_type)
```

> **For single parent with query for child:**

```python
query = {  
    "match": {  
        "id": 1  
    }  
}

parents = es_db.get(index=parent_index, doc_type=parent_type, id=parent_id)  
final = esgetfamily.parent_child(es_db, parents, child_type, query)
```

> **For multiple parents:**

```python
parents = [es_db.get(index=parent_index, doc_type=parent_type, id=parent_id),  
           es_db.get(index=parent_index, doc_type=parent_type, id=parent_id)]
final = esgetfamily.parent_child(es_db, parents, child_type)
```

> **For multiple parents with query for child:**

```python
query = {  
    "match": {  
        "id": 1  
    }  
}

parents = [es_db.get(index=parent_index, doc_type=parent_type, id=parent_id),  
           es_db.get(index=parent_index, doc_type=parent_type, id=parent_id)]  
final = esgetfamily.parent_child(es_db, parents, child_type, query)
```

> **Sample Example:**

#### Code:

```python
from elasticsearch import Elasticsearch
def get_es_object():  
    es = Elasticsearch(elastic_cred)  
    return es  
es_db = get_es_object()  
import esgetfamily, json

parents = es_db.get(index="parent", doc_type="par", id=3)
final = esgetfamily.parent_child(es_db, parents, "child")
print json.dumps(final, indent=3)
```

#### Result:

```json
{
  "3": {
    "parent": {
      "_type": "par",
      "_source": {
        "age": 23,
        "id": 3,
        "name": "ABC"
      },
      "_index": "parent",
      "_version": 1,
      "found": true,
      "_id": "3"
    },
    "child": [
      {
        "_type": "child",
        "_routing": "3",
        "_index": "parent",
        "_score": 1.0,
        "_source": {
          "id": 1,
          "name": "Child1"
        },
        "_parent": "3",
        "_id": "1"
      },
      {
        "_type": "child",
        "_routing": "3",
        "_index": "parent",
        "_score": 1.0,
        "_source": {
          "id": 2,
          "name": "Child2"
        },
        "_parent": "3",
        "_id": "2"
      }
    ]
  }
}
```
