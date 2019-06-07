from final import *
from os import getcwd, path
import pytest

@pytest.mark.parametrize("input_1, expected", [(WriteNote(), WriteNote), (ReadNote("hello_world.txt"), ReadNote)])
def test_write_instance(input_1, expected):
    assert isinstance(input_1, expected)

@pytest.mark.parametrize("expected", [getcwd() + "\\downloads\\"])
def test_delete(expected):
    test_write = WriteNote("test_jk.txt")
    test_write.get_pictures()
    test_write.write_note()
    delete()
    assert path.isdir(expected) == False

@pytest.mark.parametrize("input_1, expected", [("test_jk.txt", getcwd() + "\\downloads\\j"), ("test_jk.txt", getcwd() + "\\downloads\\k")])
def test_make_folders(input_1, expected):
    test = WriteNote(input_1)
    test.get_pictures()
    assert path.isdir(expected) == True

def test_breaking_word():
    test = WriteNote("test_jk.txt")
    assert test.message == "j k"
    test.get_pictures()
    assert test.message == ""