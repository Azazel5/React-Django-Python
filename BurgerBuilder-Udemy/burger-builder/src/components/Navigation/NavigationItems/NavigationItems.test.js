import React from 'react'
import {configure, shallow} from 'enzyme'
import Adapter from 'enzyme-adapter-react-16'
import NavigationItems from './NavigationItems'
import NavigationItem from './NavigationItem/NavigationItem'

configure({adapter: new Adapter()})

/**
 * A test uses the describe function which takes a string labelling the test with a function. 
 * Inside the function, an it function is run which takes a string which describes the test and 
 * a function with the logic of the test. Enzyme allows us to render standalone components such 
 * that we don't need the entire app. Shallow is the best way to render most components, although 
 * enzyme does offer others. 
 * Note - Pass JSX to the shallow function.
 * Use the expect function to find things. There is a variety of methods available to make testing 
 * easy. 
 */
describe('<NavigationItems />', () => {
    // BeforeEach is similar to setUp in the Django tests (there's also an afterEach)
    let wrapper;
    beforeEach(() => {
        wrapper = shallow(<NavigationItems />)
    })

    it('should render two <NavigationItems /> elements if not authenticated', () => {
        expect(wrapper.find(NavigationItem)).toHaveLength(2)
    })

    // Passing props is done as normal in tests as well. However, you can pass props in a different
    // manner as well if using a beforeEach i.e. the setProps method.
    it('should render three <NavigationItems /> elements if authenticated', () => {
        wrapper.setProps({isAuthenticated: true})
        expect(wrapper.find(NavigationItem)).toHaveLength(3)
    })
    
    // The isAuthenticated prop is necessary as the tests run independent of each other and adequate 
    // setting of the prerequisites is mandatory.
    it('should render <NavigationItem>Logout<NavigationItem> if authenticated', () => {
        wrapper.setProps({isAuthenticated: true})
        expect(wrapper.contains(<NavigationItem link="/logout">Logout</NavigationItem>)).toEqual(true)
    })
})