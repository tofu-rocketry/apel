import unittest

from apel.db.records import AcceleratorSummary


class AcceleratorSummaryRecordTest(unittest.TestCase):
    """Test case for AcceleratorSummary."""

    def setUp(self):
        self._msg1 = '''
                Month: 12
                Year: 2021
                AssociatedRecordType: cloud
                GlobalUserName: /C=UK/O=eScience/OU=CLRC/L=RAL/CN=apel-consumer2.esc.rl.ac.uk/emailAddress=sct-certificates@stfc.ac.uk
                SiteName: Site Navigation
                Count: 604800.000
                Cores: 857
                AvailableDuration: 326057
                ActiveDuration: 30739
                BenchmarkType: Site FAQs
                Benchmark: 326.000
                Model: HS About
                Type: GPU
                NumberOfRecords: 1000
                '''

        self._values1 = {
                'Month': 12,
                'Year': 2021,
                'AssociatedRecordType': 'cloud',
                'GlobalUserName': '/C=UK/O=eScience/OU=CLRC/L=RAL/CN=apel-consumer2.esc.rl.ac.uk/emailAddress=sct-certificates@stfc.ac.uk',
                'SiteName': 'Site Navigation',
                'Count': 604800.000,
                'Cores': 857,
                'AvailableDuration': 326057,
                'ActiveDuration': 30739,
                'BenchmarkType': 'Site FAQs',
                'Benchmark': 326.000,
                'Model': 'HS About',
                'Type': 'GPU',
                'NumberOfRecords': 1000,
        }

        self.cases = {}
        self.cases[self._msg1] = self._values1

    def test_load_from_msg(self):
        """Check that loading from a message works correctly."""
        for msg, values in self.cases.items():

            accelerator = AcceleratorSummary()
            accelerator.load_from_msg(msg)

            cont = accelerator._record_content

            for field, value in values.items():
                self.assertEqual(cont[field], value, "%s != %s for key %s" % (cont[field], value, field))

    def test_mandatory_fields(self):
        """Check that the set_field method works for mandatory fields."""
        record = AcceleratorSummary()
        record.set_field("Month", '01')
        record.set_field("Year", '2021')
        record.set_field("AssociatedRecordType", 'cloud')
        record.set_field('SiteName', 'MySite')
        record.set_field("Count", 100.01)
        record.set_field("AvailableDuration", 1000)
        record.set_field("Type", 'GPU')
        record.set_field("NumberOfRecords", 10)

        try:
            record._check_fields()
        except Exception as e:
            self.fail('_check_fields method failed: %s [%s]' % (e, type(e)))


if __name__ == '__main__':
    unittest.main()
