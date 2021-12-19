import './App.css';
import React, {useState} from 'react'
import Input from './components/Input'
import Output from './components/Output'
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom'

function App() {

  const [data, setData] = useState({})

  return (
    <div id="App" className="App">
        <h1 className='heading'>Theme Extracting Utility</h1>
        <Router>
          <Routes>
            <Route exact path="/" element={<Input setData={setData} />} />
            <Route exact path="/output" element={<Output data={data} />} />
          </Routes>
        </Router>
    </div>
  );
}

export default App;
