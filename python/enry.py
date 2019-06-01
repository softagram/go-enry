"""
Python library calling enry Go implementation trough cFFI (API, out-of-line) and Cgo.
"""

from _c_enry import ffi, lib


def go_str_to_py(go_str):
    str_len = go_str.n
    if str_len > 0:
        return ffi.unpack(go_str.p, go_str.n).decode()
    return ""


def py_str_to_go(py_str):
    str_bytes = py_str.encode()
    c_str = ffi.new("char[]", str_bytes)
    go_str = ffi.new("_GoString_ *", [c_str, len(str_bytes)])
    return go_str[0]


def language_by_extension(filename: str) -> str:
    fName = py_str_to_go(filename)
    guess = lib.GetLanguageByExtension(fName)
    lang = go_str_to_py(guess.r0)
    return lang


def language_by_filename(filename: str) -> str:
    fName = py_str_to_go(filename)
    guess = lib.GetLanguageByFilename(fName)
    lang = go_str_to_py(guess.r0)
    return lang


## Test


def main():
    files = ["Parse.hs", "some.cpp", "and.go", "type.h", ".bashrc"]

    print("strategy: extension")
    for filename in files:
        lang = language_by_extension(filename)
        print("file: {:10s} language: '{}'".format(filename, lang))

    print("\nstrategy: filename")
    for filename in files:
        lang = language_by_filename(filename)
        print("file: {:10s} language: '{}'".format(filename, lang))


if __name__ == "__main__":
    main()
