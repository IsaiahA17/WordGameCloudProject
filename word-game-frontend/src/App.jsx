import { useState } from "react";
import "./App.css";

const API_BASE = import.meta.env.VITE_API_URL;

export default function App() {
  const [screen, setScreen] = useState("rules");
  const [sourceWord, setSourceWord] = useState("");
  const [attempt, setAttempt] = useState("");
  const [result, setResult] = useState("");
  const [win, setWin] = useState(false);
  const [username, setUsername] = useState("");
  const [highScores, setHighScores] = useState([]);
  const [startTime, setStartTime] = useState(null);
  const [attemptTime, setAttemptTime] = useState(null);

const startGame = async () => {
    const res = await fetch(`${API_BASE}/input`, { method: "POST" });
    const data = await res.json();
    setSourceWord(data.sourceWord);
    setStartTime(data.startTime);
    setScreen("game");
};

const submitAttempt = async () => {
    const res = await fetch(`${API_BASE}/process_pattern`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ attempt, startTime, sourceWord })
    });
    const data = await res.json();
    setResult(data.result);
    setWin(data.win);
    setAttemptTime(data.attemptTime);
    setScreen("end");
};

const submitDetails = async () => {
    await fetch(`${API_BASE}/enter_details`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            username,
            sourceWord,
            win,
            attempt,
            attemptTime
        })
    });
    setScreen("rules");
};

  const showLeaderboard = async () => {
    const res = await fetch(`${API_BASE}/top10`);
    const data = await res.json();
    setHighScores(data);
    setScreen("leaderboard");
  };

  return (
    <div>
      <div>
        <ul className="menu">
          <li className="navbar" onClick={() => setScreen("rules")}>Rules</li>
          <li className="navbar" onClick={showLeaderboard}>Leaderboard</li>
        </ul>
      </div>

      <div className="main">
        {screen === "rules" && (
          <div>
            <h2>Rules</h2>
            <ul>
              <li>You must enter seven words.</li>
              <li>No word can match the source word.</li>
              <li>No duplicate words.</li>
              <li>All words must be in the dictionary.</li>
              <li>Each letter must appear in the source word.</li>
              <li>Letters can't be used more than they appear in the source word.</li>
              <li>All words must have at least four letters.</li>
            </ul>
            <button onClick={startGame}>Play Game</button>
          </div>
        )}

        {screen === "game" && (
          <div>
            <h2>{sourceWord}</h2>
            <input className="inputbox" value={attempt} onChange={e => setAttempt(e.target.value)}
                   placeholder="Enter seven words..." />
            <button onClick={submitAttempt}>Confirm</button>
          </div>
        )}

        {screen === "end" && (
          <div>
            <p>{result}</p>
            <input type="text" value={username} onChange={e => setUsername(e.target.value)}
                   placeholder="Enter your name..." />
            <button onClick={submitDetails}>Confirm</button>
          </div>
        )}

        {screen === "leaderboard" && (
          <div>
            <h2>Leaderboard</h2>
            <ul className="leaderboard">
              <table className="table">
                <thead>
                  <tr>
                    <th>Position</th>
                    <th>Time</th>
                    <th>Name</th>
                    <th>Source Word</th>
                    <th>Attempt</th>
                  </tr>
                </thead>
                <tbody>
                  {highScores.map((score, i) => (
                    <tr key={i}>
                      <td>{i + 1}</td>
                      <td>{score.time}</td>
                      <td>{score.who}</td>
                      <td>{score.sourceWord}</td>
                      <td>{score.attempt}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}