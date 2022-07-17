class BaseFactory:
    
    def __init__(self, factories):
        self.Factories = factories
        self.Connection = factories.getConnection()