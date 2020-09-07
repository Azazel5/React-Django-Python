import React, {Component} from 'react'

/**
 * Debugging using the sources tab on chrome developer tools. You can set breakpoints/use react 
 * developer tools. As of React 16, we can also use error boundaries. It uses a lifecycle method
 * to determine if there was an error thrown, and is a good way to strucutre your website if you
 * rely on server calls etc, where it can fail sometimes. Wrap up your problematic components 
 * with this error boundary: in the error case, it uses the componentDidCatch to set the state, and 
 * returns props.children if there's no problem (which is why you wrap it), otherwise throws the 
 * error message. Very neat trick.  
 * On the App file, note that you had to move the key prop from Person to ErrorBoundary because it
 * has to be placed on the outermost element being mapped. 
 * Remember, you will still see the react error because we are still in development (in production you
 * will see whatever you logged here). Only use this when you expect an error and cannot do anything
 * about it. 
 */

class ErrorBoundary extends Component {
    constructor(props) {
        super(props)
        this.state = {
            hasError: false, 
            errorMessage: '' 
        }
    }

    componentDidCatch = (error, info) => {
        this.setState({
            hasError: true, 
            errorMessage: error
        })
    }

    render() {
        if(this.state.hasError) {
            return <h1>{this.state.errorMessage}</h1>
        } else {
            return this.props.children  
        }
    }
}

export default ErrorBoundary