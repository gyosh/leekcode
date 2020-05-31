from lib.vtype import VType

template = '''// {problem_title}
#include <bits/stdc++.h>
using namespace std;
{auxiliary_classes}
// ----- BEGIN CUT HERE -----
{header}
class Solution {{
public:
    {output_type} {method_name}({input_params_type_name}) {{
        // Your solution goes here
    }}
}};

// ------ END CUT HERE ------
{helper_functions}

int nTc;
int passing;
{run_function}

int main() {{
    nTc = 0;
    passing = 0;
    {variable_init}
    {testcases}
    if (passing == nTc) {{
        printf("No error!\\n");
    }} else {{
        printf("FAIL!!!\\n");
    }}
}}
'''

template_run_function='''
int runTc(string _name, {input_params_type_name}, {output_type} _expected) {{
    nTc++;

    {output_type} _answer = Solution().{method_name}({input_params_name});
    if ({equality_check}) return 1;
    else {{
        printf("Error at `%s`\\n", _name.c_str());
        printf("Expected: %s\\n", outputToStr(_expected).c_str());
        printf("Got     : %s\\n\\n", outputToStr(_answer).c_str());
    }}
    return 0;
}}
'''

template_run_function_skip_check='''
int runTc(string _name, {input_params_type_name}, {output_type} _expected) {{
    nTc++;

    {output_type} _answer = Solution().{method_name}({input_params_name});
    printf("On `%s`\\n", _name.c_str());
    printf("Got: %s\\n\\n", outputToStr(_answer).c_str());
    return 1;
}}
'''

template_output_init = '''
    {type} _expected;
    {type} _answer;
'''

template_testcases = '''
    {inputs_init}
    _expected = {output_value};
    passing += runTc("{tc_name}", {input_params_name}, _expected);
'''

template_binary_tree = '''
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}

    static int depth(TreeNode* node) {
        if (!node) return 0;
        int ret = 1;
        if (node->left) ret = max(ret, 1 + depth(node->left));
        if (node->right) ret = max(ret, 1 + depth(node->right));
        return ret;
    }

    static vector<TreeNode*> toList(TreeNode* root) {
        vector<TreeNode*> ret((1<<depth(root)) - 1, nullptr);

        if (!root) return ret;

        vector<pair<int, TreeNode*>> stack;
        stack.push_back(make_pair(0, root));

        while (stack.size() > 0) {
            int idx = stack.back().first;
            TreeNode* node = stack.back().second;
            stack.pop_back();

            ret[idx] = node;
            if (node->left) stack.push_back(make_pair(2*idx+1, node->left));
            if (node->right) stack.push_back(make_pair(2*idx+2, node->right));
        }

        return ret;
    }

    static bool equal(TreeNode* a, TreeNode* b) {
        if ((a == nullptr) && (b == nullptr)) return true;
        if ((a == nullptr) || (b == nullptr)) return false;

        return (a->val == b->val) && equal(a->left, b->left) && equal(a->right, b->right);
    }

    static TreeNode* fromList(vector<TreeNode*> lst) {
        if (lst.size() == 0) return nullptr;

        for (int i = 0; i < lst.size(); i++) {
            int l = 2*i + 1;
            int r = 2*i + 2;
            if (l < lst.size()) lst[i]->left = lst[l];
            if (r < lst.size()) lst[i]->right = lst[r];
        }
        return lst[0];
    }
};
'''

print_boolean = '''
string outputToStr{depth}(bool output) {{
    if (output) return "true";
    return "false";
}}
'''

print_int = '''
string outputToStr{depth}(int output) {{
    return to_string(output);
}}
'''

print_float = '''
string outputToStr{depth}(double output) {{
    return to_string(output);
}}
'''

print_string = '''
string outputToStr{depth}(string output) {{
    return '"' + output + '"';
}}
'''

print_list = '''
string outputToStr{depth}(vector<{child_type}> &output) {{
    string s = "[";
    for (auto v : output) {{
        if (s.length() > 1) s += ",";
        s += outputToStr{next_depth}(v);
    }}
    s += "]";
    return s;  
}}
'''

print_binary_tree = '''
string outputToStr{depth}(TreeNode* output) {{
    vector<TreeNode*> nodes = TreeNode::toList(output);
    string s = "[";
    for (TreeNode* x : nodes) {{
        if (s.length() > 1) s += ",";
        if (x) s += to_string(x->val);
        else s += "null";
    }}
    s += "]";
    return s;
}}
'''

class Cpp:
    @staticmethod
    def generate(problem, skip_check=False, header=''):
        io_spec = problem.io_spec
        output_vtype = io_spec.output_vtype;

        if skip_check:
            run_function = template_run_function_skip_check.format(
                input_params_type_name=Cpp.format_input_params(io_spec),
                output_type=Cpp.format_type(output_vtype),
                method_name=problem.method_name,
                input_params_name=', '.join(io_spec.input_names)
            )
        else:
            run_function = template_run_function.format(
                input_params_type_name=Cpp.format_input_params(io_spec),
                output_type=Cpp.format_type(output_vtype),
                method_name=problem.method_name,
                input_params_name=', '.join(io_spec.input_names),
                equality_check=Cpp.format_equality(output_vtype)
            )

        var_inits = []
        for i in range(io_spec.get_input_size()):
            var_inits.append('{} {};'.format(
                Cpp.format_type(io_spec.input_vtypes[i]),
                io_spec.input_names[i]
            ))
        var_inits.append(template_output_init.format(type=Cpp.format_type(output_vtype)));

        auxiliary_classes = ''
        if io_spec.has_etype(VType.BINARY_TREE):
            auxiliary_classes += template_binary_tree

        return template.format(
                problem_title=problem.title,
                header=header,
                method_name=problem.method_name,
                auxiliary_classes=auxiliary_classes,
                variable_init='\n    '.join(var_inits),
                output_type=Cpp.format_type(output_vtype),
                input_params_type_name=Cpp.format_input_params(io_spec),
                helper_functions=Cpp.format_display_function(output_vtype),
                run_function=run_function,
                testcases=Cpp.format_testcases(problem.method_name, problem.testcases, skip_check)
            )
     

    @staticmethod
    def format_input_params(io_spec):
        params = []
        for i in range(io_spec.get_input_size()):
            type_s = Cpp.format_type(io_spec.input_vtypes[i])
            name = io_spec.input_names[i]
            if io_spec.input_vtypes[i].is_etype(VType.LIST):
                name = '&' + name
            params.append('{} {}'.format(type_s, name))
        return ', '.join(params)


    @staticmethod
    def format_testcases(method_name, testcases, skip_check):
        results = []
        for tc in testcases:
            io_spec = tc.io_spec
            input_inits = []
            for i in range(io_spec.get_input_size()):
                input_inits.append('{} = {};'.format(
                    io_spec.input_names[i],
                    Cpp.format_value_for_init(io_spec.input_vtypes[i], tc.inputs[i])
                ))

            tc_block = template_testcases.format(
                inputs_init='\n    '.join(input_inits),
                output_type=Cpp.format_type(io_spec.output_vtype),
                output_value=Cpp.format_value_for_init(io_spec.output_vtype, tc.output),
                tc_name=tc.title,
                input_params_name=', '.join(io_spec.input_names)
            )

            results.append(tc_block)
        return ''.join(results)


    @staticmethod
    def format_display_function(vtype, depth=0):
        if vtype.is_etype(VType.INTEGER):
            return print_int.format(depth=Cpp.format_depth_str(depth))
        if vtype.is_etype(VType.FLOAT):
            return print_float.format(depth=Cpp.format_depth_str(depth))
        if vtype.is_etype(VType.BOOLEAN):
            return print_boolean.format(depth=Cpp.format_depth_str(depth))
        if vtype.is_etype(VType.STRING):
            return print_string.format(depth=Cpp.format_depth_str(depth))
        if vtype.is_etype(VType.LIST):
            return Cpp.format_display_function(vtype.child, depth+1) + '\n' + print_list.format(
                depth=Cpp.format_depth_str(depth),
                next_depth=Cpp.format_depth_str(depth+1),
                child_type=Cpp.format_type(vtype.child)
            )
        if vtype.is_etype(VType.BINARY_TREE):
            return print_binary_tree.format(depth=Cpp.format_depth_str(depth))

        raise Exception('Unknown data type: {}'.format(vtype))


    @staticmethod
    def format_depth_str(depth):
        return '' if depth == 0 else str(depth)


    @staticmethod
    def format_equality(vtype):
        if vtype.is_etype(VType.BINARY_TREE):
            return 'TreeNode::equal(_expected, _answer)'
        elif vtype.is_etype(VType.FLOAT):
            return 'fabs(_expected - _answer) < 1e-5'
        else:
            return '_expected == _answer'


    @staticmethod
    def format_type(vtype):
        if vtype.is_etype(VType.INTEGER):
            return 'int'
        if vtype.is_etype(VType.FLOAT):
            return 'double'
        if vtype.is_etype(VType.BOOLEAN):
            return 'bool'
        if vtype.is_etype(VType.STRING):
            return 'string'
        if vtype.is_etype(VType.LIST):
            return 'vector<{}>'.format(Cpp.format_type(vtype.child))
        if vtype.is_etype(VType.BINARY_TREE):
            if not vtype.child.is_etype(VType.INTEGER):
                raise Exception('Unsupported binary tree inner data type: {}'.format(vtype.child))
            return 'TreeNode*'
        raise Exception('Unknown data type: {}'.format(vtype))


    @staticmethod
    def format_value_for_init(vtype, value):
        if vtype.is_etype(VType.INTEGER):
            return str(value)
        if vtype.is_etype(VType.FLOAT):
            return str(value)
        elif vtype.is_etype(VType.STRING):
            return "'" + value + "'"
        elif vtype.is_etype(VType.BOOLEAN):
            return str(value).lower()
        elif vtype.is_etype(VType.NULL):
            return 'None'
        elif vtype.is_etype(VType.LIST):
            return '{' + ','.join([Cpp.format_value_for_init(vtype.child, x) for x in value]) + '}'
        elif vtype.is_etype(VType.BINARY_TREE):
            elements = []
            for x in value:
                if x is None:
                    elements.append('nullptr')
                else:
                    elements.append('new TreeNode({})'.format(x))
            return 'TreeNode::fromList({' + ', '.join(elements) + '})'
        raise Exception('Unknown data type: with value {}'.format(value))
