import os

from AndroidMkScanner import AndroidMkScanner
from Edge import Edge
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


def ensure_directory(directory, target_name):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return os.path.join(directory, target_name)

def get_edges(root, edges, tracked):
    if root in tracked:
        return
    tracked.append(root)
    for child in root.children:

        get_edges(child, edges, tracked)

        edges.append(Edge(child.name, root.name, "static"))
    tracked.remove(root)

if __name__ == '__main__':
    # android_mks, target_name = get_test_android_mks()
    android_mks, target_name = read_android_mks()

    tree_builder = TreeBuilder(android_mks)

    edges = tree_builder.find_dependencies_of(target_name)
    # edges = tree_builder.build_parents_depend_on_children()
    # edges = tree_builder.build_children_depend_on_parents()

    # edges = []
    # root = tree_builder.build_children_depend_on_parents()
    #
    # tracked = []
    # get_edges(root, edges, tracked)

    plotter = GraphPlotter()
    image_name = ensure_directory('images', target_name + '.svg')
    plotter.create_image(image_name, edges)
