import datetime
import shutil
import tempfile
import unittest

from apel.db.apeldb import ApelDbException
from apel.db.records import StorageRecord
from apel.db.unloader import DbUnloader, get_start_of_previous_month


class TestDbUnloader(unittest.TestCase):
    '''
    Test case for DbUnloader.
    '''

    def setUp(self):
        # Create temporary directory for dirq to write to
        self.dir_path = tempfile.mkdtemp()
        self.unloader = DbUnloader(None, self.dir_path)

    def tearDown(self):
        shutil.rmtree(self.dir_path)

    def test_write_star_to_apel(self):
        """Check that unloading StAR records to APEL format is prevented."""
        self.assertRaises(ApelDbException, self.unloader._write_messages,
                          StorageRecord, 'table', 'query', ur=False)

    def test_to_int_min1_basic(self):
        self.assertEqual(self.unloader._to_int_min1(5), 5)
        self.assertEqual(self.unloader._to_int_min1(5.5), 5)
        self.assertEqual(self.unloader._to_int_min1("5"), 5)

    def test_to_int_min1_fraction_less_than_one(self):
        self.assertEqual(self.unloader._to_int_min1(0.6), 1)
        self.assertEqual(self.unloader._to_int_min1("0.6"), 1)

    def test_to_int_min1_zero_and_one(self):
        self.assertEqual(self.unloader._to_int_min1(0), 0)
        self.assertEqual(self.unloader._to_int_min1(1), 1)
        self.assertEqual(self.unloader._to_int_min1("1"), 1)

    def test_to_int_min1_invalid_values(self):
        self.assertIsNone(self.unloader._to_int_min1("N/A"))
        self.assertIsNone(self.unloader._to_int_min1(None))
        self.assertIsNone(self.unloader._to_int_min1([]))


class TestFunctions(unittest.TestCase):
    """Test cases for non-class functions."""

    def test_get_start_of_previous_month(self):
        """Check that get_start_of_previous_month gives the correct datetime."""
        dt = datetime.datetime(2012, 1, 1, 1, 1, 1)
        dt2 = datetime.datetime(2011, 12, 1, 0, 0, 0)
        ndt = get_start_of_previous_month(dt)
        self.assertEqual(dt2, ndt)

        dt3 = datetime.datetime(2012, 3, 1, 1, 1, 1)
        dt4 = datetime.datetime(2012, 2, 1, 0, 0, 0)
        ndt = get_start_of_previous_month(dt3)
        self.assertEqual(dt4, ndt)

if __name__ == '__main__':
    unittest.main()
