from mininet.topo import Topo
from mininet.net import Containernet
from mininet.node import Node, Controller, OVSKernelSwitch
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mininet.cli import CLI
import time
import os
setLogLevel('info')

class LinuxRouter( Node ):
    "A node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )
    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()

info('***Starting Container\n')
net = Containernet(controller=Controller, link= TCLink, switch=OVSKernelSwitch)

defaultIP1 = '10.0.3.10/24'# IPaddress for r1-eth0
defaultIP2 = '10.0.3.20/24'# IPaddress for r2-eth0
defaultIP3 = '10.0.4.30/24'# IPaddress for r3-eth0
defaultIP4 = '10.0.5.40/24'# IPaddress for r4-eth0
defaultIP5 = '10.0.6.40/24'
defaultIP6 = '10.0.7.40/24'
defaultIP7 = '10.0.9.40/24'
defaultIP8 = '10.0.11.40/24'
defaultIP9 = '10.0.13.40/24'
defaultIP10 = '10.0.15.40/24'
info('***Adding Routers\n')
router1 = net.addHost( 'r1', cls=LinuxRouter, ip=defaultIP1 )
router2 = net.addHost( 'r2', cls=LinuxRouter, ip=defaultIP2 )
router3 = net.addHost( 'r3', cls=LinuxRouter, ip=defaultIP3 )
router4 = net.addHost( 'r4', cls=LinuxRouter, ip=defaultIP4 )
router5 = net.addHost( 'r5', cls=LinuxRouter, ip=defaultIP5 )
router6 = net.addHost( 'r6', cls=LinuxRouter, ip=defaultIP6 )
router7 = net.addHost( 'r7', cls=LinuxRouter, ip=defaultIP7 )
router8 = net.addHost( 'r8', cls=LinuxRouter, ip=defaultIP8 )
router9 = net.addHost( 'r9', cls=LinuxRouter, ip=defaultIP9 )
router10 = net.addHost( 'r10', cls=LinuxRouter, ip=defaultIP10 )

info('***Adding Switches\n')
switch1 = net.addSwitch( 's1', dpid='1000000000000001')
switch2 = net.addSwitch( 's2', dpid='1000000000000002')
switch3 = net.addSwitch( 's3', dpid='1000000000000003')
switch4 = net.addSwitch( 's4', dpid='1000000000000004')
switch5 = net.addSwitch( 's5', dpid='1000000000000005')

info('***Adding hosts\n')
host1 = net.addDocker('h1', ip='10.0.1.30/24', defaultRoute='via 10.0.1.10', dimage="linphone") #define gateway
host2 = net.addDocker('h2', ip='10.0.1.20/24', defaultRoute='via 10.0.1.10', dimage="linphone")
host3 = net.addDocker('h3', ip='10.0.18.15/24', defaultRoute='via 10.0.18.40', dimage="linphone")
host4 = net.addDocker('h4', ip='10.0.18.20/24', defaultRoute='via 10.0.18.40', dimage="linphone")

docker1 = net.addDocker('d1', ip='10.0.2.30/24', defaultRoute='via 10.0.2.20', dimage="voip")
docker2 = net.addDocker('d2', ip='10.0.2.10/24', defaultRoute='via 10.0.2.20', dimage="voip")

#Adding edge network
edge1 = net.addDocker('e1', ip='10.0.19.30/24', defaultRoute='via 10.0.19.20', dimage="ubuntu:trusty")
edge2 = net.addDocker('e2', ip='10.0.20.30/24', defaultRoute='via 10.0.20.20', dimage="ubuntu:trusty")

info('***Adding links\n')
net.addLink( router1, router2, intfName1='r1-eth0', intfName2='r2-eth0')
net.addLink( router2, router6, intfName1='r2-eth2', intfName2='r6-eth1', params1={'ip':'10.0.8.10/24'}, params2={'ip':'10.0.8.40/24'})
net.addLink( router6, router10, intfName1='r6-eth2', intfName2='r10-eth0', params1={'ip':'10.0.15.10/24'}, params2={'ip':'10.0.15.40/24'})
net.addLink( router7, router10, intfName1='r7-eth2', intfName2='r10-eth1', params1={'ip':'10.0.16.10/24'}, params2={'ip':'10.0.16.40/24'})
net.addLink( router3, router7, intfName1='r3-eth2', intfName2='r7-eth1', params1={'ip':'10.0.10.10/24'}, params2={'ip':'10.0.10.40/24'})
net.addLink( router2, router3, intfName1='r2-eth1', intfName2='r3-eth0', params1={'ip':'10.0.4.10/24'}, params2={'ip':'10.0.4.30/24'})
net.addLink( router3, router4, intfName1='r3-eth1', intfName2='r4-eth0', params1={'ip':'10.0.5.10/24'}, params2={'ip':'10.0.5.40/24'})
net.addLink( router4, router8, intfName1='r4-eth2', intfName2='r8-eth1', params1={'ip':'10.0.12.10/24'}, params2={'ip':'10.0.12.40/24'})
net.addLink( router5, router9, intfName1='r5-eth2', intfName2='r9-eth1', params1={'ip':'10.0.14.10/24'}, params2={'ip':'10.0.14.40/24'})
net.addLink( router4, router5, intfName1='r4-eth1', intfName2='r5-eth0', params1={'ip':'10.0.6.10/24'}, params2={'ip':'10.0.6.40/24'})
net.addLink( router3, router8, intfName1='r3-eth3', intfName2='r8-eth0', params1={'ip':'10.0.11.10/24'}, params2={'ip':'10.0.11.40/24'})
net.addLink( router1, router6, intfName1='r1-eth2', intfName2='r6-eth0', params1={'ip':'10.0.7.10/24'}, params2={'ip':'10.0.7.40/24'})
net.addLink( router2, router7, intfName1='r2-eth3', intfName2='r7-eth0', params1={'ip':'10.0.9.10/24'}, params2={'ip':'10.0.9.40/24'})
net.addLink( router4, router9, intfName1='r4-eth3', intfName2='r9-eth0', params1={'ip':'10.0.13.10/24'}, params2={'ip':'10.0.13.40/24'})
net.addLink( switch1, router1, intfName2='r1-eth1', params2={'ip':'10.0.1.10/24'})
net.addLink( switch4, router1, intfName2='r1-eth3', params2={'ip':'10.0.19.20/24'})
net.addLink( switch5, router10, intfName2='r10-eth3', params2={'ip':'10.0.20.20/24'})
net.addLink( host1, switch1)
net.addLink( host2, switch1)
net.addLink( host3, switch3)
net.addLink( host4, switch3)
net.addLink( edge1, switch4)
net.addLink( edge2, switch5)
net.addLink( switch2, router5, intfName2='r5-eth1', params2={'ip':'10.0.2.20/24'})
net.addLink( switch3, router10, intfName2='r10-eth2', params2={'ip':'10.0.18.40/24'})
net.addLink( switch2, docker1)
net.addLink( switch2, docker2)


net.start()
info('*** Configuring OpenvSwitch:\n')
s1=net.getNodeByName('s1')
s2=net.getNodeByName('s2')
s3=net.getNodeByName('s3')
s4=net.getNodeByName('s4')
s5=net.getNodeByName('s5')

info( '*** Routing Table on Router:\n' )

r1=net.getNodeByName('r1')
r2=net.getNodeByName('r2')
r3=net.getNodeByName('r3')
r4=net.getNodeByName('r4')
r5=net.getNodeByName('r5')
r6=net.getNodeByName('r6')
r7=net.getNodeByName('r7')
r8=net.getNodeByName('r8')
r9=net.getNodeByName('r9')
r10=net.getNodeByName('r10')

#Assigning mac address to routers 

r1.cmd("ifconfig r1-eth1 hw ether 00:00:00:00:01:01")
r5.cmd("ifconfig r5-eth1 hw ether 00:00:00:00:01:02")
r10.cmd("ifconfig r10-eth2 hw ether 00:00:00:00:01:03")


info('***starting OpenVSwitch:\n')
#Adding filter on S1
s1.cmd("ovs-ofctl add-flow s1 nw_proto=1,actions=flood")
s1.cmd("ovs-ofctl add-flow s1 priority=65535,ip,dl_dst=00:00:00:00:01:01 actions=output:1")
s1.cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_dst=10.0.1.30,actions=output:2")
s1.cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_dst=10.0.1.20,actions=output:3")
#Adding filter on s2
s2.cmd("ovs-ofctl add-flow s2 nw_proto=1,actions=flood")
s2.cmd("ovs-ofctl add-flow s2 priority=65535,ip,dl_dst=00:00:00:00:01:02 actions=output:1")
s2.cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_dst=10.0.2.30,actions=output:2")
s2.cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_dst=10.0.2.10,actions=output:3")
#Adding filter on s3
s3.cmd("ovs-ofctl add-flow s3 nw_proto=1,actions=flood")
s3.cmd("ovs-ofctl add-flow s3 priority=65535,ip,dl_dst=00:00:00:00:01:03 actions=output:1")
s3.cmd("ovs-ofctl add-flow s3 priority=10,ip,nw_dst=10.0.18.15,actions=output:2")
s3.cmd("ovs-ofctl add-flow s3 priority=10,ip,nw_dst=10.0.18.20,actions=output:3")
s4.cmd("ovs-ofctl add-flow s4 nw_proto=1,actions=flood")
s5.cmd("ovs-ofctl add-flow s5 nw_proto=1,actions=flood")

info('***Configuring GRE Tunneling\n')

r1.cmd("ip tun a gre1 mode gre local 10.0.3.10 remote 10.0.15.40")
r1.cmd("ip addr a 10.0.0.1 dev gre1")
r1.cmd("ip link set gre1 up")
r1.cmd("ip rou a 10.0.0.0/24 dev gre1")
r10.cmd("ip tun a gre1 mode gre local 10.0.15.40 remote 10.0.3.10")
r10.cmd("ip addr a 10.0.0.2 dev gre1")
r10.cmd("ip link set gre1 up")
r10.cmd("ip rou a 10.0.0.0/24 dev gre1")

info('***Configuring MPLS:\n')
r1.cmd("sysctl -w net.ipv4.conf.all.rp_filter=2")
r1.cmd("sysctl -w net.mpls.platform_labels=65535")
r1.cmd("sysctl -w net.mpls.conf.gre1.input=1")
r1.cmd("ip rou c 10.0.0.1/24 encap mpls 100 dev gre1")
r1.cmd("ip -f mpls rou a 101 dev r1-eth0")

r10.cmd("sysctl -w net.ipv4.conf.all.rp_filter=2")
r10.cmd("sysctl -w net.mpls.platform_labels=65535")
r10.cmd("sysctl -w net.mpls.conf.gre1.input=1")
r10.cmd("ip rou c 10.0.0.2/24 encap mpls 101 dev gre1")
r10.cmd("ip -f mpls rou a 100 dev r10-eth0")


info('starting zebra and ospfd service:\n')

r1.cmd('zebra -f /usr/local/etc/r1zebra.conf -d -z ~/Desktop/r1zebra.api -i ~/Desktop/r1zebra.interface')
time.sleep(1) 
r2.cmd('zebra -f /usr/local/etc/r2zebra.conf -d -z ~/Desktop/r2zebra.api -i ~/Desktop/r2zebra.interface')
r3.cmd('zebra -f /usr/local/etc/r3zebra.conf -d -z ~/Desktop/r3zebra.api -i ~/Desktop/r3zebra.interface')
r4.cmd('zebra -f /usr/local/etc/r4zebra.conf -d -z ~/Desktop/r4zebra.api -i ~/Desktop/r4zebra.interface')
r5.cmd('zebra -f /usr/local/etc/r5zebra.conf -d -z ~/Desktop/r5zebra.api -i ~/Desktop/r5zebra.interface')
r6.cmd('zebra -f /usr/local/etc/r6zebra.conf -d -z ~/Desktop/r6zebra.api -i ~/Desktop/r6zebra.interface')
r7.cmd('zebra -f /usr/local/etc/r7zebra.conf -d -z ~/Desktop/r7zebra.api -i ~/Desktop/r7zebra.interface')
r8.cmd('zebra -f /usr/local/etc/r8zebra.conf -d -z ~/Desktop/r8zebra.api -i ~/Desktop/r8zebra.interface')
r9.cmd('zebra -f /usr/local/etc/r9zebra.conf -d -z ~/Desktop/r9zebra.api -i ~/Desktop/r9zebra.interface')
r10.cmd('zebra -f /usr/local/etc/r10zebra.conf -d -z ~/Desktop/r10zebra.api -i ~/Desktop/r10zebra.interface')
r1.cmd('ospfd -f /usr/local/etc/r1ospfd.conf -d -z ~/Desktop/r1zebra.api -i ~/Desktop/r1ospfd.interface')

r2.cmd('ospfd -f /usr/local/etc/r2ospfd.conf -d -z ~/Desktop/r2zebra.api -i ~/Desktop/r2ospfd.interface')
r3.cmd('ospfd -f /usr/local/etc/r3ospfd.conf -d -z ~/Desktop/r3zebra.api -i ~/Desktop/r3ospfd.interface')
r4.cmd('ospfd -f /usr/local/etc/r4ospfd.conf -d -z ~/Desktop/r4zebra.api -i ~/Desktop/r4ospfd.interface')
r5.cmd('ospfd -f /usr/local/etc/r5ospfd.conf -d -z ~/Desktop/r5zebra.api -i ~/Desktop/r5ospfd.interface')
r6.cmd('ospfd -f /usr/local/etc/r6ospfd.conf -d -z ~/Desktop/r6zebra.api -i ~/Desktop/r6ospfd.interface')
r7.cmd('ospfd -f /usr/local/etc/r7ospfd.conf -d -z ~/Desktop/r7zebra.api -i ~/Desktop/r7ospfd.interface')
r8.cmd('ospfd -f /usr/local/etc/r8ospfd.conf -d -z ~/Desktop/r8zebra.api -i ~/Desktop/r8ospfd.interface')
r9.cmd('ospfd -f /usr/local/etc/r9ospfd.conf -d -z ~/Desktop/r9zebra.api -i ~/Desktop/r9ospfd.interface')
r10.cmd('ospfd -f /usr/local/etc/r10ospfd.conf -d -z ~/Desktop/r10zebra.api -i ~/Desktop/r10ospfd.interface')

info('***Testing Connectivity\n')
net.ping([docker1, docker2])
info('***Running CLI\n')
CLI( net )
info('***Stopping Container\n')
net.stop()
os.system("killall -9 ospfd zebra")
os.system("rm -f /usr/local/etc/*api*")
os.system("rm -f /usr/local/etc/*interface*")
