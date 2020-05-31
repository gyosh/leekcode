from .language_interface import LanguageInterface
from lib.vtype import VType

template = '''# {problem_title}
from collections import *
import math
{auxiliary_classes}
# ----- BEGIN CUT HERE -----
{header}
class Solution:
    def {method_name}(self, {input_params}):
        # Your solution goes here

# ------ END CUT HERE ------

nTc = 0
passing = 0
{run_function}
{testcases}

if passing == nTc:
    print('No error!')
else:
    print('FAIL!!!')
'''

template_testcases = '''
{inputs_init}
_expected = {output_value}
passing += runTc(\'{tc_name}\', {input_params}, _expected)
'''

template_run_function='''
def runTc(_name, {param_names}, _expected):
    global nTc
    nTc += 1

    _answer = Solution().{method_name}({param_names})
    if {equality_check}:
        return 1
    print('Error at `{{}}`'.format(_name))
    print('Expected: {{}}'.format(str(_expected)))
    print('Got     : {{}}\\n'.format(str(_answer)))
    return 0
'''

template_run_function_skip_check='''
def runTc(_name, {param_names}, _expected=None):
    global nTc
    nTc += 1

    _answer = Solution().{method_name}({param_names})
    print('On `{{}}`'.format(_name))
    print('Got: {{}}\\n'.format(str(_answer)))    
    return 1
'''

template_binary_tree = '''
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __eq__(self, other):
        if other is None:
            return False
        return (self.val != other.val) and (self.left == other.left) and (self.right == other.right)

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return str(self.to_list())

    def depth(self):
        ret = 1
        if self.left is not None:
            ret = max(ret, 1 + self.left.depth())
        if self.right is not None:
            ret = max(ret, 1 + self.right.depth())
        return ret

    def to_list(self):
        ret = [None] * (2**self.depth() - 1)
        stack = [(0, self)]
        while len(stack) > 0:
            idx, node = stack.pop()
            ret[idx] = node.val
            if node.left is not None:
                stack.append((2*idx+1, node.left))
            if node.right is not None:
                stack.append((2*idx+2, node.right))
        return ret

    @staticmethod
    def from_list(lst):
        n = len(lst)
        if n == 0:
            return None

        nodes = [TreeNode(x) for x in lst]
        for i in range(n):
            l = 2*i + 1
            r = 2*i + 2
            if (l < n) and (lst[l] is not None):
                nodes[i].left = nodes[l]
            if (r < n) and (lst[r] is not None):
                nodes[i].right = nodes[r]
        return nodes[0]

'''

class Python3(LanguageInterface):
    @staticmethod
    def generate(problem, skip_check=False, header=''):
        io_spec = problem.io_spec
        output_vtype = io_spec.output_vtype;

        if skip_check:
            run_function = template_run_function_skip_check.format(
                method_name=problem.method_name,
                param_names=', '.join(io_spec.input_names)
            )
        else:
            run_function = template_run_function.format(
                method_name=problem.method_name,
                param_names=', '.join(io_spec.input_names),
                equality_check=Python3.format_equality(output_vtype)
            )

        auxiliary_classes = ''
        if io_spec.has_etype(VType.BINARY_TREE):
            auxiliary_classes += template_binary_tree

        return template.format(
                problem_title=problem.title,
                header=header,
                method_name=problem.method_name,
                auxiliary_classes=auxiliary_classes,
                run_function=run_function,
                input_params=', '.join(io_spec.input_names),
                testcases=Python3.format_testcases(problem.method_name, problem.testcases)
            )


    @staticmethod
    def format_testcases(method_name, testcases):
        results = []
        for tc in testcases:
            io_spec = tc.io_spec
            input_inits = []
            for i in range(io_spec.get_input_size()):
                input_inits.append('{} = {}'.format(
                    io_spec.input_names[i],
                    Python3.format_value_for_init(io_spec.input_vtypes[i], tc.inputs[i])
                ))

            tc_block = template_testcases.format(
                tc_name=tc.title,
                inputs_init='\n'.join(input_inits),
                input_params=', '.join(io_spec.input_names),
                output_value=Python3.format_value_for_init(io_spec.output_vtype, tc.output),
            )

            results.append(tc_block)
        return ''.join(results)


    @staticmethod
    def format_value_for_init(vtype, value):
        if vtype.is_etype(VType.INTEGER):
            return str(value)
        if vtype.is_etype(VType.FLOAT):
            return str(value)
        elif vtype.is_etype(VType.STRING):
            return "'" + value + "'"
        elif vtype.is_etype(VType.BOOLEAN):
            return str(value)
        elif vtype.is_etype(VType.NULL):
            return 'None'
        elif vtype.is_etype(VType.LIST):
            return '[' + ','.join([Python3.format_value_for_init(vtype.child, x) for x in value]) + ']'
        elif vtype.is_etype(VType.BINARY_TREE):
            return 'TreeNode.from_list([' + ','.join([Python3.format_value_for_init(vtype.child, x) for x in value]) + '])'
        raise Exception('Unknown data type: {} with value {}'.format(vtype, value))


    @staticmethod
    def format_equality(vtype):
        if vtype.is_etype(VType.FLOAT):
            return 'abs(_expected - _answer) < 1e-5'
        else:
            return '_expected == _answer'
