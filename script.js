async function runCode() {
    const code = document.getElementById("userCode").value;
    const input = document.getElementById("output").value;
    const language = document.getElementById("language").value;

    document.addEventListener("DOMContentLoaded", function () {
        document.getElementById("runButton").addEventListener("click", runCode);
      });
      

    const response = await fetch("/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, language, input })
    });

    const data = await response.json();
    document.getElementById("output").innerText = data.output || data.error;
}
