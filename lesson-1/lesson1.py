def parse_asm(asm):
    return {"instrs": [i.strip().replace(";", "") for i in asm.splitlines()[1:-1]]}


def is_label(i):
    return i.startswith(".") and i.endswith(":")


def label_name(i):
    return i[:-1]


def is_terminator(i):
    return i.split(" ")[0] in {"jmp", "br"}


def labels_referenced(i):
    split = i.split(" ")
    if split[0] == "jmp":
        return {split[1]}
    elif split[0] == "br":
        return set(split[2:])


def basic_blocks(instrs):
    labels = set()
    for i in instrs:
        if is_terminator(i):
            for label in labels_referenced(i):
                labels.add(label)
    blocks = []
    block = []
    lbl2block = {}
    lbl = None
    for i in instrs:
        if not is_label(i):
            block.append(i)
        if (is_label(i) and label_name(i) in labels) or is_terminator(i):
            blocks.append(block)
            if lbl:
                lbl2block[lbl] = block
            block = []
            lbl = label_name(i) if is_label(i) else None
    if block:
        blocks.append(block)
        if lbl:
            lbl2block[lbl] = block
    return {"blocks": blocks, "lbl2block": lbl2block}
