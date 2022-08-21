import React from "react";

export default function SubInfo(props){
    return(
        <div className="app-content-subinfo">
            <h1>{props.h1Text}</h1>
            <h3 className="">{props.h3Text}</h3>
        </div>
    )

}