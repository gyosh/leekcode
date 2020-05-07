from .template import *
from .vtype import VType

class Cpp:
    @staticmethod
    def generate(problem):
        io_spec = problem.io_spec
        output_vtype = io_spec.output_vtype;
        result = template_cpp.format(
                method_name=problem.method_name,
                output_type=Cpp.format_type(output_vtype),
                input_params=Cpp.format_input_params(io_spec),
                helper_functions=Cpp.format_display_function(output_vtype),
                n_testcases=len(problem.testcases),
                testcases=Cpp.format_testcases(problem.method_name, problem.testcases)
            )
        print(result)
     

    @staticmethod
    def format_input_params(io_spec):
        params = []
        for i in range(io_spec.get_input_size()):
            type_s = Cpp.format_type(io_spec.input_vtypes[i])
            name = io_spec.input_names[i]
            if io_spec.input_vtypes[i].is_type(VType.LIST):
                name = '&' + name
            params.append('{} {}'.format(type_s, name))
        return ', '.join(params)


    @staticmethod
    def format_testcases(method_name, testcases):
        results = []
        for tc in testcases:
            io_spec = tc.io_spec
            input_inits = []
            for i in range(io_spec.get_input_size()):
                input_inits.append('{} {} = {};'.format(
                    Cpp.format_type(io_spec.input_vtypes[i]),
                    io_spec.input_names[i],
                    Cpp.format_value_for_init(tc.inputs[i])
                ))

            results.append(template_testcases_cpp.format(
                tc_name=tc.title,
                inputs_init='\n    '.join(input_inits),
                output_type=Cpp.format_type(io_spec.output_vtype),
                output_value=Cpp.format_value_for_init(tc.output),
                method_name=method_name,
                param_names=', '.join(io_spec.input_names)
            ))
        return '\n'.join(results)


    @staticmethod
    def format_display_function(vtype, depth=0):
        if vtype.value == VType.INTEGER:
            return cpp_print_int.format(depth=Cpp.format_depth_str(depth))
        if vtype.value == VType.BOOLEAN:
            return cpp_print_boolean.format(depth=Cpp.format_depth_str(depth))
        if vtype.value == VType.STRING:
            return cpp_print_string.format(depth=Cpp.format_depth_str(depth))
        if vtype.value == VType.LIST:
            return Cpp.format_display_function(vtype.child, depth+1) + '\n' + cpp_print_list.format(
                depth=Cpp.format_depth_str(depth),
                next_depth=Cpp.format_depth_str(depth+1),
                child_type=Cpp.format_type(vtype.child)
            )
        return '// UNKNOWN'


    @staticmethod
    def format_depth_str(depth):
        return '' if depth == 0 else str(depth)


    @staticmethod
    def format_type(vtype):
        if vtype.value == VType.INTEGER:
            return 'int'
        if vtype.value == VType.BOOLEAN:
            return 'bool'
        if vtype.value == VType.STRING:
            return 'string'
        if vtype.value == VType.LIST:
            return 'vector<{}>'.format(Cpp.format_type(vtype.child))
        return '?'


    @staticmethod
    def format_value_for_init(value):
        if type(value) is int:
            return str(value)
        elif type(value) is str:
            return '"' + value + '"'
        elif type(value) is bool:
            return str(value).lower()
        elif type(value) is list:
            return '{' + ','.join([Cpp.format_value_for_init(x) for x in value]) + '}'
        return '?'

    