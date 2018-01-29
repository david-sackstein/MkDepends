import os

from AndroidMkScanner import AndroidMkScanner
from GraphPlotter import GraphPlotter
from AndroidMk import AndroidMk
from AndroidModule import AndroidModule
from TreeBuilder import TreeBuilder


def get_test_android_mks():
    a = AndroidMk("", make_modules({
        'LOCAL_MODULE': 'A',
        'LOCAL_SHARED_LIBRARIES': ['B', 'C']}))

    b = AndroidMk("", make_modules({
        'LOCAL_MODULE': 'B',
        'LOCAL_SHARED_LIBRARIES': ['C']}))

    c = AndroidMk("", make_modules({
        'LOCAL_MODULE': 'C',
        'LOCAL_SHARED_LIBRARIES': []}))

    android_mks = [a, b, c]

    return android_mks, "A"


def make_modules(dict_):
    module = AndroidModule.from_dict(dict_)
    return {module.name: module}


def read_android_mks():

    root_dir = "/data2/dsackstein/source/nova"
    target = 'libidentitycommon'

    print ("Reading all Android.mk files under " + root_dir)

    reader = AndroidMkScanner()

    print ("Analyzing all modules that {0} depends on".format(target))

    return reader.read(root_dir), target


def ensure_directory(directory, target_name_):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return os.path.join(directory, target_name_)

if __name__ == '__main__':
    android_mks, target_name = get_test_android_mks()
    # android_mks, target_name = read_android_mks()

    tree_builder = TreeBuilder(android_mks)

    root_nodes, leaf_nodes = tree_builder.build()

    plotter = GraphPlotter()
    image_name = ensure_directory('images', target_name + '.svg')
    plotter.create_image(image_name, tree_builder._node_map.values())
