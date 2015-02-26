# vim:set ft=python ts=4 sw=4 sts=4 autoindent:

'''
SQLite storage back-end.

Author:     Pontus Stenetorp    <pontus stenetorp se>
Version:    2015-02-25
'''

from json import dumps, loads
from sqlite3 import connect

from store import Store
from error import NotFound

class SQLiteStore(Store):
    '''
    SQLite storage back-end.
    '''

    def __init__(self, path=None, id_key=None):
        super(SQLiteStore, self).__init__(id_key)
        self.conn = connect(':memory:' if path is None else path)

        # Database initialisation.
        self.curse = self.conn.cursor()
        self.curse.execute('''
        CREATE TABLE IF NOT EXISTS objs(
            id  STRING,
            obj STRING,

            PRIMARY KEY(id)
        );
        ''')
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def put(self, obj, id_=None):
        if id_ is None:
            id_ = self.obj_id(obj)
        self.curse.execute('INSERT OR REPLACE INTO objs VALUES (?, ?);',
            (id_, dumps(obj), ))
        self.conn.commit()
        self.curse.execute('SELECT last_insert_rowid();')
        return self.curse.fetchone()[0]

    def insert(self, obj):
        try:
            id_ = self.obj_id(obj)
        except KeyError:
            id_ = self._assign_id(obj)
        return self.put(obj)

    def get(self, id_):
        self.curse.execute('SELECT obj FROM objs WHERE id=?;', (id_, ))
        res = self.curse.fetchone()
        if res is None:
            raise NotFound
        return loads(res[0])

    def delete(self, id_):
        self.curse.execute('DELETE FROM objs WHERE id=?;', (id_, ))
        self.conn.commit()
        self.curse.execute('SELECT changes();')
        changes = self.curse.fetchone()[0]
        if changes != 1:
            assert False # TODO: Decide on exception.
        return changes

    def ids(self):
        self.curse.execute('SELECT id FROM objs;')
        return [res[0] for res in self.curse.fetchall()]

    def _assign_id(self, obj):
        raise NotImplementedError
