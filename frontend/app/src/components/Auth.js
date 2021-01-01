import React, { useState, useEffect } from "react";
import { API } from "../apiService";
import { useCookies } from "react-cookie";

function Auth() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoginView, setisLoginView] = useState(true);

  const [token, setToken] = useCookies(["mr-token"]);

  useEffect(() => {
    console.log(token);
    if (token["mr-token"]) window.location.href = "/todos";
  }, [token]);

  const LoginClicked = () => {
    API.Login({ username, password })
      .then((resp) => setToken("mr-token", resp.token))
      .catch((error) => console.log(error));
  };
  const RegisterClicked = () => {
    API.Register({ username, password })
      .then(() => LoginClicked())
      .catch((error) => console.log(error));
  };

  return (
    <div className="App">
      <header className="App-header">
        {isLoginView ? <h1>Login</h1> : <h1>Register</h1>}
      </header>
      <div className="login-container">
        <label htmlFor="Username">Username</label>
        <br />
        <input
          id="Username"
          type="text"
          value={username}
          placeholder="Username"
          onChange={(event) => setUsername(event.target.value)}
        />
        <br />
        <label htmlFor="password">password</label>
        <br />
        <input
          id="password"
          type="password"
          value={password}
          placeholder="password"
          onChange={(event) => setPassword(event.target.value)}
        />
        <br />
        {isLoginView ? (
          <button onClick={LoginClicked}>Login</button>
        ) : (
          <button onClick={RegisterClicked}>Register</button>
        )}

        {isLoginView ? (
          <p onClick={() => setisLoginView(false)}>Create an account</p>
        ) : (
          <p onClick={() => setisLoginView(true)}>
            Sign in with existing account
          </p>
        )}
      </div>
    </div>
  );
}

export default Auth;
