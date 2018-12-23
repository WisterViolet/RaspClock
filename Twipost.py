import keyAPI
import twitter


def Twi_aupos(state):
    try:
        auth = twitter.OAuth(consumer_key=keyAPI.CK,
                             consumer_secret=keyAPI.CS,
                             token=keyAPI.AT,
                             token_secret=keyAPI.ATS)
        po = twitter.Twitter(auth=auth)
        po.statuses.update(status=state)
        return 0
    except:
        print('error')
        return -1
