import * as actionTypes from './actionTypes';
import axios from 'axios';
export const authStart = () => {
    return {
        type: actionTypes.AUTH_START
    };
};

export const authSuccess = (token) => {
    return {
        type: actionTypes.AUTH_SUCCESS,
        idToken: token
    };
};

export const authFail = (error) => {
    return {
        type: actionTypes.AUTH_FAIL,
        error: error
    };
};
export const logout = () => {
    return {
        type: actionTypes.AUTH_LOGOUT
    };
};

export const auth = (email, password, isSignUp) => {
    let url = '';
    if(isSignUp) {
        url = '/api/users';
    } else {
        url = '/api/tokens';
    }
    return dispatch => {
        dispatch(authStart());
        const authData = {
            email : email,
            password : password
        };
        axios.post(url, {
            'email': email,
            'password': password,
        })
            .then(response => {
                console.log(response);
                dispatch(authSuccess(response.data.token));
            })
            .catch(err => {
                console.log(err.response.data.message);
                dispatch(authFail(err.response.data.message));
            })

    };
};