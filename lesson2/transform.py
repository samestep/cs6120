#!/usr/bin/env python3

import json
import sys


def transform(prog):
    for f in prog["functions"]:
        instrs = []
        for i in f["instrs"]:
            instrs.append(i)
            if "dest" in i:
                instrs.append(
                    {
                        "op": "id",
                        "dest": i["dest"],
                        "type": i["type"],
                        "args": [i["dest"]],
                    }
                )
        f["instrs"] = instrs
    return prog


if __name__ == "__main__":
    print(json.dumps(transform(json.load(sys.stdin))))
