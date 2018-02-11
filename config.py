from ConfigParser import ConfigParser
from os.path import expanduser

parser = ConfigParser()
parser.read('~/.aws/config')


class Config(object):
    def __init__(self):
        super(Config, self).__init__()
        self.parser = ConfigParser()
        home = expanduser("~")
        self.parser.read('{}/.aws/config'.format(home))

    @property
    def profiles(self):
        for section in self.parser.sections():
            if 'profile' in section:
                yield section.split(' ')[1]

    def get_arn(self, profile):
        return AWSArn(self.parser.get('profile {}'.format(profile), 'role_arn'))


class AWSArn(object):
    def __init__(self, arn):
        super(AWSArn, self).__init__()
        # arn:partition:service:region:account-id:resourcetype/resource
        split = arn.split(':')
        self.partition = split[1]
        self.service = split[2]
        self.region = split[3]
        self.account_id = split[4]
        self.resource_type = split[5]
        self.resource = self.resource_type.split('/')[-1]

        # Ignore if there is no actual role set
        if self.resource == 'role':
            self.resource = None
