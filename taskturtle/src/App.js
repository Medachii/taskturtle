import { useState, useEffect } from 'react'
import axios from "axios";
import "./App.css";
import { Routes, Route, Link, BrowserRouter } from 'react-router-dom';
import Create from './components/Create';
import List from './components/List';
import Profile from './components/Profile';
import Login from './components/Login';
import Header from './components/Header';
import useToken from './components/useToken';


function App() {

  const [info, setInfo] = useState("")
  const [user, setUser] = useState(-1)
  const { token, removeToken, setToken } = useToken();
  function getInfo() {
    console.log("Je clique")
    axios({
      method: "GET",
      url: "http://localhost:5000/",
    })
      .then((response) => {
        console.log(response)
        setInfo(response.data)
      })
  }


  function changeUser(e) {
    e.preventDefault()
    const form = e.target;
    const formData = new FormData(form);
    //send the form to the server at the route /changeUser and get the response
    fetch("http://localhost:5000/changeUser", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((result) => {
        console.log(result);
        setUser(result.id);
      });
  }


  function disconnect() {
    fetch("http://localhost:5000/disconnect", { method: "POST" });
  }

  function handleSubmit(e) {
    // Prevent the browser from reloading the page
    e.preventDefault();
    // Read the form data
    const form = e.target;
    const formData = new FormData(form);
    const formJson = Object.fromEntries(formData.entries());
    console.log("FORMDATA");
    console.log(formData);
    console.log("FORMJSON");
    console.log(formJson);
    // You can pass formData as a fetch body directly:
    axios({
      method: "POST",
      url: "http://localhost:5000/createUser",
      data: formJson
    });
    window.location.reload();
  }



  useEffect(() => {
    getInfo()
  }, [])

  return (
    <BrowserRouter >
      <div className="App">

        <Header token={removeToken} />
        {!token && token !== "" && token !== undefined ?
          <Login setToken={setToken} />
          : (
            <>
              <Routes>
                <Route exact path="/profile" element={<Profile token={token} setToken={setToken} />}></Route>
                <Route path="/list" element={<List id={user} />} />
              </Routes>
            </>
          )}
        <Link to="/list" className="link">Liste des tâches</Link> <br></br>
        <Link to="/profile" className="link">Profil</Link>

        {!token && token !== "" && token !== undefined ?
        (
          <form method="post" onSubmit={handleSubmit}>
          <input type="text" name="email" placeholder="Adresse mail" />
          <input type="text" name="name" placeholder="Nom" />
          <input type="text" name="firstname" placeholder="Prénom" />
          <input type="password" name="password" placeholder="Mot de Passe" />
          <button type="submit">S'inscrire</button>
        </form>
        ) : <br></br>}
        


      </div>
    </BrowserRouter>
  );
}

export default App;
