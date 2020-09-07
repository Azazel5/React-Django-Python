import React, { Component } from 'react';
import axios from 'axios'

import './FullPost.css';

class FullPost extends Component {
    constructor(props) {
        super(props)
        this.state = {
            loadedPost: null
        }
    }

    componentDidMount() {
        this.loadData()
    }

    componentDidUpdate() {
        this.loadData()
    }

    loadData() {
        if (this.props.match.params.id) {
            if (!this.state.loadedPost ||
                (this.state.loadedPost && this.state.loadedPost.id != this.props.match.params.id)) {
                axios.get(`/posts/${this.props.match.params.id}`)
                    .then(response => {
                        this.setState({ loadedPost: response.data })
                    })
            }
        }
    }

    deletePostHandler = () => {
        axios.delete(`/posts/${this.props.march.params.id}`)
            .then(response => console.log(response))
    }

    /**
     * Be careful here that you will get your props before your 'loadedPost', so it will be null 
     * if you try to set it immediately (fetching data is asynchronous). If you check the network tab
     * at this point, you'll see that you'll enter an infinite loop of sending requests. This is because you
     * shouldn't update your state from within the componentDidUpdate.
     */
    render() {
        const loadedPost = this.state.loadedPost
        let post = <p style={{ textAlign: 'center' }}>Please select a Post!</p>;
        if (this.props.match.params.id) {
            post = <p style={{ textAlign: 'center' }}>Loading...</p>;
        }
        if (loadedPost) {
            post = (
                <div className="FullPost">
                    <h1>{loadedPost.title}</h1>
                    <p>{loadedPost.body}</p>
                    <div className="Edit">
                        <button onClick={this.deletePostHandler} className="Delete">Delete</button>
                    </div>
                </div>

            );
        }
        return post;
    }
}

export default FullPost;