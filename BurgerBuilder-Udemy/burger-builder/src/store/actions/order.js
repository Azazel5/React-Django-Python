import * as actionTypes from './actionTypes'

export const purchaseBurgerSuccess = (id, orderData) => {
    return {
        type: actionTypes.PURCHASE_BURGER_SUCCESS, 
        orderId: id,
        orderData: orderData
    }
}

export const purchaseBurgerFail = (error) => {
    return {
        type: actionTypes.PURCHASE_BURGER_FAIL, 
        error: error
    }
}

// An extra action creator for detecting the loading state. It is dispatched right in the beginning of the 
// purchase burger action creator. 
export const purchaseBurgerStart = () => {
    return {
        type: actionTypes.PURCHASE_BURGER_START, 
    }
}

export const purchaseBurger = (orderData, token) => {
    return {
        type: actionTypes.PURCHASE_BURGER, 
        orderData: orderData, 
        token: token
    }
}

export const purchaseInit = () => {
    return {
        type: actionTypes.PURCHASE_INIT
    }
}

export const fetchOrdersSuccess = (orders) => {
    return {
        type: actionTypes.FETCH_ORDERS_SUCCESS,
        orders: orders
    }
}

export const fetchOrdersFail = (error) => {
    return {
        type: actionTypes.FETCH_ORDERS_FAIL,
        error: error
    }
}

export const fetchOrdersStart = () => {
    return {
        type: actionTypes.FETCH_ORDERS_START,
    }
}

/**
 * After adding the authentication token to the redux store, we have to now add the authentication token 
 * to wherever we use the orders endpoint, as we have added auth != null access type to the orders 
 * node. How to get the token here? You could use 1) getState (not recommended) 2) Simply pass it 
 * where you dispatch it.
 * -----------------------------------------------------------------------------------------------------
 * It's all about passing query params to limit the orders viewed by the person (which can be done easily
 * by either Django or Firebase).
 */
export const fetchOrders = (token, userId) => {
    return {
        type: actionTypes.FETCH_ORDERS, 
        token: token, 
        userId: userId
    }
}