import os

from AndroidMk import AndroidMk
from AndroidMkReader import AndroidMkReader
from AndroidModule import AndroidModule


class AndroidMkScanner:

    def __init__(self):
        self._mk_reader = AndroidMkReader()

    def read(self, root_dir):
        android_mks = []

        for file_name in self._get_android_mk_filenames(root_dir):
            modules = self._read_modules(file_name)
            mk = AndroidMk(file_name, modules)
            android_mks.append(mk)

        return android_mks

    def _read_modules(self, file_name):
        modules = {}
        for m in self._mk_reader.read(file_name):
            module = AndroidModule.from_dict(m)
            modules[module.name] = module
        return modules

    @staticmethod
    def _get_android_mk_filenames(root_dir):
        for root, directories, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename == "Android.mk":
                    yield (os.path.join(root, filename))
