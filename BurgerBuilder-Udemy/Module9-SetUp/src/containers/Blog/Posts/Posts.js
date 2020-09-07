import React, { Component } from 'react'
import Post from '../../../components/Post/Post'
import {Route} from 'react-router-dom'
import axios from 'axios'
import FullPost from '../FullPost/FullPost'
import './Posts.css'

/**
 * Using the default axios here instead of the custom axios because it was taking too much time for some reason.
 * Understand that using routers may reload the page, which refreshes the state of your react components, which
 * is not what you want. Thus, you have to tell react what to re-render. 
 */
class Posts extends Component {
    constructor(props) {
        super(props)
        this.state = {
            posts: [],
        }
    }

    componentDidMount() {
        axios.get('/posts')
            .then(response => {
                const posts = response.data.slice(0, 4)
                const updatedPost = posts.map(post => {
                    return {
                        ...post,
                        author: 'Subhanga'
                    }
                })
                this.setState({ posts: updatedPost })
            })
            .catch(error => {
                console.log(error)
                this.setState({ error: true })
            })
    }

    postSelected = (id) => {
        this.props.history.push({pathname: `/posts/${id}`})
    }

    render() {
        let posts = <p style={{ textAlign: 'center' }}>Something went wrong!</p>
        if (!this.state.error) {
            posts = this.state.posts.map(post => {
                return (
                    //<Link key={post.id} to={`/posts/${post.id}`}>
                        <Post key={post.id} clicked={() => this.postSelected(post.id)} author={post.author}
                        title={post.title} />
                    //</Link>
                )
            })
        }

        return (
            <div>
            <section className="Posts">
                {posts}
            </section>
            <Route path={`${this.props.match.url}/:id`} exact component={FullPost} />
            </div>
        )
    }
}

export default Posts