import React from 'react';

import './Post.css';

/**
 * Attaching this component with a withRouter (from react-router-dom) to access props passed by the
 * router to Posts.js which is rendered by a list of this current Post.js file. 
 */
const post = (props) => {
    return (
        <article onClick={props.clicked} className="Post">
            <h1>{props.title}</h1>
            <div className="Info">
                <div className="Author">{props.author}</div>
            </div>
        </article>
    )
}

export default post;