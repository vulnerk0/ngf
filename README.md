# ngf

<img width="1920" height="998" alt="image" src="https://github.com/user-attachments/assets/3244ed82-a0fe-4b92-8013-79e37e11bab5" />


ngf is a script I made to visualize the output of Nmap. The script is simple, it takes an XML file and parses the hosts and thier information and using pyvis, displays a graph of the hosts with a side bar to view the information.

# Installation

clone the repo
```shell
git clone https://github.com/vulnerk0/ngf.git
```

cd into the repo directory
```shell
cd ngf
```

install the libraries, the only one you need is pyvis
```shell
pip3 install pyvis
```

>[!note]
>DON'T FORGET TO SETUP A VIRTUAL ENVIRONMENT FOR PYTHON
>` python -m venv .venv ; source .venv/bin/activate `

# Usage
run the nmap scan, don't forget to provide the `-oX` flag to output the results to an XML file
```shell
nmap -sS -A -T4 192.168.0.0/8 -oX nmap_scan.xml
```

you can run the script without any arguments
```shell
python ngf.py nmap_scan.xml
```

the script will output an HTML file that you can simply share or view
```shell
firefox nmap_graph.html
```

| TODO        |
| ------------- |
| Fetch the Router / Domain Controller|
| Find a better way to determine the OS|
| Add a host rename functionality|
| Find a better way to set an image for the node|
| Make it possible to run the script from anywhere on the system|

# AI Usage
I wrote the entire script and only used AI to generate the side bar and I then modified it extensively

# Credit
Thanks to my friend [Mohammed Alsafari](https://github.com/Feloxorea) for giving me the idea for the script
