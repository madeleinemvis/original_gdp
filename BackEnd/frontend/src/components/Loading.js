import {Spinner} from "react-bootstrap";
import React from "react";

const Loading = () =>{
    return(
            <Spinner className="spinner" animation="border" role="status">
                <span className="sr-only">Loading...</span>
            </Spinner>
    );
}

export default Loading;