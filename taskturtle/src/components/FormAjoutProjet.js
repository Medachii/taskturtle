import axios from "axios";

function FormAjoutProjet() {

  function handleSubmit(e) {
    // Prevent the browser from reloading the page
    e.preventDefault();

    // Read the form data
    const form = e.target;
    const formData = new FormData(form);
    const formJson = Object.fromEntries(formData.entries());
    // You can pass formData as a fetch body directly:
    axios({
      method: "POST",
      url: "http://localhost:5000/add",
      data: formJson,
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    });
    window.location.reload();
    console.log(formJson);
  }

  return (
    <div>
      <h2>Ajout d'une tâche</h2>
      <form method="post" onSubmit={handleSubmit}>
        <label>
          Nom : <input name="nom" placeholder="Nom du projet" />
        </label>
        <label>
          Description : <input name="desc" placeholder="Description du projet" />
        </label>
        <label>
          Prix : <input name="prix" placeholder="Prix" type="number" />
        </label>
        <button type="submit">Submit form</button>
      </form>
    </div>
  );
}

export default FormAjoutProjet;
