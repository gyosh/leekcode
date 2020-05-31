class VType:
    INTEGER = 'INTEGER'
    FLOAT = 'FLOAT'
    BOOLEAN = 'BOOLEAN'
    STRING = 'STRING'
    NULL = 'NULL'
    LIST = 'LIST'
    BINARY_TREE = 'BINARY_TREE'

    COMPOUND_TYPES = [LIST, BINARY_TREE]

    def __init__(self, value, child=None):
        self.value = value
        self.child = child


    def __str__(self):
        if self.child is None:
            return self.value
        return '{}<{}>'.format(self.value, self.child)


    def set_child(self, child):
        self.child = child


    def is_etype(self, value):
        return self.value == value


    def get_hierarchy(self):
        if self.value not in VType.COMPOUND_TYPES:
            return [self.value]
        return [self.value] + self.child.get_hierarchy()


    def is_ambiguous(self):
        if self.value == VType.NULL:
            return True
        if self.value not in VType.COMPOUND_TYPES:
            return False
        return (self.child is None) or self.child.is_ambiguous()


    def is_superset_of(self, other):
        if self.value == VType.FLOAT:
            if other.is_etype(VType.INTEGER):
                return True

        if self.value in VType.COMPOUND_TYPES:
            if self.child is None:
                return False
            elif other.child is None:
                return True
            else: # Both has child  
                return self.child.is_superset_of(other.child)

        # Anything is superset of NULL
        return other.is_etype(VType.NULL)


    def __eq__(self, other):
        ret = self.value == other.value

        # If one of them has None as child
        if (self.child is None) != (other.child is None):
            return False
        else:
            ret = ret and (self.child == other.child)

        return ret


    def __ne__(self, other):
        return not (self == other)
