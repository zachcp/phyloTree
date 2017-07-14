import json
from io import StringIO

import pandas as pd
import numpy as np

from Bio import Phylo


def adorntree(tree, dataframe):
    """

    """
    dataframe = dataframe.set_index("node")
    nodevals = dataframe.to_dict("index")

    nodes  = set(nodevals.keys())
    rowprops = dataframe.columns

    nodenum=0
    for treenode in tree.find_clades():

        if treenode.name in nodes:
            for attr in rowprops:
                treenode.__setattr__(attr, nodevals[treenode.name][attr])
        else:
            treenode.__setattr__("node", "NODE_{:06d}".format(nodenum))
        
        nodenum+=1
    return tree


def tree_to_json(tree,
                 exclude_attr = ['clades'],
                 default_branch_length=0.01):

    tree_json = {}
    node = tree.root
    nodeprops = {key: value for key, value in node.__dict__.items()
                 if not key.startswith("__")
                 and key not in exclude_attr}

    if "name" in nodeprops.keys():
        tree_json["strain"] = nodeprops['name']
    if "id" in nodeprops.keys():
        tree_json["strain"] = nodeprops['id']
    if "node" in nodeprops.keys():
        tree_json["strain"] = nodeprops['node']

    # add node data
    for key, value in nodeprops.items():
        if value is None:
            if key == "branch_length":
                tree_json["branch_length"] = default_branch_length
        else:
            tree_json[key] = value

    # recur
    if node.clades:
        tree_json["children"] = []
        for ch in node.clades:
            tree_json["children"].append(tree_to_json(ch, exclude_attr))
    return tree_json


def write_json(data, file_name, indent=1):
    try:
        handle = open(file_name, 'w')
    except IOError:
        pass
    else:
        json.dump(data, handle, indent=indent)
        handle.close()


tree = Phylo.read(StringIO("(A, (B, C), (D, E))"), "newick")

Phylo.draw_ascii(tree)
nodes = pd.DataFrame({"node": ["A", "B", "C", "D", "E"],
                      "lat": [10,11,12,13,14],
                      "kind": ["AA", "BA", "CA", "DA", "EA"]})


tree2 = adorntree(tree, nodes)
tree4 = tree_to_json(tree=tree2)
write_json(tree4, "data/testdata.json")
