function getCSRFToken() {
    let cookies = document.cookie.split("; ");
    for (let cookie of cookies) {
        let [name, value] = cookie.split("=");
        if (name === "csrftoken") {
            return value;
        }
    }
    return ""; // Return empty string if CSRF token is not found
}
    function deleteWorker(workerId) {
    if (confirm("Are you sure you want to delete this worker?")) {
        fetch(`/showworkers/delete/${workerId}/`, {
            method: "DELETE",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCSRFToken()  // CSRF protection
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => { throw new Error(text) }); // 🔍 Handle errors
            }
            return response.json(); // ✅ Parse JSON response
        })
        .then(data => {
            console.log("Server Response:", data); // 🔍 Debugging
            if (data.success) {
                document.getElementById(`worker-${workerId}`).remove();
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(error => {
            console.error("Fetch error:", error);
            alert("Failed to delete worker. Check console for details.");
        });
    }
}

