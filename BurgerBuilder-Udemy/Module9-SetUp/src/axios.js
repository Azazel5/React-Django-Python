import axios from 'axios'

/**
  * In the case where you want things to be shared in between some places but not all like shown in
  * the index.js defaults section
  */

const instance = axios.create({
    baseURL: 'https://jsonplaceholder.typicode.com'
})

instance.defaults.headers.common['Authorization'] = 'Axios instance overwrites'

export default instance 
