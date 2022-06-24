# /usr/bin/python
#**************TOPOLOGY *******************

#   H1----------S1------------
# (10.0.1.10\24)                  \
#                                          \
#   H2---------S2---------CORE SWITCH------------S4---------SERVER(10.0.4.10/24)
# (10.0.1.20\24)                    /  |
#                                         /   |
#   H3---------S3-------------    |_____H4(10.0.2.10/24)
# (10.0.1.30\24)



from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import RemoteController

class ques2_topo(Topo):
  def build(self):
    #add switches 
    print( '*** Add switches to topology')
    s1 = self.addSwitch('s1')
    s2 = self.addSwitch('s2')
    s3 = self.addSwitch('s3')
    cs12 = self.addSwitch('cs12')  #core switch 
    s4 = self.addSwitch('s4')

    #add hosts by defining their mac address,ip address and default router
    print( '*** Add hosts to topology')
    h1 = self.addHost('h1',mac='00:00:00:00:00:01',ip='10.0.1.10/24',defaultRoute='h1-eth0')
    h2 = self.addHost('h2',mac='00:00:00:00:00:02',ip='10.0.2.20/24',defaultRoute='h2-eth0')
    h3 = self.addHost('h3',mac='00:00:00:00:00:03',ip='10.0.3.30/24',defaultRoute='h3-eth0')
    h4 = self.addHost('h4',mac='00:00:00:00:00:05',ip='10.0.2.10/24',defaultRoute='h4-eth0')
    server = self.addHost('server',mac='00:00:00:00:00:04',ip='10.0.4.10/24',defaultRoute='server-eth0')


    #add links
    print( '*** Add links to topology')
    self.addLink(h1,s1)  #link between h1 and s1
    self.addLink(h2,s2)  #link between h2 and s2
    self.addLink(h3,s3)  #link between h3 and s3
    self.addLink(s1,cs12)  #link between s1 and core
    self.addLink(s2,cs12)  #link between s2 and core
    self.addLink(s3,cs12)  #link between s3 and core
    self.addLink(server,s4)  #link between server and s4
    self.addLink(cs12,s4)  #link between core and s4
    self.addLink(h4,cs12) #link between h4 and core
    print('*** Post configure switches and hosts\n')

topos = {'ques2' : ques2_topo}

def configure():
  topo = ques2_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  print( '*** Adding controller to topology ' )
  print( '*** Starting network')
  net.start()

  CLI(net)

  net.stop()


if __name__ == '__main__':
  configure()





