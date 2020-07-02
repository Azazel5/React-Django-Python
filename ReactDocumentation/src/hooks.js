import { useState, useEffect } from "react"

export const example = (props) => {
    const [count, setCount] = useState(0)
    return (
        <div>
            <p>You clicked {count} times!</p>
            <button onClick={() => setCount(count + 1)}>Click me</button>
        </div>
    )
}

/**
 * This small example demonstrates the useState hook. The hook returns the state value and a 
 * setter function. Again, hooks don't replace state values like this.setState did. 
 * Data-fetching, subscriptions, or manually changing the DOM, etc are called side-effects, which 
 * are handled by the useEffect hook. 
 */

// You can also perform cleanups in useEffect
export function CleanupExample(props) {
    const [isOnline, setIsOnline] = useState(null)

    useEffect(() => {
        Api.subscribeToFriendStatus()
        return () => {
            Api.unsubscribeFromFriendStatus()
        }
    })
}

/**
 * What if you want to share state-ful logic across components? You can write your own
 * custom hooks for that. Bye bye render props and HOCs. 
 * Since states are completely independent in hooks, it allows perfect reusability. 
 * Other hooks include useContext, useRef, useReducer, etc. 
 * By default, useEffect runs after each render. If your effect returns a function, React will run
 * it when it is time to clean up.
 * 
 * ----------------------------
 * Tips for using effects/hooks
 * ----------------------------
 * 
 * 1. Use multiple effects to seperate concerns. React will apply every effect in order of specification.
 * The most important takeaway: hooks let us split code by what they're doing instead of lifecycle
 * methods. 
 * 2. Why does useEffect clean itself up after every render? What happens if you use lifecycle hooks and 
 * only do cleanup on unmount? If the prop changes while the component is mounted, the component 
 * renders again without unsubscribing, which is a blatant memory leak. You'd have to use 
 * componentDidUpdate to determine things again. useEffect handles this by default.
 * 3. You can skip effects if you want to focus on performance optimizations (class-based components
 * did this via componentDidUpdate). This is done by the dependency array. Adding a value to it
 * tells react to only re-render if that value has changed. 
 * 4. Passing an empty dependency array will only run the effect onMount and onUnmount.
 * 5. If you want to call an effect conditionally, make sure the con dition is inside the hook. 
 */

// Custom hooks 

/**
 * If you want a component which tells you whether a friend is online or not, and you also 
 * want a contactList which will show if the friends are online, you see the clear similarity
 * between them. Hooks provide an elegant solution to this common problem: outsource this 
 * commonality into a custom hook and use it in both components. Since the state will be 
 * independent in each, it's a beautiful solution.
 */

function useFriendStatus(friendId) {
    const [isOnline, setIsOnline] = useState(null)
    useEffect(() => {
        function handleStatusChange(status) {
            setIsOnline(status.isOnline)
        }

        ChatAPI.subscribeToFriendStatus(friendID, handleStatusChange);
        return () => {
          ChatAPI.unsubscribeFromFriendStatus(friendID, handleStatusChange);
        };
    })

    return isOnline
}

// Now you can simply use this hook in the two components

export function FriendStatus(props) {
    const isOnline = useFriendStatus(props.friends.id)
    if(!isOnline) {
        return 'Loading...'
    }

    return isOnline ? 'Online': 'Offline'
}

export function FriendList(props) {
    const isOnline = useFriendStatus(props.friend.id)
    return (
        <li style={{color: isOnline ? 'green': 'black'}}>
            {props.friend.name}
        </li>
    )
}

/**
 *  Passing information between hooks is simple. Just call one hook and pass its variable to
 * the next hook, as you would pass arguments to normal functions. 
 * A little tip from the documentation: don't try to go for abstractions early. Find something 
 * you're doing a lot more than you'd like to and turn that into a custom hook.
 */