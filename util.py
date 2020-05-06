template_cpp = '''// Generated
#include <bits/stdc++.h>
using namespace std;

class Solution {{
public:
  {return_type} {method_name}({params}) {{

  }}
}};


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

template_testcases_cpp = '''{{
    {inputs_init}
    {output_type} expected = {output_value};
    {output_type} answer = solution.{method_name}({param_names});
    if (expected == answer)
      passing++;
    else
      printf("Error at `{tc_name}`: expected %d, got %d\\n", expected, answer);
  }}'''