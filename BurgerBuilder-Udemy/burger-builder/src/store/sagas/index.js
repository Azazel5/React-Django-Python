import {takeEvery, all} from 'redux-saga/effects'
import * as actionTypes from '../actions/actionTypes'
import {logoutSaga, checkAuthTimeoutSaga, authUserSaga, authCheckStateSaga} from './auth'
import {initIngredientsSaga} from './burgerBuilder'
import {purchaseBurgerSaga, fetchOrderSaga} from './order'

// takeEvery is the function which 'listens' for the dispatched action. You can combine that into one
// nice function using the all method. With all they run concurrently. There are also functions 
// available like takeLatest (which only executes the latest action type).
export function* watchAuth() {
    yield all([
        takeEvery(actionTypes.AUTH_INITIATE_LOGOUT, logoutSaga),
        takeEvery(actionTypes.AUTH_CHECK_TIMEOUT, checkAuthTimeoutSaga),
        takeEvery(actionTypes.AUTH_USER, authUserSaga),
        takeEvery(actionTypes.AUTH_CHECK_STATE, authCheckStateSaga)
    ])
   
}

export function* watchBurgerBuilder() {
    yield takeEvery(actionTypes.INIT_INGREDIENTS, initIngredientsSaga)
}

export function* watchOrder() {
    yield takeEvery(actionTypes.PURCHASE_BURGER, purchaseBurgerSaga)
    yield takeEvery(actionTypes.FETCH_ORDERS, fetchOrderSaga)
}
