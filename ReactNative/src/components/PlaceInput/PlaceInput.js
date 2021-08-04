import React, { useState } from 'react'
import { StyleSheet, View, Button, TextInput } from 'react-native'

const PlaceInput = props => {
    const [placeName, setPlaceName] = useState('')
    const { onPlaceAdded } = props

    const placeNameChangedHandler = event => {
        setPlaceName(event)
    }

    const placeSubmitHandler = () => {
        if (placeName.trim() === "")
            return

        onPlaceAdded(placeName)
        setPlaceName('')
    }

    return (
        <View style={styles.inputContainer}>
            <TextInput
                placeholder="An awesome place"
                value={placeName}
                onChangeText={placeNameChangedHandler}
                style={styles.placeInput}
            />

            <Button
                title="Add" style={styles.placeButton}
                onPress={placeSubmitHandler} />
        </View>
    )
}

const styles = StyleSheet.create({
    inputContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        width: '100%'
    },

    placeInput: {
        width: "70%"
    },

    placeButton: {
        width: "30%"
    },
})

export default PlaceInput