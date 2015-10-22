#  PYTHONPATH=.:/usr/share/datadog/agent/ python checks.d/pm2.py

from checks import AgentCheck


def run_command(command):
    pass


class Pm2(AgentCheck):

    def check(self, instance):
        json_data = run_command(instance['command'])
        self.gauge('pm2.processes', json_data[''])


if __name__ == '__main__':
    check, instances = Pm2.from_yaml('conf.d/pm2.yaml')
    for instance in instances:
        print "\nRunning on %s" % instance['command']
        check.check(instance)
        if check.has_events():
            print "Events: %s" % check.get_events()
        print
        for m in check.get_metrics():
            print m
