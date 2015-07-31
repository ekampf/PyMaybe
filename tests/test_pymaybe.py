#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pymaybe
----------------------------------

Tests for `pymaybe` module.
"""

import sys
import unittest
import doctest

from pymaybe import maybe, Something, Nothing

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

def load_tests(loader, tests, ignore):
    import pymaybe
    tests.addTests(doctest.DocTestSuite(pymaybe, globs=pymaybe.get_doctest_globs()))
    return tests

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

class TestPyMaybe(unittest.TestCase):

    def test_maybe_withValue_returnsSomething(self):
        result = maybe("Value")
        self.assertIsInstance(result, Something)

    def test_maybe_withMaybe_returnMaybe(self):
        m = maybe("value")
        self.assertEqual(maybe(m), m)

    def test_maybe_withNone_returnsNothing(self):
        result = maybe(None)
        self.assertIsInstance(result, Nothing)


    #region Nothing - Comparison
    def test_nothing_cmp(self):
        if PY2:
            self.assertEqual(0, cmp(Nothing(), Nothing()))
            self.assertEqual(1, cmp(1, Nothing()))
            self.assertEqual(1, cmp(Something(5), Nothing()))
            self.assertEqual(1, cmp(5, Nothing()))
            self.assertEqual(-1, cmp(Nothing(), Something(5)))
            self.assertEqual(-1, cmp(Nothing(), 5))

    def test_nothing_equalToNothing(self):
        self.assertTrue(Nothing() == Nothing())

    def test_nothing_notEqualToSomething(self):
        self.assertFalse(Nothing() == Something(2))
        self.assertFalse(Something(1) == Nothing())

    def test_nothing_neSomething(self):
        self.assertTrue(Nothing() != Something(2))
        self.assertTrue(Something(1) != Nothing())

    def test_nothing_neNothing(self):
        self.assertFalse(Nothing() != Nothing())

    def test_nothing_ltNothing_isFalse(self):
        self.assertFalse(Nothing() < Nothing())

    def test_nothing_ltSomething_isTrue(self):
        self.assertTrue(Nothing() < Something(1))

    def test_nothing_ltNone_isFalse(self):
        self.assertFalse(Nothing() < None)

    def test_nothing_ltNotNone_isFalse(self):
        self.assertTrue(Nothing() < "some")

    def test_nothing_gtAnything_isFalse(self):
        self.assertFalse(Nothing() > Nothing())
        self.assertFalse(Nothing() > Something(123))
        self.assertFalse(Nothing() > None)
        self.assertFalse(Nothing() > "Value")

    def test_nothing_leAnything_isTrue(self):
        self.assertTrue(Nothing() <= Nothing())
        self.assertTrue(Nothing() <= Something(123))
        self.assertTrue(Nothing() <= None)
        self.assertTrue(Nothing() <= "Value")

    def test_nothing_geNothing_isTrue(self):
        self.assertTrue(Nothing() >= Nothing())

    def test_nothing_geNone_isTrue(self):
        self.assertTrue(Nothing() >= None)

    def test_nothing_geNotNoneOrNothing_isFalse(self):
        self.assertFalse(Nothing() >= Something(2))
        self.assertFalse(Nothing() >= "some")

    #endregion

    #region Nothing - Dict
    def test_nothing_len_isZero(self):
        self.assertEqual(len(Nothing()), 0)

    def test_nothing_getItem_returnsNothing(self):
        n = Nothing()['name']
        self.assertTrue(isinstance(n, Nothing))
        self.assertTrue(n.is_none())
        self.assertFalse(n.is_some())

    def test_nothing_setItem_doestNothing(self):
        Nothing()['name'] = 'value'  # Will raise if __setitem__ wasnt defined

    def test_nothing_delItem_doestNothing(self):
        del Nothing()['name']  # Will raise if __delitem__ wasnt defined

    #endregion

    #region Nothing - Custom representation
    def test_nothing_repr(self):
        self.assertEqual(repr(Nothing()), repr(None))

    def test_nothing_str(self):
        self.assertEqual(str(Nothing()), str(None))

    def test_nothing_unicode(self):
        if PY2:
            self.assertEqual(unicode(Nothing()), unicode(None))

    def test_nothing_nonzero_isFalse(self):
        self.assertFalse(bool(Nothing()))
    #endregion


    #region Nothing - Misc Methods

    def test_nothing_length_isZero(self):
        self.assertEqual(len(Nothing()), 0)

    def test_nothing_getItem_returnsNone(self):
        result = Nothing()[10]
        self.assertIsInstance(result, Nothing)

    def test_nothing_strings_returnNone(self):
        n = Nothing()
        self.assertEqual(str(n), str(None))

    #endregion

    #region Something - Comparison
    def test_something_cmp(self):
        if PY2:
            n = Nothing()
            s = maybe(5)
            s1 = maybe(7)

            self.assertEqual(1, cmp(s, n))
            self.assertEqual(cmp(5, 5), cmp(s, s))
            self.assertEqual(cmp(5, 7), cmp(s, s1))
            self.assertEqual(cmp(7, 5), cmp(s1, s))
            self.assertEqual(cmp(5, 5), cmp(s, 5))
            self.assertEqual(cmp(5, 7), cmp(s, 7))
            self.assertEqual(cmp(7, 5), cmp(7, s))

    def test_something_cmp_greaterThanNothong(self):
        l = [Something(0), Nothing()]
        sortedl = sorted(l)
        self.assertTrue(isinstance(sortedl[0], Nothing))
        self.assertTrue(isinstance(sortedl[1], Something))

    def test_something_cmp_handlesComparisonBetweenSomethings(self):
        l = [Something(10), Something(3)]
        sortedl = sorted(l)
        self.assertTrue(isinstance(sortedl[0], Something))
        self.assertTrue(isinstance(sortedl[1], Something))

        self.assertEqual(sortedl[0], 3)
        self.assertEqual(sortedl[1], 10)

    def test_something_notEqualToNothing(self):
        self.assertFalse(Something(1) == Nothing())
        self.assertFalse(Nothing() == Something(2))

    def test_something_ltNothing_isFalse(self):
        self.assertFalse(Something("value") < Nothing())

    def test_something_ltSomething_usesValue(self):
        self.assertFalse(Something(3) < Something(1))
        self.assertTrue(Something(3) > Something(1))

    def test_something_gtNothing_isTrue(self):
        self.assertTrue(Something("value") > Nothing())

    def test_something_leNothing_isFalse(self):
        self.assertFalse(Something("value") <= Nothing())

    def test_something_geNothing_isTrue(self):
        self.assertTrue(Something("value") >= Nothing())

    #endregion

    def test_something_conversions(self):
        s = "value"
        d = dict(name="Eran")
        n = 123
        f = 3.14

        if PY2:
            self.assertEqual(unicode(Something(s)), s)

            self.assertEqual(long(Something(n)), n)
            self.assertIsInstance(long(Something(f)), long)

        self.assertEqual(str(Something(s)), s)

        self.assertEqual(repr(Something(s)), repr(s))
        self.assertEqual(repr(Something(d)),  repr(d))

        self.assertEqual(int(Something(n)), n)
        self.assertIsInstance(int(Something(n)), int)

        self.assertEqual(float(Something(f)), f)
        self.assertIsInstance(float(Something(f)), float)





    #region method call forwarding

    def test_something_forwardsMethodCalls(self):
        result = maybe('VALUE').lower()
        assert result.is_some()
        assert result == 'value', "result %s should be 'value'" % result
        assert result == maybe('value')

    def test_something_forwardsMethodCalls_handlesNonExisting(self):
        result = maybe('VALUE').lowerr()
        assert result.is_none()

    def test_nothing_forwardsMethodCalls_handlesNonExisting(self):
        result = maybe(None).invalid().call()
        assert result.is_none()

    #endregion

    # region Assertions (for compatibility between Python version)

    def assertIsInstance(self, obj, cls, msg=None):
        result = isinstance(obj, cls)
        self.assertTrue(result, msg=msg)

    #endregion


if __name__ == '__main__':
    unittest.main()
