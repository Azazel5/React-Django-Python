import React, { Component } from 'react'
import Input from '../../components/UI/Input/Input'
import Button from '../../components/UI/Button/Button'

import { connect } from 'react-redux'
import { Redirect } from 'react-router-dom'
import * as actionCreators from '../../store/actions/index'
import classes from './Auth.module.css'
import Spinner from '../../components/UI/Spinner/Spinner'
import {updateObject, checkValidity} from '../../shared/utility'

class Auth extends Component {
    constructor(props) {
        super(props)
        this.state = {
            controls: {
                email: {
                    inputType: 'input',
                    elementConfig: {
                        type: 'email',
                        placeholder: 'Your Email',
                    },
                    value: '',
                    validation: {
                        required: true,
                    },
                    valid: false,
                    touched: false
                },

                password: {
                    inputType: 'input',
                    elementConfig: {
                        type: 'password',
                        placeholder: 'Password',
                    },
                    value: '',
                    validation: {
                        required: true,
                        minLength: 7
                    },
                    valid: false,
                    touched: false
                }
            },
            isSignUp: true
        }
    }

    componentDidMount() {
        if(!this.props.buildingBurger && this.props.authRedirectPath !== '/') {
            this.props.onSetAuthRedirect()
        }
    }

    inputChangedHandler = (event, controlName) => {
        const updatedControls = updateObject(this.state.controls, {
            [controlName]: updateObject(this.state.controls[controlName], {
                value: event.target.value,
                valid: checkValidity(event.target.value, this.state.controls[controlName].validation),
                touched: true
            })
        })

        this.setState({ controls: updatedControls })
    }

    submitHandler = event => {
        event.preventDefault()
        this.props.onAuth(
            this.state.controls.email.value,
            this.state.controls.password.value,
            this.state.isSignUp
        )
    }

    switchAuthModeHandler = () => {
        this.setState(prevState => {
            return {
                isSignUp: !prevState.isSignUp
            }
        })
    }

    render() {
        const formArray = []
        for (let key in this.state.controls) {
            formArray.push({
                id: key,
                config: this.state.controls[key]
            })
        }

        let form = formArray.map(element => {
            return <Input
                key={element.id}
                shouldValidate={element.config.validation}
                invalid={!element.config.valid}
                elementType={element.config.inputType}
                elementConfig={element.config.elementConfig}
                value={element.config.value}
                touched={element.config.touched}
                changed={(event) => this.inputChangedHandler(event, element.id)} />
        })

        if (this.props.loading) {
            form = <Spinner />
        }

        let errorMessage = null
        // We're using the message property in the error as that's what firebase gives back. Tailor this
        // to your own backend. 
        if (this.props.error) {
            errorMessage = (
                <p>{this.props.error.message}</p>
            )
        }

        let authRedirect = null 
        if(this.props.isAuthenticated) {
            authRedirect = <Redirect to={this.props.authRedirectPath}/>
        }

        return (
            <div className={classes.Auth}>
                {authRedirect}
                {errorMessage}
                <form onSubmit={this.submitHandler}>
                    {form}
                    <Button buttonType="Success">Submit</Button>
                </form>
                <Button
                    clicked={this.switchAuthModeHandler}
                    buttonType="Danger">{this.state.isSignUp ? 'Sign Up' : 'Login'}</Button>
            </div>
        )
    }
}

const mapStateToProps = state => {
    return {
        loading: state.auth.loading,
        error: state.auth.error,
        isAuthenticated: state.auth.token !== null, 
        buildingBurger: state.burger.building, 
        authRedirectPath: state.auth.authRedirectPath
    }
}

const mapDispatchToProps = dispatch => {
    return {
        onAuth: (email, password, isSignUp) => dispatch(actionCreators.auth(email, password, isSignUp)), 
        onSetAuthRedirect: () => dispatch(actionCreators.setAuthRedirectPath('/'))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Auth)