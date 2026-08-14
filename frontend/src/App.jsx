import { useState } from "react";

import "./App.css";


function App() {

  const [loggedIn, setLoggedIn] =
    useState(false);

  const [username, setUsername] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [question, setQuestion] =
    useState("");

  const [answer, setAnswer] =
    useState("");

  const [groups, setGroups] =
    useState([]);

  const API_URL = import.meta.env.VITE_API_URL;
  
  async function login() {
    console.log("API_URL:", API_URL);
    console.log("Login URL:", `${API_URL}/login`);
    const response = await fetch(`${API_URL}/login`,
      {
        method: "POST",

        headers: {
          "Content-Type":
            "application/json"
        },

        body: JSON.stringify({
          username:
            username,
          password:
            password
        })
      }
    );

    console.log("Status:", response.status);
    const responseText = await response.text();
    console.log("Response:", responseText);

    if (!response.ok) {
      alert(
        `Login failed\nStatus: ${response.status}\nResponse: ${responseText}`
      );

      return;
    }


    const data =
      await response.json();
    setLoggedIn(true);
    setGroups(
      data.groups
    );
  }


  async function askQuestion() {
    if (!question.trim()) {
      return;
    }

    setAnswer(
      "Searching authorized documents..."
    );

    const response = await fetch(
      `${API_URL}/ask`,
      {
        method: "POST",
        headers: {
          "Content-Type":
            "application/json"
        },
        body: JSON.stringify({
          user_id:
            username,
          question:
            question
        })
      }
    );

    const data =
      await response.json();

    setAnswer(
      data.answer
    );
  }

  if (!loggedIn) {
    return (
      <div className="login">
        <h1>
          Secure RAG
        </h1>
        <input
          placeholder="Username"
          value={username}
          onChange={
            e =>
              setUsername(
                e.target.value
              )
          }
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={
            e =>
              setPassword(
                e.target.value
              )
          }
        />

        <button
          onClick={login}
        >
          Login
        </button>

      </div>
    );
  }


  return (
    <div className="container">
      <h1>
        Enterprise RAG Assistant
      </h1>
      <div className="user">
        Logged in as:
        <strong>
          {" "}{username}
        </strong>
        <br />
        Groups:
        <strong>
          {" "}
          {groups.join(", ")}
        </strong>
      </div>
      <textarea
        placeholder=
          "Ask your question..."

        value={question}
        onChange={
          e =>
            setQuestion(
              e.target.value
            )
        }

      />

      <button
        onClick={askQuestion}
      >
        Ask
      </button>
      <div className="answer">
        <h2>
          Answer
        </h2>
        <p>
          {answer}
        </p>

      </div>

    </div>
  );
}


export default App;