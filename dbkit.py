
from typing_extensions import Self

class F:
    def __self__(self, *argv):
        '''
        
        '''

    @classmethod
    def COUNT(cls, *argv) -> Self:
        return F(*argv)




class QueryHandler:
    '''
    
    '''

    def __init__(self, table, operation):
        '''
        
        '''

        self.table = table
        self.operation = operation

    def join(self) -> Self:
        return self
    
    def where(self) -> Self:
        return self
    
class TermHandler:
    '''
    
    '''

    def __init__(self):
        '''
        
        '''

    def __lt__(self, other) -> Self:
        return self

class ColumnHandler:
    '''
    
    '''

    def __init__(self, table, name):
        '''
        
        '''
        self.table = table
        self.name = name

    def in_(self, x) -> TermHandler:
        return TermHandler()

    def not_in(self, x) -> TermHandler:
        return TermHandler()

    def __lt__(self, other) -> TermHandler:
        return TermHandler()

    def __gt__(self, other) -> TermHandler:
        return TermHandler()

    def __eq__(self, other) -> TermHandler:
        return TermHandler()

class TableHandler:
    '''
    
    '''

    def __init__(self, name):
        self.__name = name

    def __getattr__(self, name: str) -> ColumnHandler:
        return ColumnHandler(self, name)

    def select(self, *argv, **argkw) -> QueryHandler:
        return QueryHandler(self, 'select')

    def update(self, **argkw) -> QueryHandler:
        return QueryHandler(self, 'update')

    

class DatabaseHandler:
    '''
    
    '''

    def __init__(self):
        '''
        
        '''

    def __getattr__(self, name: str) -> TableHandler:
        return TableHandler(name)

if '__main__' == __name__:
    db = DatabaseHandler()
    print(db.user)
    print(db.user.username)
    print(db.user.select(F.COUNT()).where())

    print(db.user.name.in_([]))
    print(db.user.aaa < db.user.bbb)
    print(db.user.aaa > db.user.bbb)
    print(db.user.aaa == db.user.bbb)