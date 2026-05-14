#!/usr/bin/python

from pyvis.network import Network
import os
import sys
import xml.etree.ElementTree as ET

tree = ET.parse(sys.argv[1])
root = tree.getroot()
net = Network(bgcolor='#343a40', font_color='#FFFFFF', height='1000px')

def get_hosts(root):
    hosts_arr = []
    try:
        for host in root.findall("host"):
            if(host[0].attrib['state'] == 'up'):
                hosts_arr.append(host)
    except Exception as e:
        print("There was an error in get_hosts", e)
    return hosts_arr

def set_image(os):

    # TODO: find another way to set the image.
    images_dict = {"Windows":"./ngf_icons/Windows.png",
                    "Linux":"./ngf_icons/Linux.png",
                    "FreeBSD":"./ngf_icons/FreeBSD.png",
                    "Cisco":"./ngf_icons/Cisco.png",
                    "Unknown":"./ngf_icons/Unknown.png"}
    try: # I chose to use if else instead of switch case because some people might be using python < 3.10 . might change later...
        if(os == None):
            return images_dict["Unknown"]
        elif("Windows" in os):
            return images_dict["Windows"]
        elif("Linux" in os):
            return images_dict["Linux"]
        elif("FreeBSD" in os):
            return images_dict["FreeBSD"]
        elif("Cisco" in os):
            return images_dict["Cisco"]
        else:
            return images_dict["Unknown"]
    except Exception as e:
        print("There was an error in set_image", e)


def get_info(host):
    try:
        ip = host.find("address").attrib["addr"]
        os = host.find("os").find("osmatch").get("name") if host.find("os").find("osmatch") is not None else None # basically get the name attribute if there is a tag, else None.
        hostname = host.find("hostnames").find("hostname").get("name") if host.find("hostnames").find("hostname") is not None else ip
        host_info = dict(ip = ip, os = os, hostname = hostname, ports = [])
        
        for port in host.find("ports").iter("port"):
            proto = port.attrib["protocol"]
            portid = port.attrib["portid"]
            state = port.find("state").attrib["state"]
            service = port.find("service").attrib["name"]
            product = port.find("service").get("product") if port.find("service").get("product") is not None else None
            version = port.find("service").get("version") if port.find("service").get("version") is not None else None
            scripts_arr = []
            
            if port.find("script") is not None:
                for script in port.findall("script"):
                    s_dict = dict(id = script.attrib["id"], output = script.attrib["output"])
                    scripts_arr.append(s_dict)
            port_info = dict(proto = proto, portid = portid, state = state, service = service, product = product, version = version, scripts_arr = scripts_arr)
            host_info["ports"].append(port_info)

    except Exception as e:
        print("There was an error in get_info: ", e, host.find("address").attrib["addr"])
    return host_info


def create_network(hosts_arr):
    try:
        for host in hosts_arr:
            host_info = get_info(host)
            os = host_info["os"]
            image = set_image(os)
            ip = host_info["ip"]
            title = host_info["hostname"]
            net.add_node(ip, label=title + f" [{len(host_info["ports"])}]", shape='image', image=image,host_info = host_info)
    except Exception as e:
        print("There was an error in create_network", e)



def main():
    hosts_arr = get_hosts(root)
    create_network(hosts_arr)
    net.set_options("""
options = 
{
  "nodes": {
    "shape": "dot",
    "size": 30,
    "font": {
      "size": 14
    }
  },

  "edges": {
    "smooth": false,
    "color": {
      "inherit": true
    }
  },

  "physics": {
    "enabled": true,

    "solver": "barnesHut",

    "barnesHut": {
      "gravitationalConstant": -2500,
      "centralGravity": 0.2,
      "springLength": 230,
      "springConstant": 0.04,
      "damping": 0.25,
      "avoidOverlap": 1
    },

    "stabilization": {
      "enabled": true,
      "iterations": 2000,
      "updateInterval": 50,
      "fit": true
    },

    "minVelocity": 0.1
  }
}
""")
    # net.show_buttons()
    # net.set_template("./settings.html")
    net.set_template("./template.html")
    net.save_graph(name='index.html')

if __name__ == '__main__':
    main()
