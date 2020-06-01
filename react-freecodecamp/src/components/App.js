import React from 'react'
import {Header} from './Header'
import {MemeGenerator} from './MemeGenerator'

// A class based component which simply renders other child components 
export class App extends React.Component {
    render() {
        return (
            <div>
                <Header />
                <MemeGenerator />
            </div>
        )
    }
}