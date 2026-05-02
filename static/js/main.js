// Trigger emergency ambulance request with popup + status updates.
async function requestAmbulance(patientId) {
  const statusText = document.getElementById("ambulance-status");

  const confirmAction = confirm("Are you sure you want to request an ambulance?");
  if (!confirmAction) {
    statusText.textContent = "Request cancelled.";
    return;
  }

  statusText.textContent = "Sending...";

  try {
    const response = await fetch(`/patient/${patientId}/request-ambulance`, { method: "POST" });
    const data = await response.json();

    if (response.ok) {
      statusText.textContent = data.status;
      setTimeout(() => window.location.reload(), 800);
    } else {
      statusText.textContent = "Failed to send request.";
    }
  } catch (error) {
    statusText.textContent = "Error: Unable to send request.";
  }
}
