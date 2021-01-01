''' 
    Daily get followers and verify if they follow back. 
    Unfollow followers that don't follow back. 
'''
import os
import twitter
import json

new_list = []

def read_json(): 

    with open("following.json", 'r') as json_file: 
        following = json.load(json_file)

    return following

def unfollow(following):

    global new_list
    new_list = following
    unfollowed = []

    i = 0 
    for friend in following: 
        if i < 15:
            try:
                following_status = api.LookupFriendship(friend)
                print('verificando: ' + str(friend) + ': ' + following_status[0].name)
                if following_status[0].followed_by == False:
                        followers_list = api.GetFollowerIDs(friend, total_count = 5000)
                        if len(followers_list) < 1000: 
                            print('unfollowing: ' +  str(friend) + ' - ' + following_status[0].name)
                            api.DestroyFriendship(friend)
                            new_list.remove(friend)
                            unfollowed.append(friend)
            except Exception as e: 
                break  
            i += 1 
        else: 
            break  

    save_followers_json(new_list, 'following.json' )
    save_followers_json(unfollowed, 'unfollowed.json')

            
def save_followers_json(follow_list = None , file = 'following.json' ): 

    following_ids =  follow_list or api.GetFriendIDs()
    with open( file , 'w') as json_file: 
        json.dump(following_ids, json_file)

if __name__ == "__main__": 

    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_secret = os.getenv('ACCESS_SECRET')
  
    api = twitter.Api(consumer_key=  consumer_key ,
                  consumer_secret= consumer_secret ,
                  access_token_key= access_token ,
                  access_token_secret= access_secret) 

    try: 
        me = api.VerifyCredentials()
        
    except Exception as e: 
        raise ValueError(str(e))

    following = read_json()
    unfollow( following )
    
   
    



             

           
        




   



    
