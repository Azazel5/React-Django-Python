import React, { useEffect, useState } from 'react'
import { apiProfileDetail, apiProfileFollowToggle } from './lookup'
import { UserDisplay, UserPicture } from './components'
import {DisplayCount} from './utils'

function Badge(props) {
    const { user, didFollowToggle, profileLoading } = props
    let currentVerb = user && user.is_following ? "Unfollow" : "Follow"
    currentVerb = profileLoading ? "Loading...": currentVerb
    const handleFollowToggle = (event) => {
        event.preventDefault()
        if (didFollowToggle && !profileLoading) {
            didFollowToggle(currentVerb)
        }
    }
    return user ? <div>
        <UserPicture user={user} hideLink />
        <p><UserDisplay user={user} includeFullName hideLink /></p>
<p><DisplayCount>{user.follower_count}</DisplayCount> {user.follower_count === 1 ? "follower": "followers"}</p>
<p><DisplayCount>{user.following_count}</DisplayCount> following </p>
<p>{user.location}</p>
<p>{user.bio}</p>

<button onClick={handleFollowToggle} className="btn btn-primary">{currentVerb}</button>
    </div> : null
}

export function ProfileBadge(props) {
    const { username } = props
    const [didLookup, setDidLookup] = useState(false)
    const [profile, setProfile] = useState(null)
    const [profileLoading, setProfileLoading] = useState(false)

    const handleBackendLookup = (response, status) => {
        if (status === 200) {
            setProfile(response)
        }
    }
    useEffect(() => {
        if (!didLookup) {
            apiProfileDetail(username, handleBackendLookup)
            setDidLookup(true)
        }

    }, [username, didLookup, setDidLookup])

    const handleNewFollow = (actionVerb) => {
        apiProfileFollowToggle(username, actionVerb, (response, status) => {
            if (status === 200) {
                setProfile(response)
            }
        })
        setProfileLoading(false)

    } 
    return didLookup === false ? "Loading..." : <Badge user={profile} didFollowToggle={handleNewFollow} profileLoading={profileLoading}/>
}