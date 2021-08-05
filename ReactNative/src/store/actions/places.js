import { ADD_PLACE, DELETE_PLACE, SELECT_PLACE, DESELECT_PLACE } from './actionTypes'

// Action creators
// Side effects are always handled in the actions
// Action creators act as factories for creating actions
// which are JS objects after all

export const addPlace = placeName => {
    return {
        type: ADD_PLACE,
        placeName: placeName
    }
}

export const deletePlace = () => {
    return {
        type: DELETE_PLACE
    }
}

export const selectPlace = key => {
    return {
        type: SELECT_PLACE,
        placeKey: key
    }
}

export const deselectPlace = () => {
    return {
        type: DESELECT_PLACE
    }
}