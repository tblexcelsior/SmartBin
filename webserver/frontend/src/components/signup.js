import React from "react";
import { useState } from "react";
import './App.css'

export default function SignUp(){
    const [formData, setFormData] = useState(
        {"username": "", "password": "", "confirmed": "", email: ""}
    )
    function handleChange(event) {
        setFormData(prevFormData => {
            return {
                ...prevFormData,
                [event.target.name]: event.target.value
            }
        })
    }
    function handleSubmit(event){
        event.preventDefault()
        console.log(formData)
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
                    required = 'required'
                />
                <input 
                    type='password' 
                    placeholder="Password"
                    onChange={handleChange}
                    name='password'
                    value={formData.password}
                    className="app-form-submit-input"
                    required = 'required'
                />
                <input 
                    type='password' 
                    placeholder="Confirmed Password"
                    onChange={handleChange}
                    name='confirmed'
                    value={formData.confirmed}
                    className="app-form-submit-input"
                    required = 'required'
                />
                <input 
                    type='email' 
                    placeholder="Email"
                    onChange={handleChange}
                    name='email'
                    value={formData.email}
                    className="app-form-submit-input"
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