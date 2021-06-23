"""
Unit tests for the `dqstutil` module.

The following functions are tested:

*  _is_valid_colnames
*  is_numeric
*  is_possible_date
*  is_possible_numeric
*  determine_column_type
*  inspect_dataset
*  extract_unique_values
*  gen_freq_table
*  load_csv_dataset
*  add_column
*  remove_column
*  modify_column
*  transform_column
*  remove_columns
*  extract_row_range
*  extract_rows
"""


import unittest

# Temporary file creation/deletion ('load_csv_dataset')
from os import unlink
from tempfile import NamedTemporaryFile

# Test captured stdout ('inspect_dataset')
from io import StringIO
from contextlib import redirect_stdout

# System-under-test (SUT) module path context
import context

# SUT test entities
from dqstutil import *


class Tests__is_valid_colnames_Function(unittest.TestCase):
    """
    Unit tests for the function, `_is_valid_colnames`.
    """

    def test_arg_wrong_type(self):
        test_result = _is_valid_colnames(['a', 'b', 'c'], {})
        self.assertFalse(test_result)

    def test_arg_is_empty(self):
        test_result = _is_valid_colnames(['a', 'b', 'c'], [])
        self.assertFalse(test_result)

    def test_one_colname_is_missing(self):
        test_result = _is_valid_colnames(['a', 'b', 'c'], ['e', 'c'])
        self.assertFalse(test_result)

    def test_colnames_not_valid(self):
        test_result = _is_valid_colnames(['a', 'b', 'c'], [1, 2])
        self.assertFalse(test_result)

    def test_colname_is_valid(self):
        test_result = _is_valid_colnames(['a', 'b', 'c'], ['b', 'c'])
        self.assertTrue(test_result)


class Tests_is_numeric_Function(unittest.TestCase):
    """
    Unit tests for the function, `is_numeric`.
    """

    def test_arg_wrong_type_01(self):
        test_result = is_numeric([4, 5, 7])
        self.assertFalse(test_result)

    def test_arg_wrong_type_02(self):
        test_result = is_numeric({'a': 5})
        self.assertFalse(test_result)

    def test_accept_integer_string(self):
        test_result = is_numeric('6')
        self.assertTrue(test_result)

    def test_accept_integer(self):
        test_result = is_numeric(6)
        self.assertTrue(test_result)

    def test_accept_float_string(self):
        test_result = is_numeric('4.1')
        self.assertTrue(test_result)

    def test_accept_float(self):
        test_result = is_numeric(4.1)
        self.assertTrue(test_result)

    def test_accept_negative_float_string(self):
        test_result = is_numeric('-4.1')
        self.assertTrue(test_result)

    def test_accept_negative_float(self):
        test_result = is_numeric(-4.1)
        self.assertTrue(test_result)

    def test_reject_non_numeric_string(self):
        test_result = is_numeric('sgsgsg')
        self.assertFalse(test_result)

    def test_reject_version_string(self):
        test_result = is_numeric('4.1.4')
        self.assertFalse(test_result)

    def test_reject_suffixed_integer(self):
        test_result = is_numeric('56M')
        self.assertFalse(test_result)

    def test_accept_complex(self):
        test_result = is_numeric(complex(3, 4))
        self.assertTrue(test_result)


class Tests_is_possible_date_Function(unittest.TestCase):
    """
    Unit tests for the function, `is_possible_date`.
    """

    def test_reject_non_numeric_string(self):
        test_result = is_possible_date('sgsgsg')
        self.assertFalse(test_result)

    def test_accept_forward_slash_date_separator(self):
        test_result = is_possible_date('1/1/1')
        self.assertTrue(test_result)

    def test_reject_extra_forward_slash_date_separator(self):
        test_result = is_possible_date('1/1/1/')
        self.assertFalse(test_result)

    def test_accept_dash_date_separator(self):
        test_result = is_possible_date('1-1-1')
        self.assertTrue(test_result)

    def test_reject_extra_dash_date_separator(self):
        test_result = is_possible_date('1--1-1')
        self.assertFalse(test_result)

    def test_accept_string_with_monthname(self):
        test_result = is_possible_date('January 1, 1999')
        self.assertTrue(test_result)


class Tests_is_possible_numeric_Function(unittest.TestCase):
    """
    Unit tests for the function, `is_possible_numeric`.
    """

    def test_reject_non_numeric_string(self):
        test_result = is_possible_numeric('sgsgsg')
        self.assertFalse(test_result)

    def test_reject_forward_slash_separated_date_string(self):
        test_result = is_possible_numeric('1/1/1')
        self.assertFalse(test_result)

    def test_reject_monthname_date_string(self):
        test_result = is_possible_numeric('January 1, 1999')
        self.assertFalse(test_result)

    def test_accept_suffixed_integer(self):
        test_result = is_possible_numeric('15M')
        self.assertTrue(test_result)

    def test_accept_valid_dollar_currency_string(self):
        test_result = is_possible_numeric('$14.34')
        self.assertTrue(test_result)

    def test_reject_invalid_dollar_currency_string(self):
        test_result = is_possible_numeric('$$59')
        self.assertFalse(test_result)

    def test_accept_comma_delimited_integer_string(self):
        test_result = is_possible_numeric('1,456,234')
        self.assertTrue(test_result)

    def test_reject_version_string(self):
        test_result = is_possible_numeric('1.0.23')
        self.assertFalse(test_result)

    def test_accept_float_string(self):
        test_result = is_possible_numeric('1.23')
        self.assertTrue(test_result)

    def test_accept_possibly_invalid_suffixed_numeric(self):
        test_result = is_possible_numeric('1,7kM')
        self.assertTrue(test_result)


class Tests_determine_column_type_Function(unittest.TestCase):
    """
    Unit tests for the function, `determine_column_type`.
    """

    def test_is_text(self):
        test_result = determine_column_type('sgsgsg')
        self.assertEqual(test_result, 'T')

    def test_is_possible_numeric(self):
        test_result = determine_column_type('15M')
        self.assertEqual(test_result, 'PN')

    def test_is_numeric(self):
        test_result = determine_column_type('-4.1')
        self.assertEqual(test_result, 'N')

    def test_is_possible_date(self):
        test_result = determine_column_type('January 1, 1999')
        self.assertEqual(test_result, 'PD')


class Tests_inspect_dataset_Function(unittest.TestCase):
    """
    Unit tests for the function, `inspect_dataset`.
    """

    def test_return_tuple(self):
        header = ['a', 'b', 'c']
        dataset = [
            ['a1', 'b1', 'c1'],
            ['a2', 'c2'], \
            ['a3', 'b3', 'c3'],
            ['a4', 'bib', '3'],
            ['ay', 'bib', 'x'],
            ['ay', 'bib', 'x']
        ]
        exp_skiprows = [1]
        exp_columns = {'a': {'PN': 3, 'T': 2}, 'b': {'PN': 2, 'T': 3}, 'c': {'PN': 2, 'N': 1, 'T': 2}}
        exp_uniques = {'a': 1, 'b': 1, 'c': 1}
        exp_duplicates = {'a': 1, 'b': 2, 'c': 1}
        skiprows, columns, uniques, duplicates = \
            inspect_dataset(dataset, header, generate_report=False)
        test_result = \
            skiprows == exp_skiprows \
            and columns == exp_columns \
            and uniques == exp_uniques \
            and duplicates == exp_duplicates
        self.assertTrue(test_result)

    def test_report_output(self):
        header = ['a', 'b', 'c']
        dataset = [
            ['a1', 'b1', 'c1'],
            ['a2', 'c2'],
            ['a3', 'b3', 'c3'],
            ['a4', 'bib', '3'],
            ['ay', 'bib', 'x'],
            ['ay', 'bib', 'x']
        ]
        f = StringIO()
        with redirect_stdout(f):
            inspect_dataset(dataset, header, generate_report=True)
        output = f.getvalue()
        exp_output = "Invalid (incorrect length) row numbers:[1]\n\n" \
            + "Tentative column type(s) [T - text, N - numeric, PN - possible numeric, PD - possible date]:\n\n" \
            + "{'a': {'PN': 3, 'T': 2}, 'b': {'PN': 2, 'T': 3}, 'c': {'PN': 2, 'N': 1, 'T': 2}}\n\n" \
            + "Unique value counts (non-numeric and non-date columns only):\n\n" \
            + "{'a': 1, 'b': 1, 'c': 1}\n\n" \
            + "Duplicate value counts (non-numeric and non-date columns only):\n\n" \
            + "{'a': 1, 'b': 2, 'c': 1}\n"
        self.maxDiff = None
        self.assertEqual(output, exp_output)


class Tests_extract_unique_values_Function(unittest.TestCase):
    """
    Unit tests for the function, `extract_unique_values`.
    """

    def test_arg_wrong_type(self):
        values = {'a': 4}
        test_result = extract_unique_values(values)
        self.assertIsNone(test_result)

    def test_arg_is_empty(self):
        values = []
        test_result = extract_unique_values(values)
        self.assertIsNone(test_result)

    def test_arg_wrong_list_element_type_01(self):
        values = ['d', 4, {'a': 4}, [3, 4, 5]]
        test_result = extract_unique_values(values)
        self.assertIsNone(test_result)

    def test_extract_unique_values_ok_01(self):
        values = ['a', 't', 'z', 'k', 'v', 'z', 't']
        uniques = ['a', 't', 'z', 'k', 'v']
        test_result = extract_unique_values(values)
        self.assertEqual(test_result, uniques)

    def test_extract_unique_values_ok_02(self):
        values = [1, 3, 2, 1]
        uniques = [1, 3, 2]
        test_result = extract_unique_values(values)
        self.assertEqual(test_result, uniques)

    def test_extract_unique_values_ok_03(self):
        values = [1, 3, 2, 1]
        uniques = [1, 3, 2]
        test_result = extract_unique_values(values, sort=True)
        self.assertEqual(test_result, sorted(uniques))

    def test_extract_unique_values_ok_04(self):
        values = [
            ['a1'], ['b1'], ['c1'],
            ['a2'], ['b1'], ['c1'],
            ['a1'], ['b2'], ['c1']
        ]
        uniques = ['a1', 'b1', 'c1', 'a2', 'b2']
        test_result = sorted(extract_unique_values(values))
        self.assertEqual(test_result, sorted(uniques))

    def test_extract_unique_values_ok_05(self):
        values = [[1], [2], [3], [1]]
        uniques = [1, 2, 3]
        test_result = extract_unique_values(values)
        self.assertEqual(test_result, uniques)

    def test_extract_unique_values_ok_06(self):
        values = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3'],
            ['a2', 'b2', 'c2']
        ]
        uniques = ['a1|b1|c1', 'a2|b2|c2', 'a3|b3|c3']
        test_result = sorted(extract_unique_values(values))
        self.assertEqual(test_result, sorted(uniques))

    def test_arg_wrong_list_element_type_02(self):
        values = [['a1'], ['b1'], [], ['a2'], ['b1']]
        test_result = extract_unique_values(values)
        self.assertIsNone(test_result)

    def test_arg_wrong_list_element_type_03(self):
        values = [['a1'], ['b1'], 0, ['a2'], ['b1']]
        test_result = extract_unique_values(values)
        self.assertIsNone(test_result)

    def test_arg_wrong_list_element_type_04(self):
        values = [
            ['a1', 'b1', 'c1'],
            [],
            ['a3', 'b3', 'c3'],
            ['a2', 'b2', 'c2']
        ]
        test_result = extract_unique_values(values)
        self.assertIsNone(test_result)

    def test_arg_wrong_list_element_type_05(self):
        values = [
            ['a1', 'b1', 'c1'],
            ['a2', 'c2'],
            ['a3', 'b3', 'c3'],
            ['a2', 'b2', 'c2']
        ]
        test_result = extract_unique_values(values)
        self.assertIsNone(test_result)

    def test_arg_wrong_list_element_type_06(self):
        values = [
            ['a1', 'b1', 'c1'],
            ['a2', 0, 'c2'],
            ['a3', 'b3', 'c3'],
            ['a2', 'b2', 'c2']
        ]
        test_result = extract_unique_values(values)
        self.assertIsNone(test_result)

    def test_extract_unique_values_ok_07(self):
        values = [[11, 12, 13], [34, 0, 85], [11, 12, 13]]
        uniques = ['11|12|13', '34|0|85']
        test_result = sorted(extract_unique_values(values))
        self.assertEqual(test_result, sorted(uniques))


class Tests_gen_freq_table_Function(unittest.TestCase):
    """
    Unit tests for the function, `gen_freq_table`.
    """

    def test_non_existent_column(self):
        header = ['a', 'b', 'c']
        dataset = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3'],
            ['a3', 'b3', 'c3']
        ]
        test_result = gen_freq_table(dataset, header, 'Z')
        self.assertIsNone(test_result)

    def test_freq_count_ok_01(self):
        header = ['a', 'b', 'c']
        dataset = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3'],
            ['a3', 'b3', 'c3']
        ]
        fqt = {'b1': (1, 25.0), 'b2': (1, 25.0), 'b3': (2, 50.0)}
        ret_fqt = gen_freq_table(dataset, header, 'b')
        test_result = \
            all([fqt[k][0] == ret_fqt[k][0]
                for k in fqt if k in ret_fqt]) \
            and fqt.keys() == ret_fqt.keys()
        self.assertTrue(test_result)

    def test_freq_count_ok_02(self):
        header = ['a', 'b', 'c']
        dataset = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3'],
            ['a3', 'b3', 'c3']
        ]
        fqt = {'b3': (2, 50.0), 'b1': (1, 25.0), 'b2': (1, 25.0), }
        ret_fqt = gen_freq_table(dataset, header, 'b',
                                 sort_by_value=True)
        test_result = \
            all([fqt[k][0] == ret_fqt[k][0]
                for k in fqt if k in ret_fqt]) \
            and fqt.keys() == ret_fqt.keys()
        self.assertTrue(test_result)

    def test_freq_count_ok_03(self):
        header = ['a', 'b', 'c']
        dataset = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3'],
            ['a3', 'b3', 'c3']
        ]
        fqt = {'b3': (2, 50.0), 'b2': (1, 25.0), 'b1': (1, 25.0)}
        ret_fqt = gen_freq_table(dataset, header, 'b', reverse=True)
        test_result = \
            all([fqt[k][0] == ret_fqt[k][0]
                for k in fqt if k in ret_fqt]) \
            and fqt.keys() == ret_fqt.keys()
        self.assertTrue(test_result)


class Tests_add_column_Function(unittest.TestCase):
    """
    Unit tests for the function, `add_column`.
    """

    def test_arg_wrong_type(self):
        header = ['a', 'b', 'c']
        dummy = [[], [], []]
        ret_ds, ret_hd = add_column(dummy, header, [], dummy)
        self.assertTrue(ret_ds is None and ret_hd is None)

    def test_arg_is_empty(self):
        header = ['a', 'b', 'c']
        dummy = [[], [], []]
        ret_ds, ret_hd = add_column(dummy, header, '', dummy)
        self.assertTrue(ret_ds is None and ret_hd is None)

    def test_column_already_exists(self):
        header = ['a', 'b', 'c']
        dummy = [[], [], []]
        ret_ds, ret_hd = add_column(dummy, header, 'a', dummy)
        self.assertTrue(ret_ds is None and ret_hd is None)

    def test_add_new_column_ok_return_copy(self):
        orig_hd = ['a', 'b', 'c']
        new_hd = ['a', 'b', 'c', 'd']
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        new_ds = [
            ['a1', 'b1', 'c1', 'd1'],
            ['a2', 'b2', 'c2', 'd2'],
            ['a3', 'b3', 'c3', 'd3']
        ]
        coldata = ['d1', 'd2', 'd3']
        ret_ds, ret_hd = add_column(orig_ds, orig_hd, 'd', coldata)
        cmpds = all(map(lambda p, q: p is not q and p == q,
                        ret_ds, new_ds))
        cmphd = all(map(lambda p, q: p == q, ret_hd, new_hd))
        test_result = \
            ret_ds is not orig_ds \
            and cmpds \
            and ret_hd is not orig_hd \
            and cmphd
        self.assertTrue(test_result)

    def test_add_new_column_ok_return_original(self):
        orig_hd = ['a', 'b', 'c']
        new_hd = ['a', 'b', 'c', 'd']
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        new_ds = [
            ['a1', 'b1', 'c1', 'd1'],
            ['a2', 'b2', 'c2', 'd2'],
            ['a3', 'b3', 'c3', 'd3']
        ]
        coldata = ['d1', 'd2', 'd3']
        ret_ds, ret_hd = add_column(orig_ds, orig_hd, 'd', coldata,
                                    inplace=True)
        cmpds = all(map(lambda p, q, r: p is q and p == q and p == r,
                        ret_ds, orig_ds, new_ds))
        cmphd = all(map(lambda p, q, r: p == q and p == r,
                        ret_hd, orig_hd, new_hd))
        test_result = \
            ret_ds is orig_ds \
            and cmpds \
            and ret_hd is orig_hd \
            and cmphd
        self.assertTrue(test_result)


class Tests_remove_column_Function(unittest.TestCase):
    """
    Unit tests for the function, `remove_column`.
    """

    def test_arg_wrong_type(self):
        header = ['a', 'b', 'c']
        dummy = [[], [], []]
        ret_ds, ret_hd = remove_column(dummy, header, [])
        self.assertTrue(ret_ds is None and ret_hd is None)

    def test_arg_is_empty(self):
        header = ['a', 'b', 'c']
        dummy = [[], [], []]
        ret_ds, ret_hd = remove_column(dummy, header, '')
        self.assertTrue(ret_ds is None and ret_hd is None)

    def test_column_not_exists(self):
        header = ['a', 'b', 'c']
        dummy = [[], [], []]
        ret_ds, ret_hd = remove_column(dummy, header, 'd')
        self.assertTrue(ret_ds is None and ret_hd is None)

    def test_remove_column_ok_return_copy(self):
        orig_hd = ['a', 'b', 'c']
        new_hd = ['a', 'c']
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        new_ds = [
            ['a1', 'c1'],
            ['a2', 'c2'],
            ['a3', 'c3']
        ]
        ret_ds, ret_hd = remove_column(orig_ds, orig_hd, 'b')
        cmpds = all(map(lambda p, q: p is not q and p == q,
                        ret_ds, new_ds))
        cmphd = all(map(lambda p, q: p == q, ret_hd, new_hd))
        test_result = \
            ret_ds is not orig_ds \
            and cmpds \
            and ret_hd is not orig_hd \
            and cmphd
        self.assertTrue(test_result)

    def test_remove_column_ok_return_original(self):
        orig_hd = ['a', 'b', 'c']
        new_hd = ['a', 'c']
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        new_ds = [
            ['a1', 'c1'],
            ['a2', 'c2'],
            ['a3', 'c3']
        ]
        ret_ds, ret_hd = remove_column(orig_ds, orig_hd, 'b',
                                       inplace=True)
        cmpds = all(map(lambda p, q, r: p is q and p == q and p == r,
                        ret_ds, orig_ds, new_ds))
        cmphd = all(map(lambda p, q, r: p == q and p == r,
                        ret_hd, orig_hd, new_hd))
        test_result = \
            ret_ds is orig_ds \
            and cmpds \
            and ret_hd is orig_hd \
            and cmphd
        self.assertTrue(test_result)


class Tests_modify_column_Function(unittest.TestCase):
    """
    Unit tests for the function, `modify_column`.
    """

    def test_arg_wrong_type(self):
        header = ['a', 'b', 'c']
        dummy = [[], [], []]
        ret_ds, ret_hd = modify_column(dummy, header, [], dummy)
        self.assertTrue(ret_ds is None and ret_hd is None)

    def test_arg_is_empty(self):
        header = ['a', 'b', 'c']
        dummy = [[], [], []]
        ret_ds, ret_hd = modify_column(dummy, header, '', dummy)
        self.assertTrue(ret_ds is None and ret_hd is None)

    def test_column_not_exists(self):
        header = ['a', 'b', 'c']
        dummy = [[], [], []]
        ret_ds, ret_hd = modify_column(dummy, header, 'd', dummy)
        self.assertTrue(ret_ds is None and ret_hd is None)

    def test_modify_column_ok_return_copy(self):
        header = ['a', 'b', 'c']
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        new_ds = [
            ['a1', 'X1', 'c1'],
            ['a2', 'X2', 'c2'],
            ['a3', 'X3', 'c3']
        ]
        coldata = ['X1', 'X2', 'X3']
        ret_ds, _ = modify_column(orig_ds, header, 'b', coldata)
        cmpds = all(map(lambda p, q: p is not q and p == q,
                        ret_ds, new_ds))
        test_result = ret_ds is not orig_ds and cmpds
        self.assertTrue(test_result)

    def test_modify_column_ok_return_original(self):
        header = ['a', 'b', 'c']
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        new_ds = [
            ['a1', 'X1', 'c1'],
            ['a2', 'X2', 'c2'],
            ['a3', 'X3', 'c3']
        ]
        coldata = ['X1', 'X2', 'X3']
        ret_ds, _ = modify_column(orig_ds, header, 'b', coldata,
                                  inplace=True)
        cmpds = all(map(lambda p, q, r: p is q and p == q and p == r,
                        ret_ds, orig_ds, new_ds))
        test_result = ret_ds is orig_ds and cmpds
        self.assertTrue(test_result)


class Tests_transform_column_Function(unittest.TestCase):
    """
    Unit tests for the function, `transform_column`.
    """

    def test_arg_wrong_type(self):
        header = ['a', 'b', 'c']
        dummy = [[], [], []]
        transform = lambda x: None
        ret_ds, ret_hd = transform_column(dummy, header, [], transform)
        self.assertTrue(ret_ds is None and ret_hd is None)

    def test_arg_is_empty(self):
        header = ['a', 'b', 'c']
        dummy = [[], [], []]
        transform = lambda x: None
        ret_ds, ret_hd = transform_column(dummy, header, '', transform)
        self.assertTrue(ret_ds is None and ret_hd is None)

    def test_column_not_exists(self):
        header = ['a', 'b', 'c']
        dummy = [[], [], []]
        transform = lambda x: None
        ret_ds, ret_hd = transform_column(dummy, header, 'd', transform)
        self.assertTrue(ret_ds is None and ret_hd is None)

    def test_transform_wrong_type(self):
        header = ['a', 'b', 'c']
        dummy = [[], [], []]
        transform = {}
        ret_ds, ret_hd = transform_column(dummy, header, 'a', transform)
        self.assertTrue(ret_ds is None and ret_hd is None)

    def test_transform_wrong_arg_number(self):
        header = ['a', 'b', 'c']
        dummy = [[], [], []]
        transform = lambda x, y: None
        ret_ds, ret_hd = transform_column(dummy, header, 'a', transform)
        self.assertTrue(ret_ds is None and ret_hd is None)

    def test_transform_ok_return_copy(self):
        header = ['a', 'b', 'c']
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        new_ds = [
            ['a1', 'B1', 'c1'],
            ['a2', 'B2', 'c2'],
            ['a3', 'B3', 'c3']
        ]
        ret_ds, _ = transform_column(orig_ds, header, 'b',
                                     lambda x: x.upper())
        cmpds = all(map(lambda p, q: p is not q and p == q,
                        ret_ds, new_ds))
        test_result = ret_ds is not orig_ds and cmpds
        self.assertTrue(test_result)

    def test_transform_ok_return_original(self):
        header = ['a', 'b', 'c']
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        new_ds = [
            ['a1', 'B1', 'c1'],
            ['a2', 'B2', 'c2'],
            ['a3', 'B3', 'c3']
        ]
        ret_ds, _ = transform_column(orig_ds, header, 'b',
                                     lambda x: x.upper(),
                                     inplace=True)
        cmpds = all(map(lambda p, q, r: p is q and p == q and p == r,
                        ret_ds, orig_ds, new_ds))
        test_result = ret_ds is orig_ds and cmpds
        self.assertTrue(test_result)


class Tests_remove_columns_Function(unittest.TestCase):
    """
    Unit tests for the function, `remove_columns`.
    """

    def test_arg_wrong_type(self):
        header = ['a', 'b', 'c']
        dummy = [[], [], []]
        ret_ds, ret_hd = remove_columns(dummy, header, {})
        self.assertTrue(ret_ds is None and ret_hd is None)

    def test_arg_is_empty(self):
        header = ['a', 'b', 'c']
        dummy = [[], [], []]
        ret_ds, ret_hd = remove_columns(dummy, header, [])
        self.assertTrue(ret_ds is None and ret_hd is None)

    def test_column_not_exists(self):
        header = ['a', 'b', 'c']
        dummy = [[], [], []]
        ret_ds, ret_hd = remove_columns(dummy, header, ['d'])
        self.assertTrue(ret_ds is None and ret_hd is None)

    def test_remove_one_column_ok_return_copy(self):
        orig_hd = ['a', 'b', 'c']
        new_hd = ['a', 'c']
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        new_ds = [
            ['a1', 'c1'],
            ['a2', 'c2'],
            ['a3', 'c3']
        ]
        ret_ds, ret_hd = remove_columns(orig_ds, orig_hd, ['b'])
        cmpds = all(map(lambda p, q: p is not q and p == q,
                        ret_ds, new_ds))
        cmphd = all(map(lambda p, q: p == q, ret_hd, new_hd))
        test_result = \
            ret_ds is not orig_ds \
            and cmpds \
            and ret_hd is not orig_hd \
            and cmphd
        self.assertTrue(test_result)

    def test_remove_one_column_ok_return_original(self):
        orig_hd = ['a', 'b', 'c']
        new_hd = ['a', 'c']
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        new_ds = [
            ['a1', 'c1'],
            ['a2', 'c2'],
            ['a3', 'c3']
        ]
        ret_ds, ret_hd = remove_columns(orig_ds, orig_hd, ['b'],
                                        inplace=True)
        cmpds = all(map(lambda p, q, r: p is q and p == q and p == r,
                        ret_ds, orig_ds, new_ds))
        cmphd = all(map(lambda p, q, r: p == q and p == r,
                        ret_hd, orig_hd, new_hd))
        test_result = \
            ret_ds is orig_ds \
            and cmpds \
            and ret_hd is orig_hd \
            and cmphd
        self.assertTrue(test_result)

    def test_remove_multiple_columns_ok_return_copy(self):
        orig_hd = ['a', 'b', 'c']
        new_hd = ['b']
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        new_ds = [
            ['b1'],
            ['b2'],
            ['b3']
        ]
        ret_ds, ret_hd = remove_columns(orig_ds, orig_hd, ['a', 'c'])
        cmpds = all(map(lambda p, q: p is not q and p == q,
                        ret_ds, new_ds))
        cmphd = all(map(lambda p, q: p == q, ret_hd, new_hd))
        test_result = \
            ret_ds is not orig_ds \
            and cmpds \
            and ret_hd is not orig_hd \
            and cmphd
        self.assertTrue(test_result)

    def test_remove_multiple_columns_ok_return_original(self):
        orig_hd = ['a', 'b', 'c']
        new_hd = ['b']
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        new_ds = [
            ['b1'],
            ['b2'],
            ['b3']
        ]
        ret_ds, ret_hd = remove_columns(orig_ds, orig_hd, ['a', 'c'],
                                        inplace=True)
        cmpds = all(map(lambda p, q, r: p is q and p == q and p == r,
                        ret_ds, orig_ds, new_ds))
        cmphd = all(map(lambda p, q, r: p == q and p == r,
                        ret_hd, orig_hd, new_hd))
        test_result = \
            ret_ds is orig_ds \
            and cmpds \
            and ret_hd is orig_hd \
            and cmphd
        self.assertTrue(test_result)

    def test_remove_all_columns_ok_return_copy(self):
        orig_hd = ['a', 'b', 'c']
        new_hd = []
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        new_ds = []
        ret_ds, ret_hd = remove_columns(orig_ds, orig_hd, ['a', 'b', 'c'])
        cmpds = all(map(lambda p, q: p is not q and p == q,
                        ret_ds, new_ds))
        cmphd = all(map(lambda p, q: p == q, ret_hd, new_hd))
        test_result = \
            ret_ds is not orig_ds \
            and cmpds \
            and ret_hd is not orig_hd \
            and cmphd
        self.assertTrue(test_result)

    def test_remove_all_columns_ok_return_original(self):
        orig_hd = ['a', 'b', 'c']
        new_hd = []
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        new_ds = []
        ret_ds, ret_hd = remove_columns(orig_ds, orig_hd, ['a', 'c'],
                                        inplace=True)
        cmpds = all(map(lambda p, q, r: p is q and p == q and p == r,
                        ret_ds, orig_ds, new_ds))
        cmphd = all(map(lambda p, q, r: p == q and p == r,
                        ret_hd, orig_hd, new_hd))
        test_result = \
            ret_ds is orig_ds \
            and cmpds \
            and ret_hd is orig_hd \
            and cmphd
        self.assertTrue(test_result)


class Tests_extract_row_range_Function(unittest.TestCase):
    """
    Unit tests for the function, `extract_row_range`.
    """

    def test_negative_lower_bound(self):
        dummy = [[], [], []]
        self.assertIsNone(extract_row_range(dummy, [-1, 2]))

    def test_lower_bound_gt_upper_bound(self):
        dummy = [[], [], []]
        self.assertIsNone(extract_row_range(dummy, [2, 1]))

    def test_lower_bound_out_of_range(self):
        dummy = [[], [], []]
        self.assertIsNone(extract_row_range(dummy, [3, 1]))

    def test_upper_bound_out_of_range(self):
        dummy = [[], [], []]
        self.assertIsNone(extract_row_range(dummy, [1, 4]))

    def test_multiple_rows_ok(self):
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        exp_ds = [
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        ret_ds = extract_row_range(orig_ds, [1, 2])
        self.assertTrue(ret_ds == exp_ds and ret_ds is not exp_ds)

    def test_single_row_ok(self):
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        exp_ds = [
            ['a2', 'b2', 'c2'],
        ]
        ret_ds = extract_row_range(orig_ds, [1, 1])
        self.assertTrue(ret_ds == exp_ds and ret_ds is not exp_ds)


class Tests_extract_rows_Function(unittest.TestCase):
    """
    Unit tests for the function, `extract_rows`.
    """

    def test_predicate_wrong_type(self):
        header = ['a', 'b', 'c']
        dummy = [[], [], []]
        predicate = []
        self.assertIsNone(extract_rows(dummy, header, predicate))

    def test_predicate_wrong_arg_number(self):
        header = ['a', 'b', 'c']
        dummy = [[], [], []]
        predicate = lambda x, y, z: None
        self.assertIsNone(extract_rows(dummy, header, predicate))

    def test_extract_all_rows_and_all_columns(self):
        header = ['a', 'b', 'c']
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        exp_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        predicate = lambda row, header: True
        ret_ds, _ = extract_rows(orig_ds, header, predicate)
        self.assertTrue(ret_ds is not orig_ds and ret_ds == exp_ds)

    def test_extract_select_rows_and_all_columns(self):
        header = ['a', 'b', 'c']
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        exp_ds = [
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        predicate = lambda row, header: row[header.index('c')] > 'c1'
        ret_ds, _ = extract_rows(orig_ds, header, predicate)
        self.assertTrue(ret_ds is not orig_ds and ret_ds == exp_ds)

    def test_columns_list_is_empty(self):
        header = ['a', 'b', 'c']
        dummy = [['a1', 'b1', 'c1'], ['a2', 'b2', 'c2']]
        predicate = lambda row, header: True
        colnames = []
        self.assertIsNone(extract_rows(dummy, header, predicate,
                                       colnames))

    def test_non_existent_column(self):
        header = ['a', 'b', 'c']
        dummy = [['a1', 'b1', 'c1'], ['a2', 'b2', 'c2']]
        predicate = lambda row, header: True
        colnames = ['a', 'd']
        self.assertIsNone(extract_rows(dummy, header, predicate,
                                       colnames))

    def test_extract_all_rows_and_select_columns(self):
        orig_hd = ['a', 'b', 'c']
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        exp_hd = ['a', 'c']
        exp_ds = [
            ['a1', 'c1'],
            ['a2', 'c2'],
            ['a3', 'c3']
        ]
        predicate = lambda row, header: True
        ret_ds, ret_hd = extract_rows(orig_ds, orig_hd, predicate,
                                      ['a', 'c'])
        test_result = \
            ret_ds is not orig_ds \
            and ret_ds == exp_ds \
            and ret_hd is not orig_hd \
            and ret_hd == exp_hd
        self.assertTrue(test_result)

    def test_extract_select_rows_and_select_columns(self):
        orig_hd = ['a', 'b', 'c']
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3']
        ]
        exp_hd = ['a', 'c']
        exp_ds = [
            ['a2', 'c2'],
            ['a3', 'c3']
        ]
        predicate = lambda row, header: row[header.index('c')] > 'c1'
        ret_ds, ret_hd = extract_rows(orig_ds, orig_hd, predicate,
                                      ['a', 'c'])
        test_result = \
            ret_ds is not orig_ds \
            and ret_ds == exp_ds \
            and ret_hd is not orig_hd \
            and ret_hd == exp_hd
        self.assertTrue(test_result)


class Tests_load_csv_dataset_Function(unittest.TestCase):
    """
    Unit tests for the function, `load_csv_dataset`.
    """

    def test_arg_wrong_type(self):
        filename = []
        ret_ds, ret_hd = load_csv_dataset(filename)
        self.assertTrue(ret_ds is None and ret_hd is None)

    def test_arg_is_empty(self):
        filename = ''
        ret_ds, ret_hd = load_csv_dataset(filename)
        self.assertTrue(ret_ds is None and ret_hd is None)

    def test_non_existent_file(self):
        filename = '***NON_EXISTENT_FILE***'
        ret_ds, ret_hd = load_csv_dataset(filename)
        self.assertTrue(ret_ds is None and ret_hd is None)

    def test_load_csv_ok(self):
        orig_hd = ['a', 'b', 'c']
        orig_ds = [
            ['a1', 'b1', 'c1'],
            ['a2', 'b2', 'c2'],
            ['a3', 'b3', 'c3'],
        ]
        csvdata = 'a,b,c\na1,b1,c1\na2,b2,c2\na3,b3,c3\n'
        file = NamedTemporaryFile(mode='w+', delete=False)
        filename = file.name
        _ = file.write(csvdata)
        file.close()
        ret_ds, ret_hd = load_csv_dataset(filename)
        unlink(filename)
        cmpds = all(map(lambda p, q: p is not q and p == q,
                        ret_ds, orig_ds))
        cmphd = all(map(lambda p, q: p == q, ret_hd, orig_hd))
        test_result = \
            ret_ds is not orig_ds \
            and cmpds \
            and ret_hd is not orig_hd \
            and cmphd
        self.assertTrue(test_result)


if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2)
