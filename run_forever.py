''' 
    Daily get followers and verify if they follow back. 
    Unfollow followers that don't follow back. 
'''

import os , sys 
import twitter
import json
import signal

new_list = []

def signal_handler(signal, frame): 
    print('You pressed ctrl+c')
    if len(new_list) > 1: 
        save_followers_json(new_list)
    sys.exit()

def postTweet(message): 
    try:
        status = api.PostUpdate(message)

    except :
        print("Your message could not be encoded.  Perhaps it contains non-ASCII characters? ")
        print("Try explicitly specifying the encoding with the --encoding flag")
        sys.exit(2)

    print("{0} just posted: {1}".format(status.user.name, status.text))


def read_json(): 

    with open("following.json", 'r') as json_file: 
        following = json.load(json_file)

    return following

def unfollow(following):

    global new_list
    new_list = following

    for friend in following: 
        following_status = api.LookupFriendship(friend)
        print('verificando: ' + str(friend) + ': ' + following_status[0].name)
        if following_status[0].followed_by == False:
            try: 
                followers_list = api.GetFollowerIDs(friend, total_count = 5000)
                if len(followers_list) < 1000: 
                    print('unfollowing: ' +  str(friend) + ' - ' + following_status[0].name)
                    new_list.remove(friend)
                    api.DestroyFriendship(friend)
            
            except Exception as e: 
                print(str(e))
                pass 
            

def save_followers_json(follow_list = None ): 

    following_ids =  follow_list or api.GetFriendIDs()
    with open('following.json', 'w') as json_file: 
        json.dump(following_ids, json_file)

if __name__ == "__main__": 

    signal.signal(signal.SIGINT, signal_handler) 

    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_secret = os.getenv('ACCESS_SECRET')
    
    consumer_key = CONSUMER_KEY
    consumer_secret = CONSUMER_SECRET
    access_token = ACCESS_TOKEN
    access_secret = ACCESS_SECRET
    api = twitter.Api(consumer_key=  consumer_key ,
                  consumer_secret= consumer_secret ,
                  access_token_key= access_token ,
                  access_token_secret= access_secret ,sleep_on_rate_limit=True ) 

    me = api.VerifyCredentials()
    #save_followers_json()
    following = read_json()
    unfollow( following )
    



             

           
        




   



    
