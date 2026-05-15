#!/usr/bin/python

from pyvis.network import Network
import os
import sys
import xml.etree.ElementTree as ET
import concurrent.futures

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
    # Instead of using the github API which has rate limiting, I found out that githubusercontent doesn't have any rate limiting and no auth is needed...
    try:
        supported_OSs = ["Linux", "Microsoft", "Cisco", "FreeBSD", "Apple"]
        
        if os is not None:
            os = os.split(' ')[0]
        else:
            os = "Unknown"
        
        image_url = f"https://raw.githubusercontent.com/vulnerk0/ngf_icons/refs/heads/main/{os}.png"
        if os in supported_OSs:
            return image_url
        else:
            return "https://raw.githubusercontent.com/vulnerk0/ngf_icons/refs/heads/main/Unknown.png"
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


def add_node(host):
    try:
        host_info = get_info(host)
        os = host_info["os"]
        image = set_image(os)
        ip = host_info["ip"]
        title = host_info["hostname"]
        net.add_node(ip, label=title + f" [{len(host_info["ports"])}]", shape='image', image=image,host_info = host_info)
    except Exception as e:
        print("There was an error in add_node", e)



def main():
    hosts_arr = get_hosts(root)
    with concurrent.futures.ThreadPoolExecutor() as executer:
        for host in hosts_arr:
            executer.submit(add_node, host)
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
    net.set_template("./template.html")
    net.save_graph(name='nmap_graph.html')

if __name__ == '__main__':
    main()
