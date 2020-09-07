import React, { useState, useEffect, useRef } from 'react';

import Card from '../UI/Card';
import './Search.css';
import useHttp from '../../hooks/http'
import ErrorModal from '../UI/ErrorModal'

/**
 * If you need to use props inside useEffect, you can. However, don't pass props as a dependecy as 
 * that effect will run whenever ANY props is passed to the component. Instead, use array destructuring
 * to get that prop out of props and pass that as a dependency. 
 */
const Search = React.memo(props => {
  const [enteredFilter, setEnteredFilter] = useState('')
  const { onLoadIngredients } = props
  const inputRef = useRef()
  const { loading, error, data, sendRequest, clear } = useHttp()

  /**
   * In JS closures, the enteredFilter value inside the setTimeout anonymous function will be locked in 
   * and doesn't change. Be wary with side-effects in useEffect as it creates reapeated resources on 
   * re-renders. Example - if you create a timer in the useEffect, you might create multiple timers
   * on multiple render cycles. So remember to cleanup after you're done!
   * Remember, the cleanup is done only if the dependencies change here.
   * Using one effect for request and one for response. We have a loading prop which we can use 
   * in the second effect. 
   */
  useEffect(() => {
    const timer = setTimeout(() => {
      if (enteredFilter === inputRef.current.value) {
        const query =
          enteredFilter.length === 0
            ? ''
            : `?orderBy="title"&equalTo="${enteredFilter}"`;
        sendRequest(
          'https://react-hooks-c1405.firebaseio.com/ingredients.json' + query,
          'GET'
        );
      }
    }, 500);
    return () => {
      clearTimeout(timer);
    };
  }, [enteredFilter, inputRef, sendRequest]);

  useEffect(() => {
    if (!loading && !error && data) {
      const loadedIngredients = [];
      for (const key in data) {
        loadedIngredients.push({
          id: key,
          title: data[key].title,
          amount: data[key].amount
        });
      }
      onLoadIngredients(loadedIngredients);
    }
  }, [data, loading, error, onLoadIngredients]);
  
  return (
    <section className="search">
      {error && <ErrorModal onClose={clear}>{error}</ErrorModal>}
      <Card>
        <div className="search-input">
          <label>Filter by Title</label>
          {loading && <span>Loading...</span>}
          <input
            ref={inputRef}
            type="text"
            onChange={(event) => setEnteredFilter(event.target.value)} />
        </div>
      </Card>
    </section>
  );
});

export default Search;
