import http from "../http-common";
// https://bezkoder.com/react-hooks-crud-axios-api/

const getAll = collection => {
    return http.get(`/${collection}`)
}

export default {
    getAll
}