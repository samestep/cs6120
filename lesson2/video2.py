#!/usr/bin/env python3

import json
import sys

import lesson2.common as l2common


def is_label(i):
    return "label" in i


def label_name(i):
    return i["label"]


def is_terminator(i):
    return "labels" in i or i.get("op") == "ret"


def labels_referenced(i):
    return i.get("labels", [])


basic_blocks = l2common.basic_blocks_fn(
    is_label=is_label,
    label_name=label_name,
    is_terminator=is_terminator,
    labels_referenced=labels_referenced,
)


cfg = l2common.cfg_fn(is_terminator=is_terminator, labels_referenced=labels_referenced)


def dot(name, graph):
    print(f"digraph {name} {{")
    for pred, succs in graph.items():
        for succ in succs:
            print(f'    "{pred}" -> "{succ}";')
    print("}")


if __name__ == "__main__":
    functions = json.load(sys.stdin)["functions"]
    for f in functions:
        b = basic_blocks(f["instrs"])
        g = cfg(b["blocks"], b["lbl2block"])
        dot(f["name"], g)
