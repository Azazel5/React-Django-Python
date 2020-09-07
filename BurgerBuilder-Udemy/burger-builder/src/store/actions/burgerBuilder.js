import * as actionTypes from './actionTypes'

export const addIngredients = (name) => {
    return {
        type: actionTypes.ADD_INGREDIENTS,
        ingredientName: name 
    }
}

export const removeIngredients = (name) => {
    return {
        type: actionTypes.REMOVE_INGREDIENTS,
        ingredientName: name 
    }
}

/** 
 * The workflow of executing async code for one given action type in redux is:
 * 1. Create the async creator which returns dispatch
 * 2. Create a normal synchronous creator, which simply returns whatever
 * 3. Use the normal function in the dispatch method, and pass the result 
 *    as the argument 
 */
export const setIngredients = (ingredients) => {
    return {
        type: actionTypes.SET_INGREDIENTS,
        ingredients: ingredients
    }
}

export const fetchIngredientsFailed = () => {
    return {
        type: actionTypes.FETCH_INGREDIENTS_FAILED
    }
}

export const initIngredients = () => {
    return {
        type: actionTypes.INIT_INGREDIENTS
    }
}