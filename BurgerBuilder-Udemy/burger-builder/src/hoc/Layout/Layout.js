import React, { Component } from 'react'
import Aux from '../Aux/Aux'
import classes from './Layout.module.css'
import Toolbar from '../../components/Navigation/Toolbar/Toolbar'
import SideDrawer from '../../components/Navigation/SideDrawer/SideDrawer'

import { connect } from 'react-redux'

class Layout extends Component {
    constructor(props) {
        super(props)
        this.state = {
            showSideDrawer: false
        }
    }

    sideDrawerClosedHandler = () => {
        this.setState({ showSideDrawer: false })
    }

    sideDrawerToggleHandler = () => {
        this.setState(prevState => {
            return { showSideDrawer: !prevState.showSideDrawer }
        })
    }

    render() {
        return (
            <Aux>
                <Toolbar
                    isAuthenticated={this.props.isAuthenticated}
                    drawerToggleClicked={this.sideDrawerToggleHandler} />
                <SideDrawer open={this.state.showSideDrawer} closed={this.sideDrawerClosedHandler}
                    isAuthenticated={this.props.isAuthenticated} />
                <main className={classes.Content}>{this.props.children}</main>
            </Aux>
        )
    }
}

const mapStateToProps = state => {
    return {
        isAuthenticated: state.auth.token !== null
    }
}

export default connect(mapStateToProps)(Layout)

/**
 * Hookified Layout.js
 * const layout = props => {
 *  const [showSideDrawer, setShowSideDrawer] = useState(false)
 *  sideDrawerClosedHandler = () => {
        setShowSideDrawer(false)
    }
 * sideDrawerToggleHandler = () => {
     setShowSideDrawer(!showSideDrawer)
 }

    return (
        <Aux>
            <Toolbar
                isAuthenticated={props.isAuthenticated}
                drawerToggleClicked={sideDrawerToggleHandler} />
            <SideDrawer open={showSideDrawer} closed={sideDrawerClosedHandler}
                isAuthenticated={props.isAuthenticated} />
            <main className={classes.Content}>{props.children}</main>
        </Aux>
    )
 */