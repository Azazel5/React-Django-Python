import { StatusBar } from 'expo-status-bar';
import React, { useState } from 'react';
import { StyleSheet, View } from 'react-native';
import { Provider } from 'react-redux'
import { connect } from 'react-redux'

import PlaceInput from './src/components/PlaceInput/PlaceInput';
import PlaceList from './src/components/PlaceList/PlaceList';
import PlaceDetail from './src/components/PlaceDetail/PlaceDetail';
import configureStore from './src/store/configureStore';
import { addPlace, deletePlace, selectPlace, deselectPlace } from './src/store/actions'

const App = props => {
    const placeSubmitHandler = place => {
        props.onAddPlace(place)
    }

    const placeSelectedHandler = key => {
        props.onSelectPlace(key)
    }

    const placeDeletedHandler = () => {
        props.onDeletePlace()
    }

    const modalClosedHandler = () => {
        props.onDeselectPlace()
    }

    return (
        <Provider store={configureStore()}>
            <View style={styles.container}>
                <PlaceDetail
                    selectedPlace={selectedPlace}
                    onItemDeleted={placeDeletedHandler}
                    onModalClose={modalClosedHandler} />
                <PlaceInput onPlaceAdded={placeSubmitHandler} />
                <PlaceList places={places} onItemSelected={placeSelectedHandler} />
            </View>
        </Provider>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'flex-start',
        padding: 36
    }
});

// Anytime you want a component to map redux state to props
const mapStateToProps = state => {
    return {
        places: state.places.places,
        selectedPlace: state.places.selectedPlace
    }
}

const mapDispatchToProps = dispatch => {
    return {
        onAddPlace: (name) => dispatch(addPlace(name)),
        onDeletePlace: () => dispatch(deletePlace()),
        onSelectPlace: (key) => dispatch(selectPlace(key)),
        onDeselectPlace: () => dispatch(deselectPlace)
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(App)