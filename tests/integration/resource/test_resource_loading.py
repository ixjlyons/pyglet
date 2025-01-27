#!/usr/bin/env python

"""
Layout:

.                               (script home)
    file.txt                    F1
    dir1/
        file.txt                F2
        dir1/
            file.txt            F3
        res.zip/
            file.txt            F7
            dir1/
                file.txt        F8
                dir1/
                    file.txt    F9
    dir2/
        file.txt                F6

"""

import os
import unittest

from pyglet import resource
from pyglet.compat import asbytes

from ...annotations import Platform, require_platform


class ResourceLoadingTestCase(unittest.TestCase):
    def setUp(self):
        self.script_home = os.path.dirname(__file__)

    def check(self, path, result):
        self.check_file(path, 'file.txt', result)

    def check_file(self, path, file, result):
        loader = resource.Loader(path, script_home=self.script_home)
        self.assertTrue(loader.file(file).read() == asbytes('%s\n' % result))

    def checkFail(self, path):
        loader = resource.Loader(path, script_home=self.script_home)
        self.assertRaises(resource.ResourceNotFoundException, loader.file, 'file.txt')

    def test1(self):
        self.check(None, 'F1')

    def test2(self):
        self.check('', 'F1')

    def test2a(self):
        self.check('.', 'F1')

    def test2b(self):
        self.checkFail(())

    def test2c(self):
        self.checkFail('foo')

    def test2d(self):
        self.checkFail(['foo'])

    def test2e(self):
        self.check(['foo', '.'], 'F1')

    def test3(self):
        self.check(['.', 'dir1'], 'F1')

    def test4(self):
        self.check(['dir1'], 'F2')

    def test5(self):
        self.check(['dir1', '.'], 'F2')

    def test6(self):
        self.check(['dir1/dir1'], 'F3')

    @require_platform(Platform.WINDOWS)
    def test6_win(self):
        self.check([r'dir1\\dir1'], 'F3')

    def test7(self):
        self.check(['dir1', 'dir1/dir1'], 'F2')

    @require_platform(Platform.WINDOWS)
    def test7_win(self):
        self.check(['dir1', r'dir1\\dir1'], 'F2')

    def test8(self):
        self.check(['dir1/dir1', 'dir1'], 'F3')

    @require_platform(Platform.WINDOWS)
    def test8_win(self):
        self.check([r'dir1\\dir1', 'dir1'], 'F3')

    def test9(self):
        self.check('dir1/res.zip', 'F7')

    @require_platform(Platform.WINDOWS)
    def test9_win(self):
        self.check(r'dir1\\res.zip', 'F7')

    def test9a(self):
        self.check('dir1/res.zip/', 'F7')

    @require_platform(Platform.WINDOWS)
    def test9a_win(self):
        self.check(r'dir1\\res.zip\\', 'F7')

    def test10(self):
        self.check('dir1/res.zip/dir1', 'F8')

    @require_platform(Platform.WINDOWS)
    def test10_win(self):
        self.check(r'dir1\\res.zip\dir1', 'F8')

    def test10a(self):
        self.check('dir1/res.zip/dir1/', 'F8')

    @require_platform(Platform.WINDOWS)
    def test10a_win(self):
        self.check(r'dir1\\res.zip\dir1\\', 'F8')

    def test11(self):
        self.check(['dir1/res.zip/dir1', 'dir1/res.zip'], 'F8')

    @require_platform(Platform.WINDOWS)
    def test11_win(self):
        self.check([r'dir1\\res.zip\dir1', r'dir1\\res.zip'], 'F8')

    def test12(self):
        self.check(['dir1/res.zip', 'dir1/res.zip/dir1'], 'F7')

    @require_platform(Platform.WINDOWS)
    def test12_win(self):
        self.check([r'dir1\\res.zip', r'dir1\\res.zip\dir1'], 'F7')

    def test12a(self):
        self.check(['dir1/res.zip', 'dir1/res.zip/dir1/dir1'], 'F7')

    @require_platform(Platform.WINDOWS)
    def test12a_win(self):
        self.check([r'dir1\\res.zip', r'dir1\\res.zip\\dir1\\dir1'], 'F7')

    def test12b(self):
        self.check(['dir1/res.zip/dir1/dir1/', 'dir1/res.zip/dir1'], 'F9')

    @require_platform(Platform.WINDOWS)
    def test12b_win(self):
        self.check([r'dir1\\res.zip\\dir1\\dir1\\', r'dir1\\res.zip\\dir1'], 'F9')

    def test12c(self):
        self.check(['dir1/res.zip/dir1/dir1', 'dir1/res.zip/dir1'], 'F9')

    @require_platform(Platform.WINDOWS)
    def test12c_win(self):
        self.check([r'dir1\\res.zip\\dir1/\\dir1', r'dir1\\res.zip\\dir1'], 'F9')

    def test13(self):
        self.check(['dir1', 'dir2'], 'F2')

    def test14(self):
        self.check(['dir2', 'dir1'], 'F6')

    # path tests

    def test15(self):
        self.check_file([''], 'dir1/file.txt', 'F2')

    @require_platform(Platform.WINDOWS)
    def test15_win(self):
        self.check_file([''], r'dir1\\file.txt', 'F2')

    def test15a(self):
        self.check_file([''], 'dir1/dir1/file.txt', 'F3')

    @require_platform(Platform.WINDOWS)
    def test15a_win(self):
        self.check_file([''], r'dir1\\dir1\\file.txt', 'F3')

    def test15b(self):
        self.check_file(['dir1'], 'dir1/file.txt', 'F3')

    @require_platform(Platform.WINDOWS)
    def test15b_win(self):
        self.check_file(['dir1'], r'dir1\\file.txt', 'F3')

    def test15c(self):
        self.check_file([''], 'dir2/file.txt', 'F6')

    @require_platform(Platform.WINDOWS)
    def test15c_win(self):
        self.check_file([''], r'dir2\\file.txt', 'F6')

    def test15d(self):
        self.check_file(['.'], 'dir2/file.txt', 'F6')

    @require_platform(Platform.WINDOWS)
    def test15d_win(self):
        self.check_file(['.'], r'dir2\\file.txt', 'F6')

    # zip path tests

    def test16(self):
        self.check_file(['dir1/res.zip'], 'dir1/file.txt', 'F8')

    @require_platform(Platform.WINDOWS)
    def test16_win(self):
        self.check_file([r'dir1\\res.zip'], r'dir1\\file.txt', 'F8')

    def test16a(self):
        self.check_file(['dir1/res.zip/'], 'dir1/file.txt', 'F8')

    @require_platform(Platform.WINDOWS)
    def test16a_win(self):
        self.check_file([r'dir1\\res.zip\\'], r'dir1\\file.txt', 'F8')

    def test16b(self):
        self.check_file(['dir1/res.zip/'], 'dir1/dir1/file.txt', 'F9')

    @require_platform(Platform.WINDOWS)
    def test16b_win(self):
        self.check_file([r'dir1\\res.zip\\'], r'dir1\\dir1\\file.txt', 'F9')

    def test16c(self):
        self.check_file(['dir1/res.zip/dir1'], 'dir1/file.txt', 'F9')

    @require_platform(Platform.WINDOWS)
    def test16c_win(self):
        self.check_file([r'dir1\\res.zip\\dir1'], r'dir1\\file.txt', 'F9')

    def test16d(self):
        self.check_file(['dir1/res.zip/dir1/'], 'dir1/file.txt', 'F9')

    @require_platform(Platform.WINDOWS)
    def test16d_win(self):
        self.check_file([r'dir1\\res.zip\\dir1\\'], r'dir1\\file.txt', 'F9')
