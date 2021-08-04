import React, { useState } from 'react'
import { StyleSheet, View } from 'react-native'

import ListItem from '../LisItem/ListItem'


const PlaceList = props => {
    const placesOutput = props.places.map((place, index) => (
        <ListItem key={index} placeName={place} />
    ))

    return (
        <View style={styles.listContainer}>{placesOutput}</View>
    )
}

const styles = StyleSheet.create({
    listContainer: {
        width: '100%'
    }
});

export default PlaceList