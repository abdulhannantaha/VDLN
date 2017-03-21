import argparse
import requests
import sys
from IPy import IP
import dicttoxml
import yaml


class Api(object):
    """Blue Print of API call"""
    end_point = None

    def __init__(self, resources=None):
        self.resources = resources

    def get_url(self):
        urls = []
        for resource in self.resources:
            urls.append(self.end_point.format(resource))
        return urls

    def download_data(self):
        responses = []
        for url in self.get_url():
            try:
                r = requests.get(url)
            except Exception as e:
                print("Something is going wrong: %s" % e)
            else:
                if r.status_code == 200:
                    responses.append(r.json())
                else:
                    print("API %s call error.\n Status code%s \nMessage:%s" % (url, r.status_code, r.content))
        return responses

    def get_response(self, format="json"):
        data = self.download_data()
        if format == 'json':
            return data
        if format == 'xml':
            xmls = []
            for d in data:
                xmls.append(dicttoxml.dicttoxml(d))
            return xmls
        if format == "yaml":
            yamls = []
            for d in data:
                yamls.append(yaml.dump(d))
            return yamls
        assert False, "Unknown Data type"


class GeoLoc(Api):
    end_point = "https://stat.ripe.net/data/geoloc/data.json?resource={0}&meta=availability"


class NetworkInfo(Api):
    end_point = "https://stat.ripe.net/data/network-info/data.json?resource={0}"


class AsOverview(Api):
    end_point = "https://stat.ripe.net/data/as-overview/data.json?resource=AS{0}"


actions = {
    'network-info': NetworkInfo,
    'geoloc': GeoLoc,
    'as-overview': AsOverview
}

formats = ['json', 'yaml', 'xml']


def validate_input(args):
    return False


class MyParser(argparse.ArgumentParser):
    def validate_input(self, args):
        if args.action.lower() not in actions:
            raise SystemExit("Action is invalid it should be from %s" % list(actions.keys()))

        if args.format.lower() not in formats:
            raise SystemExit("Format is invalid it should be from %s" % list(formats))

        if len(args.ip) == 0 and len(args.asn) == 0:
            raise SystemExit("Either you should use --ip or --asn")

        action = args.action.lower()
        if action in ['network-info', ] and (len(args.ip) == 0 or len(args.asn) != 0):
            if len(args.asn) != 0:
                raise SystemExit("To use %s you should use ip address not asn" % action)
            raise SystemExit("To use %s you should pass at least one ip address" % action)

        if action in ['as-overview', ] and (len(args.asn) == 0 or len(args.ip) != 0):
            if len(args.ip) != 0:
                raise SystemExit("To use %s you should use asn instead of ip address" % action)
            raise SystemExit("To use %s you should pass at least one asn" % action)

    def parse_args(self, args=None, namespace=None):
        args = super(MyParser, self).parse_args(args=args, namespace=namespace)
        self.validate_input(args)
        return args


def create_parser():
    parser = MyParser(description='Network Coding Exercise.')
    parser.add_argument('--ip', metavar='ipAddr', type=IP, nargs='+', default=[],
                        help='One or More ip address for query')
    parser.add_argument('--action', action="store",
                        default='network-info',
                        help='Actions(default:network-info)')
    parser.add_argument('--format', action="store",
                        default='json',
                        help='Output Format(default:json)')
    parser.add_argument("--asn", metavar="BGP ASN", default=[], type=int, nargs='+', help="BGP ASN")
    return parser


def main(args=None):
    if args is None:
        parser = create_parser()
        args = parser.parse_args()
    action = args.action.lower()
    format = args.format.lower()
    args.ip.extend(args.asn)
    api = actions.get(action)(resources=args.ip)
    data = api.get_response(format=format)
    args.ip.clear()
    return data
if __name__ == '__main__':
    print(main())
