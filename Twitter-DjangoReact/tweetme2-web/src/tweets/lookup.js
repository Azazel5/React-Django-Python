import {backLookup} from '../lookup'

export function apiTweetCreate(newTweet, callback) {
    backLookup('POST', '/tweets/create/', callback, {content: newTweet})
}

export function apiTweetAction(tweetId, action, callback) {
    const data = {
        id: tweetId,
        'action': action
    }
    backLookup('POST', '/tweets/action/', callback, data)
}

export function apiTweetList(username, callback, nextUrl) {
    let endpoint = '/tweets/'
    if (username) {
        endpoint = `/tweets/?username=${username}`
    }

    if (nextUrl !== null && nextUrl !== undefined) {
        endpoint = nextUrl.replace("http://localhost:8000/api", "")
    }

    backLookup('GET', endpoint, callback)
}

export function apiTweetDetail(tweetId, callback) {
    backLookup('GET', `/tweets/${tweetId}/`, callback)
}

export function apiTweetFeed(callback, nextUrl) {
    let endpoint = '/tweets/feed/'

    if (nextUrl !== null && nextUrl !== undefined) {
        endpoint = nextUrl.replace("http://localhost:8000/api", "")
    }

    backLookup('GET', endpoint, callback)
}