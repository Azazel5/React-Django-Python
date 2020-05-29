import {backLookup} from '../lookup'

export function apiProfileDetail(username, callback) {
    backLookup('GET', `/profile/${username}/`, callback)
}

export function apiProfileFollowToggle(username, action, callback) {
    const data = {"action": `${action && action}`.toLowerCase()}
    backLookup('POST', `/profile/${username}/follow/`, callback, data)
}