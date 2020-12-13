from pathlib import Path

import video_1 as l2v1


def asm(n):
    return (Path(__file__).parent / f"asm{n}.bril").read_text()


def test_parse_0():
    assert l2v1.parse_asm(asm(0)) == {
        "instrs": [
            "v: int = const 4",
            "jmp .somewhere",
            "v: int = const 2",
            ".somewhere:",
            "print v",
        ]
    }


def test_parse_1():
    assert l2v1.parse_asm(asm(1)) == {
        "instrs": [
            "v: int = const 4",
            "b: bool = const false",
            "br b .there .here",
            ".here:",
            "v: int = const 2",
            ".there:",
            "print v",
        ]
    }


def test_parse_2():
    assert l2v1.parse_asm(asm(2)) == {
        "instrs": [
            "v0: int = const 8",
            "value: int = id v0",
            "v1: int = const 1",
            "result: int = id v1",
            "v3: int = id value",
            "i: int = id v3",
            ".for.cond:",
            "v4: int = id i",
            "v5: int = const 0",
            "v6: bool = gt v4 v5",
            "br v6 .for.body .for.end",
            ".for.body:",
            "v7: int = id result",
            "v8: int = id i",
            "v9: int = mul v7 v8",
            "result: int = id v9",
            "v10: int = id i",
            "v11: int = const 1",
            "v12: int = sub v10 v11",
            "i: int = id v12",
            "jmp .for.cond",
            ".for.end:",
            "v13: int = id result",
            "print v13",
            "v14: int = const 0",
        ]
    }


def test_is_label():
    assert not l2v1.is_label("v: int = const 4")
    assert not l2v1.is_label("jmp .somewhere")
    assert l2v1.is_label(".somewhere:")
    assert not l2v1.is_label("print v")


def test_label_name():
    assert l2v1.label_name(".somewhere:") == ".somewhere"


def test_is_terminator():
    assert not l2v1.is_terminator("v: int = const 4")
    assert l2v1.is_terminator("jmp .somewhere")
    assert not l2v1.is_terminator(".somewhere:")
    assert not l2v1.is_terminator("print v")
    assert l2v1.is_terminator("br b .there .here")


def test_labels_referenced():
    assert l2v1.labels_referenced("jmp .somewhere") == [".somewhere"]
    assert l2v1.labels_referenced("br b .there .here") == [".there", ".here"]


def test_basic_blocks_0():
    out = {
        "blocks": [
            [
                "v: int = const 4",
                "jmp .somewhere",
            ],
            [
                "v: int = const 2",
            ],
            [
                "print v",
            ],
        ],
        "lbl2block": {
            ".somewhere": 2,
        },
    }
    assert l2v1.basic_blocks(l2v1.parse_asm(asm(0))["instrs"]) == out


def test_basic_blocks_1():
    out = {
        "blocks": [
            [
                "v: int = const 4",
                "b: bool = const false",
                "br b .there .here",
            ],
            [
                "v: int = const 2",
            ],
            [
                "print v",
            ],
        ],
        "lbl2block": {
            ".here": 1,
            ".there": 2,
        },
    }
    assert l2v1.basic_blocks(l2v1.parse_asm(asm(1))["instrs"]) == out


def test_basic_blocks_2():
    out = {
        "blocks": [
            [
                "v0: int = const 8",
                "value: int = id v0",
                "v1: int = const 1",
                "result: int = id v1",
                "v3: int = id value",
                "i: int = id v3",
            ],
            [
                "v4: int = id i",
                "v5: int = const 0",
                "v6: bool = gt v4 v5",
                "br v6 .for.body .for.end",
            ],
            [
                "v7: int = id result",
                "v8: int = id i",
                "v9: int = mul v7 v8",
                "result: int = id v9",
                "v10: int = id i",
                "v11: int = const 1",
                "v12: int = sub v10 v11",
                "i: int = id v12",
                "jmp .for.cond",
            ],
            [
                "v13: int = id result",
                "print v13",
                "v14: int = const 0",
            ],
        ],
        "lbl2block": {
            ".for.cond": 1,
            ".for.body": 2,
            ".for.end": 3,
        },
    }
    assert l2v1.basic_blocks(l2v1.parse_asm(asm(2))["instrs"]) == out


def test_basic_blocks_maximal():
    instrs = [
        "x: int = const 10",
        ".foo:",
        "x: int = const 20",
    ]
    out = {
        "blocks": [
            [
                "x: int = const 10",
                "x: int = const 20",
            ]
        ],
        "lbl2block": {},
    }
    assert l2v1.basic_blocks(instrs) == out


def test_cfg_0():
    blocks = l2v1.basic_blocks(l2v1.parse_asm(asm(0))["instrs"])
    out = {
        0: [".somewhere"],
        1: [".somewhere"],
    }
    assert l2v1.cfg(blocks["blocks"], blocks["lbl2block"]) == out


def test_cfg_1():
    blocks = l2v1.basic_blocks(l2v1.parse_asm(asm(1))["instrs"])
    out = {
        0: [".there", ".here"],
        ".here": [".there"],
    }
    assert l2v1.cfg(blocks["blocks"], blocks["lbl2block"]) == out


def test_cfg_2():
    blocks = l2v1.basic_blocks(l2v1.parse_asm(asm(2))["instrs"])
    out = {
        0: [".for.cond"],
        ".for.cond": [".for.body", ".for.end"],
        ".for.body": [".for.cond"],
    }
    assert l2v1.cfg(blocks["blocks"], blocks["lbl2block"]) == out
