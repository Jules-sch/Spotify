import spotipy
import spotipy.util as util

# Enter here your username, client id and client secret as string (replace abc)
username = 'abc'
scope = 'user-library-modify'
CLIENT_ID = 'abc'
CLIENT_SECRET = 'abc'
REDIRECT_URI = 'http://localhost'

def get_t():
    token = util.prompt_for_user_token(username,
        scope ='user-library-modify',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI)
    return token
