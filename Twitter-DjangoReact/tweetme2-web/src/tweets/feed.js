import React, { useEffect, useState }  from 'react'
import {apiTweetFeed} from './lookup'
import {Tweet} from './detail'


export function FeedList(props) {
    const [tweetsInit, setTweetsInit] = useState([])
    const [tweets, setTweets] = useState([])
    const [nextUrl, setNextUrl] = useState(null)
    const [tweetsDidSet, setTweetsDidSet] = useState(false) 
    useEffect(() => {
      const final = [...props.newTweets].concat(tweetsInit)
      if (final.length !== tweets.length) {
        setTweets(final)
      }
    }, [props.newTweets, tweets, tweetsInit])

    useEffect(() => {
      if (!tweetsDidSet) {
      const myCallback = (response, status) => {
        if (status === 200) {
          setTweetsInit(response.results)
          setNextUrl(response.next)
          setTweetsDidSet(true)
        } 
      }
      apiTweetFeed(myCallback)
    }
    }, [tweetsInit, tweetsDidSet, setTweetsDidSet])
    
    const handleDidRetweet = (newTweet) => {
      const updatedTweetsInit = [...tweetsInit]
      updatedTweetsInit.unshift(newTweet)
      setTweetsInit(updatedTweetsInit)

      const updatedFinalTweets = [...tweets]
      updatedFinalTweets.unshift(tweets)
      setTweets(updatedFinalTweets)
    }

    const handleLoadNext = (event) => {
      event.preventDefault() 
      if (nextUrl !== null) {
          const handleLoadNextResponse = (response, status) => {
            if (status === 200) {
              const newTweets = [...tweets].concat(response.results)
              setNextUrl(response.next)
              setTweets(newTweets)
              setTweetsInit(newTweets)

            }
          }
          apiTweetFeed(handleLoadNextResponse, nextUrl)
      }
    }

    return <React.Fragment>{tweets.map((item, index) => {
      return <Tweet 
        tweet={item} 
        didRetweet={handleDidRetweet}
        key={`${index}-{item.id}`}
        className='my-5 py-5 border bg-white text-dark'/>
    })}
    {nextUrl !== null && <button onClick={handleLoadNext} className='btn btn-outline-primary'>Load Next</button>}
    </React.Fragment>
  }
  