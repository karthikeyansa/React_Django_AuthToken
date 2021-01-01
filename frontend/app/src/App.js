import "./App.css";
import React, { useState, useEffect } from "react";
import Tasklist from "./components/Tasklist";
import Addtask from "./components/Addtask";
import {API} from './apiService';
import { useCookies } from "react-cookie";


function App() {
  const [tasks, setTasks] = useState([]);
  const [editTask, setEdittask] = useState(null);

  const [token, setToken, deleteToken] = useCookies(["mr-token"]);
  
  useEffect(() => {
    API.GetTasks(token["mr-token"])
      .then((resp) => setTasks(resp))
      .catch((error) => console.log(error));
  }, []);

  useEffect(() => {
    if (!token["mr-token"]) window.location.href = "/";
  }, [token]);

  /*Logout */
  const logout = () => {
    deleteToken(["mr-token"]);
  };

  /* tasklist */
  const Completetask = (tasks) => {
    setTasks(tasks);
  };
  const Deletetask = (tasks) => {
    setTasks(tasks);
  };
   /* addtask */
  const newtaskform = () => {
    setEdittask({ name: "", desc: "" });
  };
  const EditTask = (task) => {
    setEdittask(task);

  };
  const Newtask = (task) => {
    const newtask = [...tasks, task];
    setTasks(newtask);
  };
  const UpdatedEditedTask = (tasks)=>{
    setTasks(tasks);
  }

  return (
    <div className="App">
      <button onClick={logout}>Logout</button>
      <Tasklist
        tasks={tasks}
        completeTask={Completetask}
        deleteTask={Deletetask}
        editTask={EditTask}
      />
      {editTask ? (
        <Addtask
          task={editTask}
          addTask={Newtask}
          updatedTask={UpdatedEditedTask}
        />
      ) : (
        <button onClick={newtaskform}>AddTask</button>
      )}
    </div>
  );
}

export default App;
