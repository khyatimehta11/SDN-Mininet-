# creating FIREWALL


#importing header files
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr, IPAddr6, EthAddr
import pox.lib.packet as pkt

log = core.getLogger()

#statically allocate a routing table for hosts(Ip address and mac address)
#MACs used in  topob.py file
dict = {
  "h1" : ("10.0.1.10", '00:00:00:00:00:01'),
  "h2" : ("10.0.2.20", '00:00:00:00:00:02'),
  "h3" : ("10.0.3.30", '00:00:00:00:00:03'),
  "server" : ("10.0.4.10", '00:00:00:00:00:04'),
  "h4" : ("10.0.2.10", '00:00:00:00:00:05'),
}

class q2Controller (object):
  """
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    print (connection.dpid)

  # Keep track of the connection to the switch so that we can


    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

    #use the dpid to figure out what switch is being created
    if (connection.dpid == 12): # core12 is core switch in which rules are pushed so this condition will check whether switch is core switch or not with the help of dp_id Core 
      self.cs12_setup()

    # mac_to_port is used  to keep track of which ethernet address asn switch port matching here dictionary is used 
    #  (keys are MACs, values are ports).


    self.mac_to_port = {}

  #As core switch is responsible for transfering traffic between different subnets so flow rule is added in core switch
  def cs12_setup(self):

    self._act_as_router() #this method will let the  traffic  flow between different subnet

  # this method is call by core switch which allow IP traffic as normal here in every iteration port number and host is updated and flow rule is added as every time nw_dst and port is changing
  def _act_as_router(self):
    host = {10: (dict['h1'][0], 1),
            20: (dict['h2'][0], 2),
            30: (dict['h3'][0], 3),
            40: (dict['server'][0], 4),
            50: (dict['h4'][0], 5)}

    for i in range(len(host)):
      h = host[(i+1)*10][0] # it will check values of indexhost[n][0] from above and above table will check value from routing table of host
      p = host[(i+1)*10][1] # it will check values of indexhost[n][1] from above and above table will check value from routing table of host
     # self.connection.send(of.ofp_flow_mod(action=of.ofp_action_output(port=p),
                                          # priority=5,
                                          # match=of.ofp_match(dl_type=0x800,
                                                             # nw_dst=h))) #in every iteration port number and destination ip address will change and ip matching rules is applied that led the connectivity between different subnets 

      if h == '10.0.2.10':

        self.connection.send(of.ofp_flow_mod(action=of.ofp_action_output(port=of.OFPP_FLOOD),
                                             priority=5,
                                             match=of.ofp_match(dl_type=0x800,
                                                                nw_src=h)))  #iptraffic allowed for h4 whose ip address is 10.0.2.10 
      else:
        self.connection.send(of.ofp_flow_mod(priority=1,
                                             match=of.ofp_match(nw_src=h)))  #ip traffic blocked for others

      self.connection.send(of.ofp_flow_mod(action=of.ofp_action_output(port=p),
                                           priority=5,
                                           match=of.ofp_match(dl_type=0x800, nw_proto=1,
                                                              nw_dst=h)))  #icmp allowed
      self.connection.send(of.ofp_flow_mod(action=of.ofp_action_output(port=p),
                                           priority=5,
                                           match=of.ofp_match(dl_type=0x806,
                                                              nw_dst=h))) # arp allowed
  # resend _packet is used to handle individual ARP packets

  def resend_packet(self, packet_in, out_port):
    msg = of.ofp_packet_out()
    msg.data = packet_in
    action = of.ofp_action_output(port = out_port)
    msg.actions.append(action)
    self.connection.send(msg)

# except Core switch all other switch are MAC learning switch so this function will provide mac learning functinality to other switch in network

  def act_like_switch (self, packet, packet_in):
    """
    Implement switch-like behavior.
    """
#check if source that generate packet is not present in mac_port table
    if packet.src not in self.mac_to_port:
        log.debug(f"Learned {packet.src} from port {packet_in.in_port}")
        self.mac_to_port[packet.src] = packet_in.in_port

#check if source that generate packet is present in mac_port table then add the flows so that it will send packets to destination
    if packet.dst in self.mac_to_port:
        log.debug("Installing Flows...")
        self.resend_packet(packet_in, self.mac_to_port[packet.dst])
        msg = of.ofp_flow_mod()
        msg.match.dl_src = packet.src
        msg.match.dl_dst = packet.dst
        msg.actions.append(of.ofp_action_output(port = self.mac_to_port[packet.dst]))
        if self.connection.dpid != 12: # this condition will not allowed to insert rules to core switch as rules for  core switch is already defiend in act_as_router function above
            self.connection.send(msg)
    else:
        log.debug("Broadcasting...") #  for all other switch packets are flood
        self.resend_packet(packet_in, of.OFPP_ALL)

  def _handle_PacketIn (self, event):
    """
    Packets not handled by the router rules will be
    forwarded to this method to be handled by the controller
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    print('Unhandled packet from '+str(self.connection.dpid)+':'+packet.dump())
    self.act_like_switch(packet, packet_in)  # this will call act_like_switch and mac learning rules are push in other switches
def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    q2Controller(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)


