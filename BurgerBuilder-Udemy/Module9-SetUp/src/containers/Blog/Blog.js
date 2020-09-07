import React, { Component } from 'react';
import './Blog.css';
import Posts from './Posts/Posts'
//import NewPost from './NewPost/NewPost'
import { Route, NavLink, Switch, Redirect } from 'react-router-dom'
import asynComponent from '../../hoc/ayncComponent'

// Dynamic import used in our higher order component to only load NewPost when the HOC is used.
const AsyncNewPost = asynComponent(() => {
    return import('./NewPost/NewPost')
})

/**
 * You can pass a second argument to axios to configure the request. Axios requests happens 
 * asynchronously, so it uses promises.
 * Sometimes you want to execute some code globally after requests, which you can do using axios
 * using inter-seters. You can log responses, set headers etc globally.
 * ---------------------------------------------------------------------------------------------
 * The router tag takes in the path prop which is a prefix. You can add 'exact' for an exact match.
 * Use the Link tag to tackle the problem stated in Posts.js.
 * The to prop in Link always builds an absolute path, so if you want to build relative path you
 * will have to use this.props.match.url + '/path-adder'
 * Use NavLink to apply styling to active links. You can also add activeClassName to set another 
 * name for the active class.
 * Lazy loading is the concept of only loading what is required. If you load the entire bundle.js
 * file for a big application, it can harm performance. 
 */

class Blog extends Component {
    state = {
        auth: true 
    }

    render() {
        return (
            <div className="Blog">
                <header>
                    <nav>
                        <ul>
                            <li><NavLink to="/posts" exact>Posts</NavLink></li>
                            <li><NavLink to="/new-post">New Post</NavLink></li>
                        </ul>
                    </nav>
                </header>
                {
                /* <Route path="/" exact render={() => <h1>Home</h1>}/> 
                    new-post can be potentially recognized as id, which is
                    why it was moved to the position before.
                    Switch: the first route that matches is passed. The 
                    order of URLs is important while using switch. While using redirect, 
                    if you call it outside the switch, you cannot specify the from
                    property. 
                */}
                <Switch>
                    {this.state.auth && <Route path="/new-post" component={AsyncNewPost}/>}
                    <Route path="/posts" component={Posts}/>
                    <Route render={() => <h1>Not found</h1>} />
                    {/* <Redirect to="/posts" from="/" /> */}
                </Switch>
            </div>
        );
    }
}

export default Blog;