import { useEffect, useState, useRef } from "react";
import axios from "axios";

function Profile(props) {
  const [profileData, setProfileData] = useState(null);
  const noteRef = useRef(null);
  const [note, setNote] = useState(0);
  const [idSuppr, setIdSuppr] = useState(-1);

  function getData() {
    axios({
      method: "GET",
      url: "/profile",
      headers: {
        Authorization: "Bearer " + props.token,
      },
    })
      .then((response) => {
        const res = response.data;
        res.access_token && props.setToken(res.access_token);
        setProfileData({
          profile_name: res.name,
          acceptedtasks: res.acceptedtasks,
          createdtasks: res.createdtasks
        });
        console.log("C'EST LE PROFIL");
        console.log(profileData.acceptedtasks);
        console.log(profileData.createdtasks);
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
  }

  useEffect(() => {
    getData();
  }, []);

  const handleChange = (event) => {
    setNote(event.target.value);
  };

  function cancelTask(id_trans){
    console.log("ID_TRANS : " + id_trans);
    axios({
      method: "POST",
      url: "http://localhost:5000/cancel",
      data: {
        id: id_trans,
      },
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      }
    });
  };

  function evalClick(id_trans) {
    console.log("On note le projet :" + id_trans);
    setNote(noteRef.current.value);
    axios({
      method: "POST",
      url: "/noter",
      data: {
        note: note,
        transaction: id_trans,
      },
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    });
    getData();
  }

  function finalClick(id_trans) {
    console.log("On finalise le projet :" + id_trans);
    axios({
      method: "POST",
      url: "/finalise",
      data: {
        transaction: id_trans,
      },
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    });
    getData();
  }

  return (
    <div className="Profile">
      {profileData && (
        <div>
          <h1>Profile name: {profileData.profile_name}</h1>
          <h2>Tâches acceptées : </h2>

          <div>

            {profileData.acceptedTasks === [] ? <p>Vous n'avez pas accepté de projets</p> : (
              <table>
              <thead>
                <tr>
                  <th>Nom du projet</th>
                  <th>Description du projet</th>
                  <th>Auteur</th>
                  <th>Prix</th>
                  <th>Etat</th>
                </tr>
              </thead>
              <tbody>
                {profileData.acceptedtasks.map((projet) => (
                  <tr key={projet[0]}>
                    <td>{projet[1]}</td>
                    <td>{projet[2]}</td>
                    <td>
                      {projet[4]} {projet[3]}
                    </td>
                    <td> {projet[6]} wei</td>
                    <td>
                      {(projet[7] === 1 && projet[8] === 0)? (<p>Accepté</p>) : (projet[7] === 1 && projet[8] === 1) ? (<p>Finalisé</p>) : (projet[7] === 0 && projet[8] === 0) ? (<p>En attente</p>) : (<p>Annulé</p>)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            )}

            
          </div>

          <h2>Tâches publiées : </h2>
          <div>

            {profileData.createdtasks === [] ? <p>Vous n'avez pas de projet en attente</p> : (
              <table>
              <thead>
                <tr>
                  <th>Nom du projet</th>
                  <th>Description du projet</th>
                  <th>Prix</th>
                  <th>Annuler</th>
                  <th>Note</th>
                  <th>Évaluer</th>
                  <th>Finaliser</th>
                  <th>Etat</th>
                </tr>
              </thead>
              <tbody>
                {profileData.createdtasks.map((projet) => (
                  <tr key={projet[5]}>
                    <td>{projet[0]}</td>
                    <td>{projet[1]}</td>
                    <td>{projet[4]}</td>
                    <td>
                      <button onClick={() => cancelTask(projet[5])}>
                        Annuler
                      </button>
                    </td>
                    {projet[6] === 0 ? (
                      <td>Non noté</td>
                    ) : (
                      <td>{projet[6]}/5</td>
                    )}

                    <td>
                      <input
                        type="number"
                        id="message"
                        name="message"
                        ref={noteRef}
                        min="1"
                        max="5"
                        onChange={handleChange}
                      />
                      <button onClick={() => evalClick(projet[5])}>
                        Évaluer
                      </button>
                    </td>
                    <td>
                      <button onClick={() => finalClick(projet[5])}>
                        Finaliser
                      </button>
                    </td>
                    <td>
                      {(projet[7] === 1 && projet[8] === 0)? (<p>Accepté</p>) : (projet[7] === 1 && projet[8] === 1) ? (<p>Finalisé</p>) : (projet[7] === 0 && projet[8] === 0) ? (<p>En attente</p>) : (<p>Annulé</p>)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default Profile;
