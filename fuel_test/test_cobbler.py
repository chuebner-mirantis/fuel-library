from devops.helpers import ssh
from base import RecipeTestCase
from root import root
from settings import NODES

__author__ = 'vic'

import unittest

class MyTestCase(RecipeTestCase):
    def test_deploy_nova_rabbitmq(self):
        node01 = self.environment.node[NODES[0]]
        node02 = self.environment.node[NODES[1]]
        self.write_site_pp_manifest(
            root('fuel', 'deployment', 'puppet', 'cobbler', 'examples', 'server_site.pp'),
            cluster = 'true',
            cluster_nodes = [
                "%s" % node01.ip_address_by_network['internal'],
                "%s" % node02.ip_address_by_network['internal']
            ],
        )
        remote = ssh(node01.ip_address, username='root', password='r00tme')
        result1 = remote.sudo.ssh.execute('puppet agent --test')
        remote2 = ssh(node02.ip_address, username='root', password='r00tme')
        result2 = remote2.sudo.ssh.execute('puppet agent --test')
        self.assertResult(result1)
        self.assertResult(result2)


if __name__ == '__main__':
    unittest.main()


    #
    # # HERE IS IPTABLES RULES TO MAKE COBBLER AVAILABLE FROM OUTSIDE
    #      # https://github.com/cobbler/cobbler/wiki/Using%20Cobbler%20Import
    #      # SSH
    #      access_to_cobbler_port { "ssh":        port => '22' }
    #      # DNS
    #      access_to_cobbler_port { "dns_tcp":    port => '53' }
    #      access_to_cobbler_port { "dns_udp":    port => '53',  protocol => 'udp' }
    #      # DHCP
    #      access_to_cobbler_port { "dncp_67":    port => '67',  protocol => 'udp' }
    #      access_to_cobbler_port { "dncp_68":    port => '68',  protocol => 'udp' }
    #      # TFTP
    #      access_to_cobbler_port { "tftp_tcp":   port => '69' }
    #      access_to_cobbler_port { "tftp_udp":   port => '69',  protocol => 'udp' }
    #      # NTP
    #      access_to_cobbler_port { "ntp_udp":    port => '123', protocol => 'udp' }
    #      # HTTP/HTTPS
    #      access_to_cobbler_port { "http":       port => '80' }
    #      access_to_cobbler_port { "https":      port => '443'}
    #      # SYSLOG FOR COBBLER
    #      access_to_cobbler_port { "syslog_tcp": port => '25150'}
    #
    #
    #:80/api/distro/list