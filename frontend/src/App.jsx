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


  async function login() {

    const response = await fetch(
      "http://127.0.0.1:8000/login",
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


    if (!response.ok) {
      alert(
        "Invalid username or password"
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
      "http://127.0.0.1:8000/ask",
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