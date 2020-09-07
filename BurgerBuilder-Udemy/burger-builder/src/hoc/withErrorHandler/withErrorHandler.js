import React, { Component } from 'react'
import Modal from '../../components/UI/Modal/Modal'
import Aux from '../../hoc/Aux/Aux'

/**
 * The other style of higher order component, which simply is a function which returns a functional 
 * component. The received props needs to be distributed in the wrapped component. It is used by 
 * wrapping it over the exported component. This is a good way of showing custom error components to 
 * componenets which you know might receieve unexpected errors (such as absent internet connections)
 * etc. This h.o.c is returning an anonymous class with an axios arugment to listen to any errors.
 * If we detect an error is when we want 
 */

const withErrorHandler = (WrappedComponent, axios) => {
    return class extends Component {
        constructor(props) {
            super(props)
            this.state = {error: null}
        }

        componentWillMount() {
            this.reqInt = axios.interceptors.request.use(request => {
                this.setState({error: null})
                return request
            })
            this.resInt = axios.interceptors.response.use(res => res, error => {
                this.setState({error: error})
            })  
        }

        componentWillUnmount() {
            axios.interceptors.request.eject(this.reqInt)
            axios.interceptors.response.eject(this.resInt)
        }

        errorConfirmedHandler = () => {
            this.setState({error: null})
        }

        render() {
            return (
                <Aux>
                    <Modal modalClosed={this.errorConfirmedHandler} show={this.state.error}>
                        {this.state.error ? this.state.error.message: null}
                    </Modal>
                    <WrappedComponent {...this.props} />
                </Aux>
            )
        }
    }
}

export default withErrorHandler

/**
 * Since useEffect runs after the render cycle (and componentWillMount runs before),
 * we need some other hook. Simple! Just put the code before the JSX. It is a function, and 
 * the code runs linearly.

 * Hookified withErrorHandler.js 
 * const withErrorHandler = (WrappedComponent, axios) => {
 *      return props => {
 *      const [error, setError] = useState(null)
 *      const reqInt = axios.interceptors.request.use(request => {
            setError(null)
            return request
        })

        const resInt = axios.interceptors.response.use(res => res, err => {
            setError(err)
        })  

        useEffect(() => {
            return () => {
                axios.interceptors.request.eject(reqInt)
                axios.interceptors.response.eject(resInt)
            }
        }, [reqInt, resInt])

        errorConfirmedHandler = () => {
            setError(null)  
        }

        return (
            <Aux>
                <Modal modalClosed={errorConfirmedHandler} show={error}>
                    {error ? error.message: null}
                </Modal>
                <WrappedComponent {...props} />
            </Aux>
        )
 *  }
 * } 
 */