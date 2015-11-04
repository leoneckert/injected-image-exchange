# the follwoing script is taken from the mitmproxy examples on 
#
# https://github.com/mitmproxy/mitmproxy/tree/master/examples
#
# and used for the project with the title:
#
#
#                                       __                __     
#  __              __                  /\ \__            /\ \    
# /\_\     ___    /\_\      __     ___ \ \ ,_\     __    \_\ \   
# \/\ \  /' _ `\  \/\ \   /'__`\  /'___\\ \ \/   /'__`\  /'_` \  
#  \ \ \ /\ \/\ \  \ \ \ /\  __/ /\ \__/ \ \ \_ /\  __/ /\ \L\ \ 
#   \ \_\\ \_\ \_\ _\ \ \\ \____\\ \____\ \ \__\\ \____\\ \___,_\
#    \/_/ \/_/\/_//\ \_\ \\/____/ \/____/  \/__/ \/____/ \/__,_ /
#                 \ \____/                                       
#                  \/___/                                        
                                               
#  __                                            
# /\_\     ___ ___       __        __       __   
# \/\ \  /' __` __`\   /'__`\    /'_ `\   /'__`\ 
#  \ \ \ /\ \/\ \/\ \ /\ \L\.\_ /\ \L\ \ /\  __/ 
#   \ \_\\ \_\ \_\ \_\\ \__/.\_\\ \____ \\ \____\
#    \/_/ \/_/\/_/\/_/ \/__/\/_/ \/___L\ \\/____/
#                                  /\____/       
#                                  \_/__/        
#                       __                                             
#                      /\ \                                            
#    __   __  _    ___ \ \ \___       __       ___       __       __   
#  /'__`\/\ \/'\  /'___\\ \  _ `\   /'__`\   /' _ `\   /'_ `\   /'__`\ 
# /\  __/\/>  </ /\ \__/ \ \ \ \ \ /\ \L\.\_ /\ \/\ \ /\ \L\ \ /\  __/ 
# \ \____\/\_/\_\\ \____\ \ \_\ \_\\ \__/.\_\\ \_\ \_\\ \____ \\ \____\
#  \/____/\//\/_/ \/____/  \/_/\/_/ \/__/\/_/ \/_/\/_/ \/___L\ \\/____/
#                                                        /\____/       
#                                                        \_/__/        
#
#
# a project by Leon Eckert and Joakim Quach
#
# as part of Adam Harvey's Stratosphere of Surveillance class at ITP, NYU
#
# builds on the amazing mitmproxy: https://github.com/mitmproxy/mitmproxy
#
# Fall 2015
#

# what this script does
# the follwoing script is needed to redirect the admin computer to a page that displays the 
# list of image urls that are in the dicionairy at any time.


from libmproxy.protocol.http import HTTPResponse
from netlib.odict import ODictCaseless

"""
This example shows two ways to redirect flows to other destinations.
"""


def request(context, flow):
    # pretty_host(hostheader=True) takes the Host: header of the request into account,
    # which is useful in transparent mode where we usually only have the IP
    # otherwise.

    # Method 1: Answer with a locally generated response
    if flow.request.pretty_host(hostheader=True).endswith("openwifi.com"):
        reader = open('data.txt','r')
        links = reader.read()
        reader.close()
        resp = HTTPResponse(
            [1, 1], 200, "OK",
            ODictCaseless([["Content-Type", "text/html"]]),
            links)
        flow.reply(resp)

    # Method 2: Redirect the request to a different server
    if flow.request.pretty_host(hostheader=True).endswith("example.org"):
        flow.request.host = "mitmproxy.org"
        flow.request.update_host_header()
