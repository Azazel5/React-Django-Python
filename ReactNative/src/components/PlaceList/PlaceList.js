import React, { useState } from 'react'
import { StyleSheet, FlatList } from 'react-native'

import ListItem from '../LisItem/ListItem'


const PlaceList = props => {
    return (
        <FlatList
            data={props.places}
            style={styles.listContainer}
            renderItem={({ item }) => (
                <ListItem
                    placeName={item.name}
                    placeImage={item.image}
                    onItemPressed={() => props.onItemSelected(item.key)} />
            )}
            keyExtractor={item => item.key.toString()}
        />
    )
}

const styles = StyleSheet.create({
    listContainer: {
        width: '100%'
    }
});

export default PlaceList