import React from 'react'
import { Modal, View, Image, Text, Button, StyleSheet } from 'react-native'

const PlaceDetail = props => {
    const { selectedPlace, onItemDeleted, onModalClose } = props
    let modalContent = null

    if (selectedPlace) {
        modalContent = (
            <>
                <Image source={selectedPlace.image} style={styles.placeImage} />
                <Text style={styles.placeName}>{selectedPlace.name}</Text>
            </>
        )
    }

    return (
        <Modal
            onRequestClose={onModalClose}
            visible={selectedPlace !== null}
            animationType="slide">

            <View style={styles.modalContainer}>
                {modalContent}
                <View>
                    <Button title="Delete" color="red" onPress={onItemDeleted} />
                    <Button title="Close" onPress={onModalClose} />
                </View>
            </View>
        </Modal>
    )
}

const styles = StyleSheet.create({
    modalContainer: {
        margin: 22
    },

    placeImage: {
        width: "100%",
        height: 200
    },

    placeName: {
        fontWeight: 'bold',
        textAlign: 'center',
        fontSize: 28
    }
})

export default PlaceDetail