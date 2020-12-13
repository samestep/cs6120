from pathlib import Path

import lesson1 as l1


def asm(n):
    return (Path(__file__).parent / f"asm{n}.txt").read_text()


def test_parse():
    assert l1.parse_asm(asm(0)) == {
        "instrs": [
            "v: int = const 4",
            "jmp .somewhere",
            "v: int = const 2",
            ".somewhere:",
            "print v",
        ]
    }


def test_is_label():
    assert not l1.is_label("v: int = const 4")
    assert not l1.is_label("jmp .somewhere")
    assert l1.is_label(".somewhere:")
    assert not l1.is_label("print v")


def test_label_name():
    assert l1.label_name(".somewhere:") == ".somewhere"


def test_is_terminator():
    assert not l1.is_terminator("v: int = const 4")
    assert l1.is_terminator("jmp .somewhere")
    assert not l1.is_terminator(".somewhere:")
    assert not l1.is_terminator("print v")
    assert l1.is_terminator("br b .there .here")


def test_labels_referenced():
    assert l1.labels_referenced("jmp .somewhere") == {".somewhere"}
    assert l1.labels_referenced("br b .there .here") == {".there", ".here"}


def test_basic_blocks():
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
            ".somewhere": [
                "print v",
            ],
        },
    }
    assert l1.basic_blocks(l1.parse_asm(asm(0))["instrs"]) == out


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
    assert l1.basic_blocks(instrs) == out
