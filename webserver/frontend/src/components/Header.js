import React from "react";
import { useState } from "react";
import './App.css'

export default function Header(props){
    return(
        <div className='app-main-bar' >
            <h1 className='app-header' onClick={() => window.location.reload()}>Smart Bin</h1>
            <div className='app-header-btn-div' onClick={() => props.showFormHandle(true)}>
                <div className='app-header-btn' onClick={() => props.setTypeHandle(true)}>Sign In</div>
                <div className='app-header-btn' id="sign-up" onClick={() => props.setTypeHandle(false)}>Sign Up</div>
            </div>
        </div>
    )
}