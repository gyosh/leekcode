class IoSpec:
    def __init__(self, input_names, input_vtypes, output_vtype):
        self.input_names = input_names
        self.input_vtypes = input_vtypes
        self.output_vtype = output_vtype

    def get_input_size(self):
        return len(self.input_names)