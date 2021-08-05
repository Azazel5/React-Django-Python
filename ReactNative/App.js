import { StatusBar } from 'expo-status-bar';
import React, { useState } from 'react';
import { StyleSheet, View } from 'react-native';

import PlaceInput from './src/components/PlaceInput/PlaceInput';
import PlaceList from './src/components/PlaceList/PlaceList';
import PlaceDetail from './src/components/PlaceDetail/PlaceDetail';

export default function App() {
    const [places, setPlaces] = useState([])
    const [selectedPlace, setSelectedPlace] = useState(null)

    const placeSubmitHandler = place => {
        setPlaces(prevPlace => prevPlace.concat(
            {
                key: Math.random(),
                name: place,
                image: {
                    uri: "https://pbs.twimg.com/media/ExigaJFWgAQt48E?format=jpg&name=medium"
                }
            }
        ))
    }

    const placeSelectedHandler = key => {
        setSelectedPlace(places.find(place => place.key === key))
    }

    const placeDeletedHandler = ()  => {
        setPlaces(prevPlace => prevPlace.filter(place => place.key !== selectedPlace.key))
        modalClosedHandler()
    }

    const modalClosedHandler = ()  => {
        setSelectedPlace(null)
    }

    return (
        <View style={styles.container}>
            <PlaceDetail 
                selectedPlace={selectedPlace}
                onItemDeleted={placeDeletedHandler}
                onModalClose={modalClosedHandler} />
            <PlaceInput onPlaceAdded={placeSubmitHandler} />
            <PlaceList places={places} onItemSelected={placeSelectedHandler} />
        </View>
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
