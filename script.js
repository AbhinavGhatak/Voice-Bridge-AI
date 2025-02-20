document.addEventListener("DOMContentLoaded", function () {
    const startButton = document.getElementById("startButton");
    const responseContainer = document.getElementById("responseContainer");
    
    startButton.addEventListener("click", async function () {
        responseContainer.innerHTML = "Listening...";
        try {
            const response = await fetch("http://localhost:5000/start");
            const data = await response.json();
            responseContainer.innerHTML = `<strong>AI:</strong> ${data.message}`;
        } catch (error) {
            console.error("Error connecting to Voice Bridge AI:", error);
            responseContainer.innerHTML = "Error connecting to Voice Bridge AI.";
        }
    });
});
