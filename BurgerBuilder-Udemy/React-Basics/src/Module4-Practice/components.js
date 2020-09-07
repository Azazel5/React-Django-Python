import React from 'react'

export function ValidationComponent(props) {
    return (
        props.textLength !== 0 && <p>
            {props.textLength <= 5 ? 'Text too short': 'Text long enough'}
        </p>
    )
}

export function CharComponent(props) {
    const charStyle = {
        display: 'inline-block',
        padding: '16px', 
        textAlign: 'center', 
        margin: '16px', 
        border: '1px solid black'
    }

    return (
        <div onClick={props.onClick} style={charStyle}>
            <p>{props.letter}</p>
        </div>
    )
}