#  PYTHONPATH=.:/usr/share/datadog/agent/ python checks.d/pm2.py
import subprocess
import json
import time

from checks import AgentCheck


def load_json(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    out = p.communicate()[0]
    return json.loads(out)


class Pm2(AgentCheck):

    def check(self, instance):
        totals = {'cpu': 0, 'memory': 0}
        for instance in load_json(instance['command'].split(' ')):
            node_app_instance = instance['pm2_env']['NODE_APP_INSTANCE']
            # cpu, memory, errors, processes, restart, online, status
            self.gauge(
                'pm2.processes.n{}_cpu'.format(node_app_instance),
                instance['monit']['cpu'])
            totals['cpu'] += instance['monit']['cpu']
            self.gauge(
                'pm2.processes.n{}_memory'.format(node_app_instance),
                instance['monit']['memory'])
            totals['memory'] += instance['monit']['memory']
            self.gauge(
                'pm2.processes.n{}_status'.format(node_app_instance),
                instance['pm2_env']['status'])
            self.gauge(
                'pm2.processes.n{}_uptime'.format(node_app_instance),
                int(time.time()) - int(instance['pm2_env']['pm_uptime']))

        self.gauge('pm2.processes.total_cpu', totals['cpu'])
        self.gauge('pm2.processes.total_memory', totals['memory'])


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
