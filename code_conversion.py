import json
import ubjson
import dis
import pprint
import inspect
from types import CodeType


def prep_const(const):
    if inspect.iscode(const):
        return code_to_dict(const)
    return const


def prep_const_list(const):
    if inspect.iscode(const):
        return code_to_list(const)
    return const


code_keys = (
    'argcount',
    'cellvars',
    'code',
    'consts',
    'filename',
    'firstlineno',
    'flags',
    'freevars',
    'kwonlyargcount',
    'lnotab',
    'name',
    'names',
    'nlocals',
    'stacksize',
    'varnames'
)


def code_to_list(compiled_code, prep_func=prep_const_list):
    return [
        compiled_code.co_argcount,
        compiled_code.co_cellvars,
        list(compiled_code.co_code),
        list(map(prep_func, compiled_code.co_consts)),
        compiled_code.co_filename,
        compiled_code.co_firstlineno,
        compiled_code.co_flags,
        compiled_code.co_freevars,
        compiled_code.co_kwonlyargcount,
        list(compiled_code.co_lnotab),
        compiled_code.co_name,
        compiled_code.co_names,
        compiled_code.co_nlocals,
        compiled_code.co_stacksize,
        compiled_code.co_varnames
    ]


def code_to_dict(compiled_code):
    return dict(
        zip(code_keys, code_to_list(compiled_code, prep_const))
    )


def code_to_json(code, compact=False):
    compiled_code = compile(code, '<script>', 'exec')
    # return ubjson.encoder.dumpb(code_to_dict(compiled_code))
    # return json.dumps(code_to_dict(compiled_code), indent=4)

    if compact:
        code_dict = code_to_list(compiled_code)
    else:
        code_dict = code_to_dict(compiled_code)

    if compact:
        return json.dumps(code_dict, indent=None, separators=(',', ':'))
    else:
        return json.dumps(code_dict, indent=4)
