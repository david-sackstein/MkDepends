class AndroidModule:

    @classmethod
    def from_name(cls, name):
        return AndroidModule(name, {})

    @classmethod
    def from_dict(cls, dict_):
        name = ''
        if "LOCAL_MODULE" in dict_.keys():
            for i in dict_["LOCAL_MODULE"]:
                name = i
        return AndroidModule(name, dict_)

    def __init__(self, name, dict_):
        self.name = name
        self.shared_libraries = []
        self.static_libraries = []

        if "LOCAL_SHARED_LIBRARIES" in dict_.keys():
            self.shared_libraries = dict_["LOCAL_SHARED_LIBRARIES"]

        if "LOCAL_STATIC_LIBRARIES" in dict_.keys():
            self.static_libraries = dict_["LOCAL_STATIC_LIBRARIES"]

    def __str__(self):
        result = "name = " + self.name
        if self.shared_libraries:
            result += ("\n\tshared_libraries = " + str(self.shared_libraries))
        if self.static_libraries:
            result += ("\n\tstatic_libraries = " + str(self.static_libraries))
        return result
