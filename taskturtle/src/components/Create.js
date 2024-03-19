import { useState, useEffect } from 'react'
import axios from "axios";
import "../App.css";

function Create(){
    const [data, setData] = useState("");
    function getInfo() {
        console.log("Je clique")
        axios({
          method: "GET",
          url: "http://localhost:5000/create",
        })
        .then((response) => {
          console.log(response)
          setData(response.data)
        })
      }

      useEffect(() => {
        getInfo();
        }, []);


    return(
        <div>
            <h1>Page Create</h1>
            <p>{data.name}</p>
        </div>
    )
            
}

export default Create;