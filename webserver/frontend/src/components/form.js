import React from "react";
import { useState } from "react";
import './App.css'
import SignIn from "./signin";
import SignUp from "./signup";


export default function FormDiv(props){
    const [signType, setSignType] = useState(true)


    
    return(
        <div className="app-form-div" ref={props.wRef} >   
            <div className="app-form-header"> {
                props.type
                ?   <h1>Sign In</h1>
                :   <h1>Sign Up</h1>
            } </div>
            <div className="app-form-switch" onClick={props.changeType}>
                {
                props.type
                    ?<div className="app-form-switch-state">Sign In</div>
                    :<div className="app-form-switch-state" id='check'><p>Sign Up</p></div>
                }
            </div>
            {
            props.type 
                ?   <SignIn />
                :   <SignUp />
            }
            
        </div>
    )
}