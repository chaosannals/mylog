
from typing_extensions import Self

class F:
    def __self__(self, *argv):
        '''
        
        '''

    @classmethod
    def COUNT(cls, *argv):
        return F(argv)


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
    


class ColumnHandler:
    '''
    
    '''

    def __init__(self, table, name):
        '''
        
        '''
        self.table = table
        self.name = name

class TableHandler:
    '''
    
    '''

    def __init__(self, name):
        self.name = name

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