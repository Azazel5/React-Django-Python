import React, { Component } from 'react'
import Link from 'next/link'
import Router from 'next/router'

/**
 * Just setting up a folder structure creates URLs and pages, and they are all rendered server-side. No need
 * for routing at all. There's also automatic code splitting since this is all rendered server side. 
 * You cannot use CSS modules if using NextJs, but you can use styled jsx instead.. 
 * This isn't a normal lifecycle hook, as it is static and can be called without the component being 
 * instantiated. It executes first on the server, so you could do the pre-populating of props from a 
 * database or whatever.
 * We can be sure that this.props.appName will be available as getInitialProps runs first and the code
 * continues only after resolving the promise.  
 */
class IndexPage extends Component {
    static getInitialProps(context) {
        const promise = new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve({appName: 'Super App'})
            }, 1000)
        })

        return promise
    }

    render() {
        return <div>
            <h1>The main page of {this.props.appName}</h1>
            <p>Go to <Link href="/auth"><a>Auth</a></Link></p>
            <button onClick={() => Router.push("/auth")}>Go to Auth</button>
        </div>
    }
}

export default IndexPage