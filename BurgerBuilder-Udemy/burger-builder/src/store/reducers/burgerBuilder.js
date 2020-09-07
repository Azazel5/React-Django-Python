import * as actionTypes from '../actions/actionTypes'
import {updateObject} from '../../shared/utility'


const initialState = {
    ingredients: null,
    totalPrice: 4,
    error: false, 
    building: false 
}

const INGRIDIENT_PRICES = {
    salad: 0.5, 
    cheese: 0.4, 
    meat: 1.3, 
    bacon: 0.7
}

const addIngredient = (state, action) => {
    const updatedIngredient = {[action.ingredientName]: state.ingredients[action.ingredientName] + 1}
    const updatedIngredients = updateObject(state.ingredients, updatedIngredient)
    const updatedState = {
        ingredients: updatedIngredients, 
        totalPrice: state.totalPrice + INGRIDIENT_PRICES[action.ingredientName], 
        building: true 
    }
    return updateObject(state, updatedState)
}

const removeIngredient = (state, action) => {
    const updatedIng= {[action.ingredientName]: state.ingredients[action.ingredientName] - 1}
    const updatedIngs = updateObject(state.ingredients, updatedIng)
    const updatedSt = {
        ingredients: updatedIngs, 
        totalPrice: state.totalPrice - INGRIDIENT_PRICES[action.ingredientName], 
        building: true 
    }
    return updateObject(state, updatedSt)
}

const setIngredients = (state, action) => {
    return updateObject(state, {
        ingredients: action.ingredients, 
        error: false,
        totalPrice: 4, 
        building: false 
    })
}

// In ES6, you can pass [{var_name}], which is the variable name you wanna use.
const reducer = (state = initialState, action) => {
    switch(action.type) {
        case actionTypes.ADD_INGREDIENTS:
           return addIngredient(state, action)

        case actionTypes.REMOVE_INGREDIENTS:
            return removeIngredient(state, action)
        
        case actionTypes.SET_INGREDIENTS: 
            return setIngredients(state, action)
            
        case actionTypes.FETCH_INGREDIENTS_FAILED: 
            return updateObject(state, {error: true})

        default:
            return state
    }
}

export default reducer 