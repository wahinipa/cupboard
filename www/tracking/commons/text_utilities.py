#  Copyright (c) 2022, Wahinipa LLC

def description_notation_list(description, notation=None, tag=None, label=None):
    if notation is None:
        notation = {}
    if description:
        if tag:
            notation['tag'] = tag
        elif label:
            notation['label'] = label
        lines = description.split('\n')
        if len(lines) > 1:
            notation['lines'] = lines
        else:
            notation['value'] = lines[0]
        return [notation]
    else:
        return []
