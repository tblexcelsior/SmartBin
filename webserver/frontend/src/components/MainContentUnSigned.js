import React from "react";
import SubInfo from "./ContentSubInfo";
export default function MainContentUnSigned(){
    return(
        <div className="app-main-content">
            <div className="app-main-content-info-div">
                <h1 className="app-main-content-name1">SMART BIN</h1>
                <h1 className="app-main-content-name2">WASTE MANAGEMENT APPLICATION</h1>
            </div>
            <div className="app-main-content-subinfo-div">
                <SubInfo h1Text='About Us' h3Text='We are student from HCMC University of Technology and Education'/>
                <SubInfo h1Text='About Us' h3Text='We are student from HCMC University of Technology and Education'/>
            </div>
            <img src="./images/earth.png" className="app-main-content-img rotate" alt=""/>
        </div>
    )
}