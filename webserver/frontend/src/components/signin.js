import React from "react";
import { useState } from "react";
import './App.css'
import axios from "axios";

export default function SignIn(){
    const [formData, setFormData] = useState(
        {"username": "", "password": ""}
    )
    function handleChange(event) {
        setFormData(prevFormData => {
            return {
                ...prevFormData,
                [event.target.name]: event.target.value
            }
        })
    }
    async function handleSubmit(event){
        event.preventDefault()
        let res = await axios({
            method: 'post',
            url: 'http://localhost:4000/signin',
            data: formData
        })
        console.log(res)
    }
    return(
            <form onSubmit={handleSubmit} className="app-form-main">
                <input 
                    type='text' 
                    placeholder="User Name"
                    onChange={handleChange}
                    name='username'
                    value={formData.username}
                    className="app-form-submit-input"
                    autoComplete="off"
                    required = 'required'
                />
                <input 
                    type='password' 
                    placeholder="Password"
                    onChange={handleChange}
                    name='password'
                    value={formData.password}
                    className="app-form-submit-input"
                    autoComplete="off"
                    required = 'required'
                />
                <input 
                    type='submit'
                    className="app-form-submit-btn"
                    value= 'Sign Up'
                />
            </form>
    )
}