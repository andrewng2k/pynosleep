#!/usr/bin/env python3.5

import requests
import sys


CLIENT_ID = 'YOUR APP CLIENT ID'
CLIENT_SECRET = 'YOUR APP CLIENT SECRET'


def get_access_token():
    '''
    Requests access token
    '''
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {'grant_type': 'password',
                 'username': sys.argv[1],
                 'password': sys.argv[2]}
    headers = {'User-Agent': 'recommender by /u/duycoding710'}
    response = requests.post('https://www.reddit.com/api/v1/access_token',
                             auth=client_auth,
                             data=post_data,
                             headers=headers)
    response = response.json()
    return response['access_token']


def get_posts(token, subreddit='nosleep', count=5):
    '''
    Use access token to authorize.
    Return [limit] hot posts as json formated data
    '''
    headers = {'Authorization': 'bearer ' + token,
               'User-Agent': 'recommender by /u/duycoding710'}
    res = requests.get('https://oauth.reddit.com/r/nosleep/hot?limit=' + count,
                       headers=headers)
    res = res.json()
    return res


def filter_data(data):
    '''
    Filter and return essential data.
    '''
    posts = data['data']['children']
    result = []
    for post in posts:
        result.append((post['data']['title'],
                       post['data']['url'],
                       post['data']['author'],
                       post['data']['score'],
                       post['data']['visited']))
    return result


if __name__ == '__main__':
    output_data = filter_data(get_posts(get_access_token()))
    #  Remove contest annoucements
    del output_data[0]
    del output_data[0]
    #
    for data in output_data:
        data = tuple(map(str, data))
        #
        #  Format output string
        #
        print(data[0] + '\n' + data[2] + '  |  ' + 'Vote: ' + data[3])
        print('[Visited]') if not data[4] else print('[Not visited]')
        print('**' + data[1] + '**')
        print('-' * 45)
