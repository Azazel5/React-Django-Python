import { StatusBar } from 'expo-status-bar';
import React, { useState } from 'react';
import { StyleSheet, View } from 'react-native';

import PlaceInput from './src/components/PlaceInput/PlaceInput';
import PlaceList from './src/components/PlaceList/PlaceList';

export default function App() {
    const [places, setPlaces] = useState([])

    const placeSubmitHandler = place => {
        setPlaces(prevPlace => prevPlace.concat(place))
    }

    return (
        <View style={styles.container}>
            <PlaceInput onPlaceAdded={placeSubmitHandler} />
            <PlaceList places={places} />
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
