import spotipy
import spotipy.util as util

# Enter here your username, client id and client secret as string
username = 'Julian Schmocker'
scope = 'user-library-modify'
CLIENT_ID = 'f3517e840690430ca445d6b69a6ecd5c'
CLIENT_SECRET = 'a044144a2f884bd9872e8db7b4747576'
REDIRECT_URI = 'http://localhost'

def get_t():
    token = util.prompt_for_user_token(username,
        scope ='user-library-modify',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI)
    return token
