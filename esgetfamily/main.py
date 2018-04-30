from elasticsearch import NotFoundError

scroll_time = '5m'


def get_child(es_db, parent_index, parent_type, parent_ids, child_type,
              match_query=None):

    if match_query is None:
        match_query = {}

    try:
        result = {}
        childs = []
        child = es_db.search(index=parent_index, doc_type=child_type, body={
            "query": {
                "bool":
                    {
                        "must": [
                            {
                                "has_parent": {
                                    "parent_type": parent_type,
                                    "query": {
                                        "ids": {
                                            "values": parent_ids
                                        }
                                    }
                                }
                            },
                            match_query
                        ]
                    }
            }
        }, scroll=scroll_time)
        sid = child['_scroll_id']

        scroll_size = len(child['hits']['hits'])
        childs.extend(child['hits'][u'hits'])

        while scroll_size > 0:
            child = es_db.scroll(scroll_id=sid, scroll=scroll_time)
            if child['hits'][u'hits']:
                childs.extend(child['hits'][u'hits'])
            sid = child['_scroll_id']
            scroll_size = len(child['hits']['hits'])

        result = childs

        if child['hits']['total'] == 0:
            return {}

        return result

    except NotFoundError:
        return {}


def parent_child(es_db, list_parents, child_type, match_query=None):

    if match_query is None:
        match_query = {}

    ids = []
    parents = []

    try:
        for par in list_parents:
            ids.append(par[u'_id'])
            parent_index = par[u'_index']
            parent_type = par[u'_type']
        parents = list_parents
    except TypeError:
        ids.append(int(list_parents[u'_id']))
        parent_index = list_parents[u'_index']
        parent_type = list_parents[u'_type']
        parents.append(list_parents)

    child = get_child(es_db, parent_index, parent_type, ids, child_type,
                      match_query)

    final = {}
    for parent in parents:
        pcdict = {}
        childs = []
        pcdict['parent'] = parent

        for c in child:
            if c['_parent'] == parent['_id']:
                childs.append(c)
        pcdict['child'] = childs

        final[parent['_id']] = pcdict

    return final
