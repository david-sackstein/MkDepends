import os

from AndroidMk import AndroidMk
from AndroidModule import AndroidModule

variable_names = {"LOCAL_MODULE", "LOCAL_SHARED_LIBRARIES", "LOCAL_STATIC_LIBRARIES"}


class AndroidMkReader:

    def read(self, android_mk):

        with open(android_mk, "r") as file:

            modules = {}
            is_in_assignment = False
            curr_name = None

            for line in file.readlines():
                line = line.strip()

                if line.startswith("#"):
                    continue

                is_start_assignment, name, values, has_trailing_slash = self._get_assignment(line, is_in_assignment)

                if is_start_assignment:
                    if name == "LOCAL_MODULE":
                        if modules:
                            yield modules
                            modules = {}
                            is_in_assignment = False
                            curr_name = None

                    if name in modules.keys():
                        modules[name].update(values)
                    else:
                        modules[name] = values
                elif is_in_assignment:
                    modules[curr_name].update(values)

                if not is_in_assignment and is_start_assignment:
                    is_in_assignment = True
                    curr_name = name

                if is_in_assignment and not has_trailing_slash:
                    is_in_assignment = False

            if modules:
                yield modules

    @staticmethod
    def _get_values(line):
        return {v for v in line.split()}

    @staticmethod
    def _is_assignment(line):
        return line.startswith(":=") or line.startswith("+=")

    def _get_assignment(self, line, is_in_assignment):

        has_trailing_slash = line.endswith("\\")
        if has_trailing_slash:
            line = line[:-1]

        for name in variable_names:
            if line.startswith(name):

                remainder = line[len(name):].strip()

                if self._is_assignment(remainder):
                    values = self._get_values(remainder[2:].strip())
                    return True, name, values, has_trailing_slash

        if is_in_assignment:
            values = self._get_values(line)
            return False, None, values, has_trailing_slash

        return False, None, [], has_trailing_slash
