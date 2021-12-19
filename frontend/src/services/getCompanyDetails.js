import axios from 'axios';

const api = axios.create({
    baseURL:'http://localhost:8000'
});

let getCompanyDetails = async (companyName) => {
    console.log('Reached')
    let res = await api.post('/get-company-details', {
        headers:{
            'Content-Type': 'application/json'
        },
        'company-name':companyName
    })
    return res;
}

export default getCompanyDetails;