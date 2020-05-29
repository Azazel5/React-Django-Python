import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import {FeedComponent, TweetsComponent, TweetDetailComponent} from './tweets'
import {ProfileBadge} from './profiles'

import * as serviceWorker from './serviceWorker';

const app = document.getElementById('root')
if (app) {
ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>, app);
}

const e = React.createElement
const tweetEl = document.getElementById("tweetme-2")
if (tweetEl) {
  ReactDOM.render(e(TweetsComponent, tweetEl.dataset), tweetEl);
}

const tweetFeedEl = document.getElementById("tweetme-2-feed")
if (tweetFeedEl) {
  ReactDOM.render(e(FeedComponent, tweetFeedEl.dataset), tweetFeedEl);
}

const tweetDetailElements = document.querySelectorAll(".tweetme-2-detail")
tweetDetailElements.forEach(container => {
  ReactDOM.render(
    e(TweetDetailComponent, container.dataset),
    container
  );
})

const userProfileBadgeElement = document.querySelectorAll(".tweetme-2-profile-badge")
userProfileBadgeElement.forEach(container => {
  ReactDOM.render(
    e(ProfileBadge, container.dataset),
    container
  );
})


// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
