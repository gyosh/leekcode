template_cpp = '''// Generated
#include <bits/stdc++.h>
using namespace std;

class Solution {{
public:
  {output_type} {method_name}({input_params}) {{

  }}
}};

{helper_functions}

int main() {{
  Solution solution = Solution();

  int nTc = {n_testcases};
  int passing = 0;

  {testcases}

  if (passing == nTc) {{
    printf("ALL PASSING YO\\n");
  }} else {{
    printf("SOMETHING IS BAD MAN\\n");
  }}
}}
'''

template_testcases_cpp = '''
  {{
    {inputs_init}
    {output_type} expected = {output_value};
    {output_type} answer = solution.{method_name}({param_names});
    if (expected == answer) {{
      passing++;
    }} else {{
      printf("Error at `{tc_name}`\\n");
      printf("Expected: %s\\n", outputToStr(expected).c_str());
      printf("Got     : %s\\n\\n", outputToStr(answer).c_str());
    }}
  }}'''

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
