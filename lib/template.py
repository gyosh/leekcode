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
  Solution solution = Solution();

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

template_testcases_cpp = '''
  nTc++;
  {inputs_init}
  __expected = {output_value};
  __answer = solution.{method_name}({param_names});
'''

template_assertion_cpp = '''  if (__expected == __answer) {{
    passing++;
  }} else {{
    printf("Error at `{tc_name}`\\n");
    printf("__expected: %s\\n", outputToStr(__expected).c_str());
    printf("Got     : %s\\n\\n", outputToStr(__answer).c_str());
  }}
'''

template_no_assertion_cpp = '''  printf("On `{tc_name}`\\n");
  printf("Got: %s\\n\\n", outputToStr(__answer).c_str());
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

solution = Solution()

nTc = 0
passing = 0

{testcases}

if passing == nTc:
    print('No error!')
else:
    print('FAIL!!!')

'''

template_testcases_py = '''
nTc += 1
{inputs_init}
__expected = {output_value}
__answer = solution.{method_name}({param_names})
'''

template_assertion_py = '''if __expected == __answer:
    passing += 1
else:
    print('Error at `{tc_name}`')
    print('__expected: {{}}'.format(str(__expected)))
    print('Got     : {{}}'.format(str(__answer)))
'''

template_no_assertion_py = '''print('On `{tc_name}`')
print('Got: {{}}'.format(str(__answer)))
passing += 1
'''
