async function fetchEvents() {
  const res = await fetch("http://localhost:5000/events");
  const data = await res.json();
  const eventList = document.getElementById("events");
  eventList.innerHTML = "";

  data.forEach(event => {
    let line = "";
    const time = new Date(event.timestamp).toUTCString();

    if (event.action === "PUSH") {
      line = `${event.author} pushed to ${event.to_branch} on ${time}`;
    } else if (event.action === "PULL_REQUEST") {
      line = `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${time}`;
    } else if (event.action === "MERGE") {
      line = `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${time}`;
    }

    const li = document.createElement("li");
    li.textContent = line;
    eventList.appendChild(li);
  });
}

fetchEvents();
setInterval(fetchEvents, 15000);
