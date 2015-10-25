#  PYTHONPATH=.:/usr/share/datadog/agent/ python checks.d/pm2.py
import subprocess
import json

from checks import AgentCheck


def load_json(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    out = p.communicate()[0]
    return json.loads(out)[0]


class Pm2(AgentCheck):

    def check(self, instance):
        try:
            json_data = load_json(instance['command'].split(' '))
        except (ValueError, IndexError):
            return
        # cpu, memory, errors, processes, restart, online, status
        self.gauge('pm2.processes.cpu', json_data['monit']['cpu'])
        self.gauge('pm2.processes.memory', json_data['monit']['memory'])
        self.gauge('pm2.processes.status', json_data['pm2_env']['status'])
        self.gauge('pm2.processes.uptime', json_data['pm2_env']['pm_uptime'])


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
