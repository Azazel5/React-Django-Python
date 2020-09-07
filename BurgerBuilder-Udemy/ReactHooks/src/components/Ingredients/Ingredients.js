import React, { useReducer, useCallback, useMemo, useEffect } from 'react';

import IngredientForm from './IngredientForm';
import IngredientList from './IngredientList'
import Search from './Search';
import ErrorModal from '../UI/ErrorModal'
import useHttp from '../../hooks/http'

/**
 * The logic of useReducer is similar to the redux reducers even though it shares nothing with redux i.e.
 * Handle each action type and dispatch actions with payloads. 
 * You can put your reducer inside the component if you need to use props inside; however, try to 
 * put it outside to avoid unnecessary re-renders. 
 */
const ingredientReducer = (currentIngredients, action) => {
  switch (action.type) {
    case 'SET':
      return action.ingredients
    case 'ADD':
      return [
        ...currentIngredients,
        action.ingredient
      ]
    case 'DELETE':
      return currentIngredients.filter(ing => ing.id !== action.id)
    default:
      throw new Error("Shouldn't get here")
  }
}

/**
 * The useEffect hook runs AFTER every render cycle of the component. Used without the dependency 
 * array, useEffect runs like componentDidUpdate. If the dependency array changes, the useEffect
 * re-runs. If you need to use variables/functions which are defined outside the useEffect, they 
 * must be defined in the dependency array (hook variables are exceptions). 
 * With an empty array, useEffect simulates componentDidMount.
 * These states are currently being managed independently; however, we can see that they're related.
 * If what you want is interdependence, use the useReducer hook. 
 * The hook takes a second argument, which is the initial state.
 */
function Ingredients() {
  const [ingredients, dispatch] = useReducer(ingredientReducer, [])
  const { 
    loading, error, data,
    sendRequest, reqExtra, identifier, clear 
  } = useHttp()

  /**
   * When we run the sendRequest method (defined in the custom hook), we want to update the UI.
   * Hence, we can use an effect to listen for this. By adding data to the dependency array,
   * we ensure that this component re-renders when the request is successful and data changes.
   */
  useEffect(() => {
    if (!loading && !error && identifier === 'REMOVE_INGREDIENT') {
      dispatch({ type: 'DELETE', id: reqExtra })
    } else if(!loading && !error && identifier === 'ADD_INGREDIENT') {
      dispatch({
        type: 'ADD',
        ingredient: {
          id: data.name,
          ...reqExtra
        }
      })
    }
  }, [data, reqExtra, identifier, loading, error])

  // In JS whenever this component reloads, functions and variables are created anew, so be wary
  // of this behavior while using dependency arrays in useEffect. You can use useCallback for this.
  const filteredIngredientsHandler = useCallback(ingredient => {
    dispatch({
      type: 'SET',
      ingredients: ingredient
    })
  }, [])

  const addIngredientHandler = useCallback(ingredient => {
    sendRequest(
      'https://react-hooks-c1405.firebaseio.com/ingredients.json',
      'POST',
      JSON.stringify(ingredient),
      ingredient,
      'ADD_INGREDIENT'
    )
  }, [sendRequest])

  const removeIngredientHandler = useCallback(ingredientId => {
    sendRequest(
      `https://react-hooks-c1405.firebaseio.com/ingredients/${ingredientId}.json`,
      'DELETE',
      null,
      ingredientId, 
      'REMOVE_INGREDIENT'
    )
  }, [sendRequest])

  const ingredientList = useMemo(() => {
    return <IngredientList ingredients={ingredients} onRemoveItem={removeIngredientHandler} />
  }, [ingredients, removeIngredientHandler])

  // No need to call this.addIngredientHandler as we are using functions not classes.
  return (
    <div className="App">
      {error && <ErrorModal onClose={clear}>{error}</ErrorModal>}
      <IngredientForm onAddIngredient={addIngredientHandler} isLoading={loading} />
      <section>
        <Search onLoadIngredients={filteredIngredientsHandler} />
        {ingredientList}
      </section>
    </div>
  );
}

export default Ingredients;
