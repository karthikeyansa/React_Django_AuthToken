import React, { useState, useEffect } from "react";
import { API } from "../apiService";
import { useCookies } from "react-cookie";

function Addtask(props) {
  const [name, setName] = useState("");
  const [desc, setDesc] = useState("");

  const [token] = useCookies(["mr-token"]);

  useEffect(() => {
    setName(props.task.name);
    setDesc(props.task.desc);
  }, [props.task]);

  const addedNewtask = () => {
    API.TaskAdd({ name: name, desc: desc }, token["mr-token"])
      .then((resp) => props.addTask(resp))
      .catch((error) => console.log(error));
  };

  const editedTask = () => {
    API.TaskEdit(props.task, { name: name, desc: desc }, token["mr-token"])
      .then((resp) => props.updatedTask(resp))
      .catch((error) => console.log(error));
  };

  return (
    <React.Fragment>
      <form>
        Name
        <input
          id="name"
          type="text"
          value={name}
          onChange={(event) => setName(event.target.value)}
        />
        Description
        <input
          id="desc"
          type="text"
          value={desc}
          onChange={(event) => setDesc(event.target.value)}
        />
        {props.task.id ? (
          <button onClick={editedTask}>Update Task</button>
        ) : (
          <button onClick={addedNewtask}>Add Task</button>
        )}
      </form>
    </React.Fragment>
  );
}

export default Addtask;
