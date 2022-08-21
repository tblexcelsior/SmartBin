import './App.css';
import FormDiv from './form';
import { useState, useEffect, useRef } from 'react';
import Header from './Header';

function App() {
  const [showForm, setShowForm] = useState(false)
  const [signType, setSignType] = useState(true)
  function changeSignState(){
    setSignType(prevState => !prevState)
}
  // Outside click handle
  function useOutsideAlerter(ref) {
    useEffect(() => {
      /**
       * Alert if clicked on outside of element
       */
      function handleClickOutside(event) {
        if (ref.current && !ref.current.contains(event.target)) {
          setShowForm(false)
        }
      }
      // Bind the event listener
      document.addEventListener("mousedown", handleClickOutside);
      return () => {
        // Unbind the event listener on clean up
        document.removeEventListener("mousedown", handleClickOutside);
      };
    }, [ref]);
  }
  const wrapperRef = useRef(null);
  useOutsideAlerter(wrapperRef);

  return (
    <div className="App">
      {
        showForm
        ?   <div className="app-form-frame">
              <FormDiv wRef = {wrapperRef} type={signType} changeType={changeSignState}/>
            </div>
        :   <div className='app-main'>
              <Header showFormHandle={setShowForm} setTypeHandle={setSignType} />
            </div>
      }
    </div>
  );
}

export default App;
