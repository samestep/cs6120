def basic_blocks_fn(*, is_label, label_name, is_terminator, labels_referenced):
    def basic_blocks(instrs):
        labels = set()
        for i in instrs:
            if is_terminator(i):
                labels |= set(labels_referenced(i))
        blocks = []
        block = []
        lbl2block = {}
        lbl = None
        for i in instrs:
            if not is_label(i):
                block.append(i)
            if (is_label(i) and label_name(i) in labels) or is_terminator(i):
                if block:
                    if lbl:
                        lbl2block[lbl] = len(blocks)
                    blocks.append(block)
                block = []
                lbl = label_name(i) if is_label(i) else None
        if block:
            if lbl:
                lbl2block[lbl] = len(blocks)
            blocks.append(block)
        return {"blocks": blocks, "lbl2block": lbl2block}

    return basic_blocks


def cfg_fn(*, is_terminator, labels_referenced):
    def cfg(blocks, lbl2block):
        block2lbl = {v: k for k, v in lbl2block.items()}
        graph = {}
        for index, block in enumerate(blocks):
            key = block2lbl.get(index, index)
            last = block[-1]
            if is_terminator(last):
                graph[key] = labels_referenced(last)
            elif index + 1 < len(blocks):
                after = index + 1
                graph[key] = [block2lbl.get(after, after)]
        return graph

    return cfg
