import logging
from .vtype import VType
from .phrase_iterator import PhraseIterator

'''
Example for s:
  numPerson = 5, love = [1,4,2,3,0]

value_only is used when s has no variable name, e.g:
  ["typically","on","output"]

'''
def extract_variables(s, value_only=False):
    result = []
    it = PhraseIterator(s + ',')

    def parse_type_and_value():
        c = it.current_char()

        vtype = None
        value = None
        if c == '"':
            vtype = VType(VType.STRING)
            it.skip('"')
            value = ''
            # Process per escape section
            while it.current_char() != '"':
                value += it.skip_r(r'[^\\"]+')
                if it.current_char() == '\\':
                    it.next_char()
                    value += it.next_char()
            it.skip('"')
        elif c in 'tf':
            vtype = VType(VType.BOOLEAN)
            value = True if c == 't' else False
            it.skip(str(value).lower())
        elif c == 'n':
            vtype = VType(VType.NULL)
            value = None
            it.skip('null')
        elif (c == '-') or (('0' <= c) and (c <= '9')):
            vtype = VType(VType.INTEGER)
            value = int(it.skip_r(r'[-0-9]+'))
        else:
            vtype = VType(VType.LIST)
            value = []
            it.skip('[')
            element_type = VType(VType.NULL)
            while it.current_char() != ']':
                candidate_element_type, element_value = parse_type_and_value()
                value.append(element_value)
                if not candidate_element_type.is_ambiguous():
                    element_type = candidate_element_type
                if not it.can_skip(','):
                    break
                it.skip(',')
            vtype.set_child(element_type)
            it.skip(']')
        return vtype, value

    while not it.end():
        name = None
        if not value_only:
            name = it.skip_r(r'[_a-zA-Z0-9]+').strip()
            logging.info('Found variable name: `%s`', name)

            it.skip_r(r'\s*')
            it.skip_r('=')
            it.skip_r(r'\s*')
        vtype, value = parse_type_and_value()
        logging.info('Found variable type : value: `%s`: `%s`', vtype, value)
        result.append((name, vtype, value))
        it.skip_r(r'\s*')
        it.skip_r(r',')
        it.skip_r(r'\s*')
    return result