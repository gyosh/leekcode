class VType:
    INTEGER = 'INTEGER'
    BOOLEAN = 'BOOLEAN'
    STRING = 'STRING'
    LIST = 'LIST'
    def __init__(self, value, child=None):
        self.value = value
        self.child = child

    def __str__(self):
        if self.child is None:
            return self.value
        return '{}<{}>'.format(self.value, self.child)

    def set_child(self, child):
        self.child = child

    def is_type(self, value):
        return self.value == value

    def get_hierarchy(self):
        if self.value != VType.LIST:
            return [self.value]
        return [self.value] + self.child.get_hierarchy()