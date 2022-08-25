# %%

from uuid import uuid4
from random import choices, randint
from msilib.schema import Error
import yaml


# %%
stream = open("patient.yaml", 'r')
sample_draft, enum_sets = yaml.load_all(stream, yaml.FullLoader)


def buildEnumSet(enum_sets):
    new_enums = {}
    for k, enum in enum_sets.items():
        values = []
        weights = []
        for l in enum:
            values.append(l['name'])
            if 'weight' not in l:
                weights.append(1)
            else:
                weights.append(l['weight'])
        new_enums[k] = [values, weights]
    return new_enums


enum_sets = buildEnumSet(enum_sets)


def checkRandomEnum(s: str):
    if not s:
        return s
    if s[0] != '$':
        return s
    refSet = s[1:]
    if refSet not in enum_sets:
        raise BaseException

    return choices(enum_sets[refSet][0], enum_sets[refSet][1])[0]
    return enum_sets[refSet]


def checkMacro(s: str):
    if not s:
        return s
    if s[0] != '!':
        return s
    macro = s[1:]
    if macro == 'uuid':
        return str(uuid4())
    if 'number' in macro:
        numb_1 = macro[macro.find('(')+1:macro.find(',')]
        numb_2 = macro[macro.find(',')+1:macro.find(')')]
        return randint(int(numb_1), int(numb_2))
    return s



def processStrings(s: str):
    s = checkRandomEnum(s)
    s = checkMacro(s)
    return s

def main():
    for k, v in sample_draft.items():
        if isinstance(v, str):
            sample_draft[k] = processStrings(v)
        else:
            pass
    return sample_draft
        
main()

# checkMacro('!number(1,10000000)')
