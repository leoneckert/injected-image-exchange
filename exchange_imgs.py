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
# builds on the amzing mitmproxy: https://github.com/mitmproxy/mitmproxy
#
# Fall 2015
#


import urllib, cStringIO
from PIL import Image
from libmproxy.protocol.http import decoded
import random




#the 'admin' ip address belongs to the computer that is used to display the admin monitor. 
#the admin computer has to be connected to the PI's network and open the "admin-page.html" locally.
admin_ip = "192.168.42.10"

#specify width and height conditions for the images that should be detected
min_img_width = 400
min_img_height = 400

#define the maximum number of photos that are in the dicionairy/image-pool 
#as well as monitored on the admin moitor at any given moment
max_number_imgs = 45


#global dicitonairy to store clients' ip addresses and url to the images they request
victims = {}
#making sure the data.txt (in which current content of dicionairy is saved for admin monitor display) is empty at start
clearData = open('data.txt','w')
clearData.close()


#called at every http request/response
def response(context, flow):
    # finding the image requests and making sure the follwoing script is not running for the admin computer, which present the admin monitor
    if flow.response.headers.get_first("content-type", "").startswith("image") and str(flow.client_conn.address.host) != admin_ip:
        
        #variable to store the client's ip address throughout the script
        victim_host = str(flow.client_conn.address.host)
        
        #now the actual script begins:
        with decoded(flow.response):  # automatically decode gzipped responses.
            
            #try/except to prevent from errors
            try:
                #retrieving the image request
                s = cStringIO.StringIO(flow.response.content)
                #storing the size of the image that has been requested in a variable
                img_size = Image.open(s).size
                #only running the rest of the script if the image is of a minimum targeted resolution
                if(int(img_size[0]) > min_img_width or int(img_size[1]) > min_img_height):
                    
                    #if the client's ip address is not yet in the dicionairy, an entry has to be added
                    if flow.client_conn.address.host not in victims:
                        #add the entry
                        victims[victim_host] = [] 
                   
                    
                    #after adding the entry or, if it already exist do the follwing:
                    #the image url has three components, 'http://' at the start, followed by the host name and the path
                    #these components are retrieved here:
                    url_host = flow.request.headers.get_first("host")
                    url_path = flow.request.path
                    #and combined here to form the full url of the requested image.
                    #while combining, the url is put into the value array of the corresponding client-ip-address
                    #in the dicionairy 
                    victims[victim_host].append("http://" + url_host + url_path)
                    #now we upadte the data.txt file which defines the images that appear on the admin screen
                    #opening appender in 'a' mode let's us append to the file
                    appender = open('data.txt','a')
                    appender.write("http://" + url_host + url_path + " ")
                    appender.close()
                    
                   
                    #next we make sure that there are not more images in the dicitonairy and data file 
                    #than we intent to (this is needed to prevent from data overloads)
                    #we also make sure that, if images have to be deleted, they are taken from the client's
                    #dictionairy entry that currently has the most image urls/image requests in the pool

                    #temporary variable to count the overall images in the pool:
                    number_imgs = 0
                    #for every value (which is itself an array) in the dictionairy...
                    for sites in victims.values():
                        #...we go through every url/element in the array...
                        for site in sites:
                            #...and count the images
                            number_imgs = number_imgs + 1
                    
                    #we then take the final number to check if there are more than we wanted.
                    #that is defined at the beginning of the this script
                    if number_imgs > max_number_imgs:
                        #if there are too many images, 
                        #we want to find out which client 
                        #currently supplies the most
                        #requests to the image pool
                        #temporary variables to store name 
                        #and number of sites of the 'record holding' client
                        record_holder = ""
                        record = 0

                        #looping through every client in the dictionairy...
                        for key in victims:
                            #temp variable to store the number of each client's
                            #img requests 
                            count = 0
                            #...looping through each image url in the value array of the client
                            for sites in victims.get(key):
                                #counting the urls
                                count = count + 1
                            #testing who has the most urls in they value array
                            if int(count) > int(record):
                                #and assign the name of record holder to the variable
                                record_holder = str(key)
                                #and update the record for further loops
                                record = int(count)
                                

                        #when we found the 'record holder' we define his ip adress
                        #as the one out of whiches key value array we delete a random url  
                        to_delete_from = record_holder
                        #shuffle the key value array:
                        random.shuffle(victims.get(to_delete_from))
                        #and take out a value using pop()
                        victims.get(to_delete_from).pop()

                        #lastly we update the data.txt also so the changes we made 
                        #are visible on the admin monitor
                        #opening writer in 'w' mode will delete all content and first...
                        writer = open('data.txt','w')
                        #..and then we iterate through all values for every client
                        #in the dictionairy to write them to the file
                        for sites in victims.values():
                            for site in sites:
                                writer.write(site + " ")
                        #finally we close the writer
                        writer.close()
                
                    

                   

                    #the following part of the script is executed
                    #once there is more than one person coinnected 
                    #to the network/sending image requests
                    if len(victims) > 1:
                        
                        #to find a client's ip adress in the dictionairy,
                        #that is different to the client who is currently 
                        #requesting an image, we first assign the
                        #requesting client to a temporary variable 'random_pick'...
                        random_pick = victim_host
                        #...and then run a while loop, picking random keys from
                        #the dictionair until we found a exchange partner
                        while str(random_pick) ==  str(victim_host):
                            random_pick = random.choice(victims.keys())

                        #we make sure the exchange partner has url in this value array in the dicitonairy
                        #we could improve that part of the script to make sure keys with empty values 
                        #get deleted
                        if len(victims.get(random_pick)) > 0:
                            #and if he does, we shuffle the urls...
                            random.shuffle(victims.get(random_pick))
                            #...in order to pick a random one to return to the requesting client
                            #and take it out of the array value afterwards using pop()
                            replace_img = victims.get(random_pick).pop()

                            #number_imgs = 0    #TBC not needed

                            #next we update the data.txt file to represent
                            #the changes on the admin monitor
                            writer = open('data.txt','w')
                            for sites in victims.values():
                                for site in sites:
                                    writer.write(site + " ")
                                    #number_imgs = number_imgs + 1    #TBC not needed
                            writer.close()
                               

                            #and finally we return the replaced image to the requesting client
                            #like this:
                            img_temp = cStringIO.StringIO(urllib.urlopen(str(replace_img)).read())
                            img = Image.open(img_temp)
                            img_return = cStringIO.StringIO()
                            img.save(img_return, "jpeg")
                            flow.response.content = img_return.getvalue()
                            flow.response.headers["content-type"] = ["image/jpeg"]




            except:  # Unknown image types etc.
                pass


