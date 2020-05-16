template_cpp = '''// {problem_title}
#include <bits/stdc++.h>
using namespace std;

// ----- BEGIN CUT HERE -----

#define REP(a,b) for (int a = 0; a < b; a++)
#define FOR(a,b,c) for (int a = b; a <= c; a++)
#define RESET(a,b) memset(a,b,sizeof(a))
#define LL long long

const int INF = 2123123123;
const int MOD = 1000000007;

class Solution {{
public:
  {output_type} {method_name}({input_params}) {{

  }}
}};

// ------ END CUT HERE ------
{helper_functions}

int main() {{
  Solution solution;

  int nTc = 0;
  int passing = 0;
  {variable_init}
  {testcases}

  if (passing == nTc) {{
    printf("No error!\\n");
  }} else {{
    printf("FAIL!!!\\n");
  }}
}}
'''

template_output_init_cpp = '{} _expected, _answer;'

template_testcases_cpp = '''
  solution = Solution();
  nTc++;
  {inputs_init}
  _expected = {output_value};
  _answer = solution.{method_name}({param_names});
'''

template_assertion_cpp = '''  if (_expected == _answer) {{
    passing++;
  }} else {{
    printf("Error at `{tc_name}`\\n");
    printf("Expected: %s\\n", outputToStr(_expected).c_str());
    printf("Got     : %s\\n\\n", outputToStr(_answer).c_str());
  }}
'''

template_no_assertion_cpp = '''  printf("On `{tc_name}`\\n");
  printf("Got: %s\\n\\n", outputToStr(_answer).c_str());
  passing++;
'''

cpp_print_boolean = '''
string outputToStr{depth}(bool output) {{
  if (output) return "true";
  return "false";
}}
'''

cpp_print_int = '''
string outputToStr{depth}(int output) {{
  return to_string(output);
}}
'''

cpp_print_string = '''
string outputToStr{depth}(string output) {{
  return '"' + output + '"';
}}
'''

cpp_print_list = '''
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


template_py = '''# {problem_title}
from collections import *

# ----- BEGIN CUT HERE -----

MOD = 1000000007
INF = 2123123123

class Solution:
    def {method_name}(self, {input_params}):


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

template_testcases_py = '''{inputs_init}
passing += runTc(\'{tc_name}\', {input_params}, {output_value})
'''

# template_assertion_py = '''if _expected == _answer:
#     passing += 1
# else:
#     print('Error at `{tc_name}`')
#     print('Expected: {{}}'.format(str(_expected)))
#     print('Got     : {{}}\\n'.format(str(_answer)))
# '''

# template_no_assertion_py = '''print('On `{tc_name}`')
# print('Got: {{}}\\n'.format(str(_answer)))
# passing += 1
# '''

template_run_function_py='''
def runTc(_name, {param_names}, _expected):
    global nTc
    nTc += 1

    _answer = Solution().{method_name}({param_names})
    if _expected == _answer:
        return 1
    print('Error at `{{}}`'.format(_name))
    print('Expected: {{}}'.format(str(_expected)))
    print('Got     : {{}}\\n'.format(str(_answer)))
    return 0
'''

template_run_function_skip_check_py='''
def runTc(_name, {param_names}, _expected=None):
    global nTc
    nTc += 1

    _answer = Solution().{method_name}({param_names})
    print('On `{{}}`'.format(_name))
    print('Got: {{}}\\n'.format(str(_answer)))    
    return 1
'''

