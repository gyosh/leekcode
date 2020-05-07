from .template import *
from .vtype import VType

class Cpp:
    def __init__(self, problem):
        self.problem = problem


    def generate(self):
        output_vtype = self.problem.io_spec.output_vtype;
        result = template_cpp.format(
                method_name=self.problem.method_name,
                output_type=self.get_type(output_vtype),
                input_params=self.get_input_params(),
                helper_functions=self.get_display_function(output_vtype),
                n_testcases=len(self.problem.testcases),
                testcases=self.get_testcases()
            )
        print(result)
     

    def get_input_params(self):
        params = []
        io_spec = self.problem.io_spec
        for i in range(io_spec.get_input_size()):
            type_s = self.get_type(io_spec.input_vtypes[i])
            name = io_spec.input_names[i]
            if io_spec.input_vtypes[i].is_type(VType.LIST):
                name = '&' + name
            params.append('{} {}'.format(type_s, name))
        return ', '.join(params)


    def get_testcases(self):
        results = []
        for tc in self.problem.testcases:
            io_spec = tc.io_spec
            input_inits = []
            for i in range(io_spec.get_input_size()):
                input_inits.append('{} {} = {};'.format(
                    self.get_type(io_spec.input_vtypes[i]),
                    io_spec.input_names[i],
                    self.get_value_for_init(tc.inputs[i])
                ))

            results.append(template_testcases_cpp.format(
                tc_name=tc.title,
                inputs_init='\n    '.join(input_inits),
                output_type=self.get_type(io_spec.output_vtype),
                output_value=self.get_value_for_init(tc.output),
                method_name=self.problem.method_name,
                param_names=', '.join(io_spec.input_names)
            ))
        return '\n'.join(results)


    def get_display_function(self, vtype, depth=0):
        if vtype.value == VType.INTEGER:
            return cpp_print_int.format(depth=self.get_depth_str(depth))
        if vtype.value == VType.BOOLEAN:
            return cpp_print_boolean.format(depth=self.get_depth_str(depth))
        if vtype.value == VType.STRING:
            return cpp_print_string.format(depth=self.get_depth_str(depth))
        if vtype.value == VType.LIST:
            return self.get_display_function(vtype.child, depth+1) + '\n' + cpp_print_list.format(
                depth=self.get_depth_str(depth),
                next_depth=self.get_depth_str(depth+1),
                child_type=self.get_type(vtype.child)
            )
        return '// UNKNOWN'


    def get_depth_str(self, depth):
        return '' if depth == 0 else str(depth)


    def get_type(self, vtype):
        if vtype.value == VType.INTEGER:
            return 'int'
        if vtype.value == VType.BOOLEAN:
            return 'bool'
        if vtype.value == VType.STRING:
            return 'string'
        if vtype.value == VType.LIST:
            return 'vector<{}>'.format(self.get_type(vtype.child))
        return '?'


    def get_value_for_init(self, value):
        if type(value) is int:
            return str(value)
        elif type(value) is str:
            return '"' + value + '"'
        elif type(value) is bool:
            return str(value).lower()
        elif type(value) is list:
            return '{' + ','.join([self.get_value_for_init(x) for x in value]) + '}'
        return '?'

