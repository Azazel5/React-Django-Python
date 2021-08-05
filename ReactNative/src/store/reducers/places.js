// The reducer is about handling, not about dispatching
// Dispatching is done in the components, which will therefore
// use the action creators
// Payload is sent in through the dispatcher via the actionCreator

import { ADD_PLACE, DELETE_PLACE, SELECT_PLACE, DESELECT_PLACE } from '../actions/actionTypes'

const initialState = {
    places: [],
    selectedPlace: null
}

const reducer = (state = initialState, action) => {
    switch (action.type) {
        default:
            return state

        case ADD_PLACE:
            return {
                ...state,
                places: state.places.concat({
                    key: Math.random(),
                    name: action.placeName,
                    image: {
                        uri: "https://pbs.twimg.com/media/ExigaJFWgAQt48E?format=jpg&name=medium"
                    }
                })
            }

        case DELETE_PLACE:
            return {
                ...state,
                places: state.places.filter(place => {
                    return place.key !== state.selectedPlace.key
                }),
                selectedPlace: null
            }

        case SELECT_PLACE:
            return {
                ...state,
                selectedPlace: state.places.find(place => {
                    return place.key === action.placeKey
                })
            }

        case DESELECT_PLACE:
            return {
                ...state,
                selectedPlace: null
            }
    }
}

export default reducer