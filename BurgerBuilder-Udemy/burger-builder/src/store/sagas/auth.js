import { put, call, delay } from "redux-saga/effects";
import axios from "axios";

import * as actions from "../actions/index";

/**
 * These are called generators. They run incrtementally and can pause during execution. Put dispatches 
 * a new action. In a generator, you must prepend things with the yield keyword, so that the code 
 * waits for things to finish.
 * Saga workflow: dispatch an action, listen to it, so the generator can run once the action is 
 * recognized. 
 * You have to execute the action creator functions when you use it in the sagas. 
 * Executing asynchronous code such as API calls is done using the yield keyword, so you don't have
 * to manually check the resolution of promised: the code waits for it. 
 * Note - localStorage is a synchronous action, so we don't really need those yields below (but added them
 * anyways!)
 * We can also use other helps like call or fork, which do different things as can be seen in the 
 * saga documentation. The call function makes the generators testable. 
 */
export function* logoutSaga(action) {
  yield call([localStorage, 'removeItem'], "token")
  yield call([localStorage, 'removeItem'], "expirationDate")
  yield call([localStorage, 'removeItem'], "userId")
  yield put(actions.logoutSucceed());
}

export function* checkAuthTimeoutSaga(action) {
  yield delay(action.expirationTime * 1000);
  yield put(actions.logout());
}

export function* authUserSaga(action) {
  yield put(actions.authStart());
  const authData = {
    email: action.email,
    password: action.password,
    returnSecureToken: true
  };
  let url =
    "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=AIzaSyBom_JvK1Cc9U3-RRP5HXQnN2Tfe3eyu_c";
  if (!action.isSignup) {
    url =
      "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyBom_JvK1Cc9U3-RRP5HXQnN2Tfe3eyu_c";
  }
  try {
    const response = yield axios.post(url, authData);

    const expirationDate = yield new Date(
      new Date().getTime() + response.data.expiresIn * 1000
    );
    yield localStorage.setItem("token", response.data.idToken);
    yield localStorage.setItem("expirationDate", expirationDate);
    yield localStorage.setItem("userId", response.data.localId);
    yield put(
      actions.authSuccess(response.data.idToken, response.data.localId)
    );
    yield put(actions.checkAuthTimeout(response.data.expiresIn));
  } catch (error) {
    yield put(actions.authFail(error.response.data.error));
  }
}

export function* authCheckStateSaga(action) {
  const token = yield localStorage.getItem("token");
  if (!token) {
    yield put(actions.logout());
  } else {
    const expirationDate = yield new Date(
      localStorage.getItem("expirationDate")
    );
    if (expirationDate <= new Date()) {
      yield put(actions.logout());
    } else {
      const userId = yield localStorage.getItem("userId");
      yield put(actions.authSuccess(token, userId));
      yield put(
        actions.checkAuthTimeout(
          (expirationDate.getTime() - new Date().getTime()) / 1000
        )
      );
    }
  }
}
