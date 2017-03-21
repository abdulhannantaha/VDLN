from unittest import TestCase
from network_config import create_parser, main


class CommandLineTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        parser = create_parser()
        cls.parser = parser


class PingTestCase(CommandLineTestCase):
    def test_args(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])

        with self.assertRaises(SystemExit):
            self.parser.parse_args(['--format', 'xyz', '--ip', "1.2.3", "1.3.4"])

        with self.assertRaises(SystemExit):
            self.parser.parse_args(['--action', 'xyz', '--ip', "1.2.3", "1.3.4"])

        with self.assertRaises(SystemExit):
            self.parser.parse_args(
                ['--format', 'json', '--ip', "1.2.3", "1.3.4", '--action',
                 'network-info', '--asn', "1", "2", "3"])

        with self.assertRaises(SystemExit):
            self.parser.parse_args(['--ip', "267.267.234.234", "1.1"])

        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--asn", "a", "a3", "--action", 'as-overview'])

    def as_overview(self, format="json"):
        args = self.parser.parse_args(['--asn', '3333', '--action', 'as-overview', '--format', format])
        result = main(args=args)
        self.assertIsNotNone(result)

    def test_as_overview(self):
        self.as_overview("json")

    def test_as_overview_xml(self):
        self.as_overview("XML")

    def test_as_overview_yaml(self):
        self.as_overview("YAML")

    def network_info(self, format="json"):
        args = self.parser.parse_args(['--ip', '140.78.90.50', '--action', 'network-info', '--format', format])
        result = main(args=args)
        self.assertIsNotNone(result)

    def test_network_info(self):
        self.network_info()

    def test_network_info_xml(self):
        self.network_info(format="XML")

    def test_network_info_yaml(self):
        self.network_info("YAML")

    def geoloc(self, format="json"):
        args = self.parser.parse_args(['--ip', '140.78.90.50', '--action', 'geoloc', '--format', format])
        result = main(args=args)
        self.assertIsNotNone(result)

        args = self.parser.parse_args(['--asn', '3333', '--action', 'geoloc', '--format', format])
        result = main(args=args)
        self.assertIsNotNone(result)

    def test_geoloc(self):
        self.geoloc()

    def test_geoloc_xml(self):
        self.geoloc(format="XML")

    def test_geoloc_yaml(self):
        self.network_info("YAML")
