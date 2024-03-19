import { useState, useEffect } from "react";
import axios from "axios";
import FormAjoutProjet from "./FormAjoutProjet.js"
import "../App.css";
import "../List.css"

function List() {
  //data is a list of json objects
  const [profileData, setProfileData] = useState([]);

  function getData() {
    axios({
      method: "GET",
      url: "http://localhost:5000/list",
    })
      .then((response) => {
        const res = response.data;
        console.log(res);
        setProfileData(res);
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
  }

  function reservation(id){
    console.log("On va dans reservation :" + id)
    axios({
      method: "POST",
      url: "http://localhost:5000/reservation",
      data: {
        id: id
      },
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token")
      }});
      window.location.reload();
  }

  useEffect(() => {
    
    getData();
  }, []);

  return (
    <div>
      <h1>Task List</h1>
      {profileData.length && (
        <div>
          <table>
            <thead>
              <tr>
                <th>Nom</th>
                <th>Auteur</th>
                <th>Description</th>
                <th>Prix</th>
                <th>Note</th>
                <th>Réservation</th>
              </tr>
            </thead>
            <tbody>
              {profileData.map((task) => (
                <tr key={task.id}>
                  <td>{task.name}</td>
                  <td>{task.auteur}</td>
                  <td>{task.description}</td>
                  <td>{task.prix} wei</td>
                  {task.note === 0 ? <td>Non noté</td> : <td>{task.note}/5</td>}
                  <td> <button className="button" onClick={() => reservation(task.id)}>Accepter</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    <FormAjoutProjet/>
    </div>
  );
}

export default List;
