import React, { Component } from 'react'
import Aux from '../../hoc/Aux/Aux'
import Burger from '../../components/Burger/Burger'
import axios from '../../axios-orders'
import BuildControls from '../../components/Burger/BuildControls/BuildControls'
import Modal from '../../components/UI/Modal/Modal'
import OrderSummary from '../../components/Burger/OrderSummary/OrderSummary'
import Spinner from '../../components/UI/Spinner/Spinner'
import withErrorHandler from '../../hoc/withErrorHandler/withErrorHandler'
import {connect} from 'react-redux'
import * as actionCreators from '../../store/actions/index'


export class BurgerBuilder extends Component {
    constructor(props) {
        super(props)
        this.state = {
            purchasing: false, 
        }
    }

    componentDidMount() {
        this.props.onInitIngredient()
    }

    /**
     * Be careful while using state in multiple areas, for example - here, if you simple use
     * this.state.ingredients, it will be an older version of state as compared to the add/remove
     * ingredient handler. So here, it makes sense for the update function to get the state from
     * those functions as arguments, which will fix that problem. State is updated asynchronously.
     */
    updatePurchaseState = (ingredients) => {
        const sum = Object.keys(ingredients)
        .map(key => {
            return ingredients[key]
        })
        .reduce((sum, el) => {
            return sum + el
        }, 0)

        return sum > 0
    }

    // Wherever you are sure that your component is being used by the router, you can simply use
    // the history object to redirect, without using the redirect component.
    purchaseHandler = () => {
        if(this.props.isAuthenticated) {
        this.setState({purchasing: true})
        } else {
            this.props.onSetRedirectAuth('/checkout')
            this.props.history.push('/auth')
        }
    }

    purchaseCancelHandler = () => {
        this.setState({purchasing: false})
    }

    purchaseContinueHandler = () => {
        this.props.onInitPurchase()
        this.props.history.push('/checkout')
    }

    render() {
        const disabledInfo = { 
            ...this.props.ings
        }

        for(let key in disabledInfo) {
            disabledInfo[key] = disabledInfo[key] <=0
        }

        let orderSummary = null 
        let burger = this.props.error ? <p>Ingredients can't be loaded</p>: <Spinner />
        if(this.props.ings) {
            burger = (
                <Aux>
                    <Burger ingredients={this.props.ings}/>
                    <BuildControls 
                        isAuthenticated={this.props.isAuthenticated}
                        onAdd={this.props.onIngredientAdded} 
                        onRemove={this.props.onIngredientRemoved}
                        disabled={disabledInfo}
                        price={this.props.price}
                        purchasable={this.updatePurchaseState(this.props.ings)}
                        purchaseHandler={this.purchaseHandler}/>
                </Aux>
            )

            orderSummary = <OrderSummary 
            onPurchase={this.purchaseContinueHandler}
            onCancel={this.purchaseCancelHandler}
            ingredient={this.props.ings}
            price={this.props.price} />
        }
        
        return (
            <Aux>
                <Modal 
                    modalClosed={this.purchaseCancelHandler}
                    show={this.state.purchasing}>
                    {orderSummary}
                </Modal>
                {burger}
            </Aux>
        )
    }
}

const mapStateToProps = state => {
    return {
        ings: state.burger.ingredients, 
        price: state.burger.totalPrice, 
        error: state.burger.error, 
        isAuthenticated: state.auth.token !== null 
    }
}

const mapDispatchToProps = dispatch => {
    return {
        onIngredientAdded: (ingName) => dispatch(actionCreators.addIngredients(ingName)),
        onIngredientRemoved: (ingName) => dispatch(actionCreators.removeIngredients(ingName)),
        onInitIngredient: () => dispatch(actionCreators.initIngredients()),
        onInitPurchase: () => dispatch(actionCreators.purchaseInit()), 
        onSetRedirectAuth: (path) => dispatch(actionCreators.setAuthRedirectPath(path))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(withErrorHandler(BurgerBuilder, axios))