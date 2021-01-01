import React from "react";
import moment from "moment";
import EditIcon from "@material-ui/icons/Edit";
import DeleteForeverIcon from '@material-ui/icons/DeleteForever';
import DoneIcon from '@material-ui/icons/Done';
import {API} from "../apiService";
import { useCookies } from 'react-cookie';

function Tasklist(props) {

  const [token] = useCookies(["mr-token"]);

  const taskCompleted = (task) => (event) => {
    API.TaskComplete(task, token["mr-token"])
      .then((resp) => props.completeTask(resp))
      .catch((error) => console.log(error));
  };
  const taskDeleted = (task) => (event) => {
    API.TaskDelete(task, token["mr-token"])
      .then((resp) => props.deleteTask(resp))
      .catch((error) => console.log(error));
  };
  const taskEdited = (task) => (event)=> {
    props.editTask(task);
  };
  return (
    <React.Fragment>
      <center>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Progress</th>
              <th>Added On</th>
            </tr>
          </thead>
          <tbody>
            {props.tasks &&
              props.tasks.map((task, i) => {
                return (
                  <React.Fragment>
                    <tr key={i}>
                      <td>{task.name}</td>
                      <td>{task.desc}</td>
                      <td>
                        {task.completed ? (
                          <p onClick={taskDeleted(task)}><DeleteForeverIcon /></p>
                        ) : (
                          <p onClick={taskCompleted(task)}><DoneIcon /></p>
                        )}
                      </td>
                      <td>
                        {moment(task.timestamp).format("MM-DD-YYYY : hh:mm")}
                      </td>
                      <td>
                        <EditIcon onClick={taskEdited(task)} />
                      </td>
                    </tr>
                  </React.Fragment>
                );
              })}
          </tbody>
        </table>
      </center>
    </React.Fragment>
  );
}

export default Tasklist;
