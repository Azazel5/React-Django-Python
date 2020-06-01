import React from 'react'
import {FormComponent} from './FormComponent'

export class Form extends React.Component {
    constructor() {
        super() 
        this.state = {
            firstName: "", 
            lastName: "", 
            age: "", 
            gender: "", 
            option1: false, 
            option2: false,
            option3: false 
        }

        this.onChange = this.onChange.bind(this)
    }

    onChange(event) {
        /**
         * Checkboxes need to be checked for specifically. JavaScript supports object unpacking 
         * just like tuples in python. 
         */
        const {name, value, checked, type} = event.target 
        type === "checkbox" ? 
        this.setState({[name]: checked}):
        this.setState({[name]: value})
    }

    render() {
       return (
            /**
             * The state is sent to the component using the ... spread operator. 
             * Thus, you will have access to props.firstName etc in the component. If you 
             * don't like that, you can pass in a prop (such as data), which holds the entire 
             * state and you'll have to access it like props.data.firstName. 
             */
            <FormComponent onChange={this.onChange} {...this.state}/>
       )
    }
}