import React, { Component } from 'react'
import Button from '../../../components/UI/Button/Button'
import classes from './ContactData.module.css'
import Spinner from '../../../components/UI/Spinner/Spinner'
import axios from '../../../axios-orders'
import Input from '../../../components/UI/Input/Input'
import {connect} from 'react-redux'
import withErrorHandler from '../../../hoc/withErrorHandler/withErrorHandler'
import * as actionCreators from '../../../store/actions/index'
import {updateObject, checkValidity} from '../../../shared/utility'


class ContactData extends Component {
    constructor(props) {
        super(props)
        this.state = {
            orderForm: {
                name: {
                    inputType: 'input', 
                    elementConfig: {
                        type: 'text', 
                        placeholder: 'Your Name', 
                    },
                    value: '', 
                    validation: {
                        required: true, 
                    },
                    valid: false,
                    touched: false 
                },
                street: {
                    inputType: 'input', 
                    elementConfig: {
                        type: 'text', 
                        placeholder: 'Your Street', 
                    },
                    value: '',
                    validation: {
                        required: true, 
                    },
                    valid: false,
                    touched: false
                },
                zipCode: {
                    inputType: 'input', 
                    elementConfig: {
                        type: 'text', 
                        placeholder: 'Your ZipCode', 
                    },
                    value: '',
                    validation: {
                        required: true, 
                        minLength: 5, 
                        maxLength: 5
                    },
                    valid: false,
                    touched: false
                },
                country: {
                    inputType: 'input', 
                    elementConfig: {
                        type: 'text', 
                        placeholder: 'Your Country', 
                    },
                    value: '',
                    validation: {
                        required: true, 
                    },
                    valid: false,
                    touched: false
                },
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
                deliveryMethod: {
                    inputType: 'select', 
                    elementConfig: {
                        options: [
                                {value: 'fastest', displayValue: 'Fastest'},
                                {value: 'cheapest', displayValue: 'Cheapest'}
                        ]
                    },
                    value: 'fastest',
                    validation: {},
                    valid: true
                }
            },
            formIsValid: false 
        }
    }

    // Firebase uses a MongoDB style database. No tables, just a JSON-like strucutre. If you pass a 
    // baseURL/orders, it will create an orders node. (.json for firebase)
    orderHandler = (event) => {
        event.preventDefault()

        const formData = {}
        for(let formElement in this.state.orderForm) {
            formData[formElement] = this.state.orderForm[formElement].value
        }

        const orderObj = {
            ingredients: this.props.ings,
            price: this.props.price,
            orderData: formData, 
            userId: this.props.userId 
        }

        this.props.onOrderBurger(orderObj, this.props.token)
    }

    // In a deeply nested object like the orderForm object, just using the spread operator doesn't deeply 
    // the object.
    inputChangedHandler = (event, input) => {
 
        const updatedFormElem = updateObject(this.state.orderForm[input], {
            value: event.target.value , 
            valid: checkValidity(event.target.value, this.state.orderForm[input].validation), 
            touched: true
        })

        const updatedOrderForm = updateObject(this.state.orderForm, {
                [input]: updatedFormElem
        })

        let formIsValid = true 
        for(let identifier in updatedOrderForm) {
            formIsValid = updatedOrderForm[identifier].valid && formIsValid
        }
        this.setState({orderForm: updatedOrderForm, formIsValid: formIsValid })
    }

    // Need to create an array out of the orderForm above
    render() {
        const formArray = []
        for(let key in this.state.orderForm) {
            formArray.push({
                id: key, 
                config: this.state.orderForm[key]
            })
        }

        let form = (
            <form onSubmit={this.orderHandler}>
                {formArray.map(element => {
                    return <Input key={element.id}
                        shouldValidate={element.config.validation}
                        invalid={!element.config.valid}
                        elementType={element.config.inputType} 
                        elementConfig={element.config.elementConfig}
                        value={element.config.value}
                        touched={element.config.touched}
                        changed={(event) => this.inputChangedHandler(event, element.id)}/>
                })}
                <Button disable={!this.state.formIsValid} buttonType="Success">Order here</Button>
            </form>
        )

        if (this.props.loading) {
            form = <Spinner />
        }

        return (
            <div className={classes.ContactData}>
                <h4>Enter your contact information.</h4>
                {form}
            </div>
        )
    }
}

const mapStateToProps = state => {
    return {
        ings: state.burger.ingredients,
        price: state.burger.totalPrice, 
        loading: state.order.loading, 
        token: state.auth.token, 
        userId: state.auth.userId 
    }
}

const mapDispatchToProps = dispatch => {
    return {
        onOrderBurger: (orderData, token) => dispatch(actionCreators.purchaseBurger(orderData, token))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(withErrorHandler(ContactData, axios))