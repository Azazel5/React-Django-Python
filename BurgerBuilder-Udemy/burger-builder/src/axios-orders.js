import axios from 'axios'

const axe = axios.create({
    baseURL: "https://react-burger-f8573.firebaseio.com/"
})

export default axe 