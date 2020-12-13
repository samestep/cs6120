import lesson2.common as l2common


def parse_asm(asm):
    return {"instrs": [i.strip().replace(";", "") for i in asm.splitlines()[1:-1]]}


def is_label(i):
    return i.startswith(".") and i.endswith(":")


def label_name(i):
    return i[1:-1]


def is_terminator(i):
    return i.split(" ")[0] in {"jmp", "br"}


def labels_referenced(i):
    split = i.split(" ")
    labels = None
    if split[0] == "jmp":
        labels = [split[1]]
    elif split[0] == "br":
        labels = split[2:]
    if labels:
        return [label[1:] for label in labels]


basic_blocks = l2common.basic_blocks_fn(
    is_label=is_label,
    label_name=label_name,
    is_terminator=is_terminator,
    labels_referenced=labels_referenced,
)


cfg = l2common.cfg_fn(is_terminator=is_terminator, labels_referenced=labels_referenced)
