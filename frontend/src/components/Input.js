import getCompanyDetails from '../services/getCompanyDetails'
import {Link} from 'react-router-dom'

function Input({setData}) {

    const handleSubmit = async (e) => {
      e.preventDefault();
      let companyName = document.getElementById('company-name').value;
      if(companyName === '') {
        console.log('Please enter company name');
        return;
      }
      let response = await getCompanyDetails(companyName);
      console.log(response.data)
      setData(response.data)
    }

    return (
        <div>
            <form className='flex-vertical' onSubmit={handleSubmit} >
                <input type='text' name='company-name' id='company-name' placeholder='Please enter company name' className='form-input' />
                <input type='submit' value='Submit' className='form-input' />
            </form>
            <Link to='/output'>See Output</Link>
        </div>
    )
}

export default Input