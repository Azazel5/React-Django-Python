import React, { Component } from 'react'
import Aux from '../../../hoc/Aux/Aux'
import Button from '../../UI/Button/Button'

class OrderSummary extends Component {
    componentDidUpdate() {
        console.log("[OrderSummary.js] did update")
    }
    
    render() {
        const ingredientSummary = Object.keys(this.props.ingredient )
        .map(ingredient => {
            return (
                <li key={ingredient}>
                    <span style={{textTransform: 'capitalize'}}>
                    {ingredient}</span>: {this.props.ingredient[ingredient]}
                </li>
            )
        })

        return (
        <Aux>
            <h3>Your order</h3>
            <p>A delicious burger with the following ingredients: </p>
            <ul>
                {ingredientSummary}
            </ul>
            <p><strong>Total Price: {this.props.price.toFixed(2)}</strong></p>
            <p>Continue to checkout?</p>
            <Button clicked={this.props.onCancel} buttonType="Danger">CANCEL</Button>
            <Button clicked={this.props.onPurchase} buttonType="Success">CONTINUE</Button>
        </Aux>
        )
    }
}

export default OrderSummary