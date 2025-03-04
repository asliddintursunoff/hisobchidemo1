document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("td").forEach(td => {
        let span = td.querySelector(".number-display");
        if (span) {
            td.addEventListener("click", function (event) {
                if (event.detail === 2) { // Фақат икки марта босганда очиш
                    editNumber(this);
                }
            });
        }
    });
});

function editNumber(td) {
    let span = td.querySelector(".number-display");
    let form = td.querySelector(".edit-form");

    if (form) {
        closeAllForms();
        span.style.display = "none";
        form.style.display = "block";

        let input = form.querySelector("input");
        input.focus();
        input.select();
    }
}

// ✅ Бошқа ҳужжатларга босилганда формани ёпиш
document.addEventListener("click", function (event) {
    if (!event.target.closest("td")) {
        closeAllForms();
    }
});

function getCSRFToken() {
    return document.querySelector("meta[name='csrf-token']").getAttribute("content");
}

function closeAllForms() {
    document.querySelectorAll(".edit-form").forEach(form => {
        let td = form.closest("td");
        let span = td.querySelector(".number-display");

        form.style.display = "none";
        span.style.display = "block";
    });
}

function submitForm(event, form, progressId) {
    event.preventDefault(); // Reload'ни олдини олиш

    let input = form.querySelector("input[type='number']");
    let newValue = input.value.trim();
    let year2 = document.getElementById("year2").value;
    let month2 = document.getElementById("month2").value;

    if (!/^\d+$/.test(newValue)) {
        showFlashMessage("❌ Илтимос, тўғри сон киритинг!", "error");
        return;
    }

    fetch("/update-progress-item/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({
            progress_id: progressId,
            progress_value: parseInt(newValue),
            year2 : year2,
            month2 : month2,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            let td = form.closest("td");
            let span = td.querySelector(".number-display");

            span.textContent = data.new_value;
            form.style.display = "none";
            span.style.display = "block";
            showFlashMessage("✅ Маълумот сақланди!", "success");
        } else {
            showFlashMessage("❌ Хатолик: " + data.error, "error");
        }
    })
    .catch(error => console.error("Fetch Error:", error));
}

function validateInteger(input) {
    input.value = input.value.replace(/[^0-9]/g, ""); // Фақат сонларга рухсат бериш
}

// ✅ Флеш хабарни кўрсатиш функцияси
function showFlashMessage(message, type) {
    let flashMessage = document.getElementById("flash-message");
    if (!flashMessage) return;

    flashMessage.textContent = message;
    flashMessage.style.display = "block";
    flashMessage.style.backgroundColor = type === "success" ? "green" : "red";
    flashMessage.style.color = "white";

    setTimeout(() => {
        flashMessage.style.display = "none";
        //for reloading
        location.reload();
        //for reloading
    }, 1500);
}




document.getElementById("save-btn").addEventListener("click", function(event) {
    event.preventDefault();  // Prevent form submission

    let workName = document.getElementById("work-name").value;
    let workPrice = document.getElementById("work-price").value;
    let productType = document.getElementById("mahsulot_turi1").value;

    // Validate input
    if (!workName || !workPrice) {
        showFlashMessage("Илтимос, барча майдонларни тўлдиринг!", "error");
        return;
    }

    fetch("/adminpage/addworker/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({
            work_name: workName,
            price: parseInt(workPrice),
            types: productType,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showFlashMessage("Иш муваффақиятли қўшилди!", "success");
            document.getElementById("work-name").value = "";
            document.getElementById("work-price").value = "";
            document.getElementById("mahsulot_turi1").value;
        } else {
            showFlashMessage("Хатолик: " + data.error, "error");
        }
    })
    .catch(error => console.error("Error:", error));
});

// Function to show flash messages
function showFlashMessage(message, type) {
    let flashMessage = document.getElementById("flash-message");
    flashMessage.innerText = message;
    flashMessage.style.display = "block";
    flashMessage.style.color = "#fff";
    flashMessage.style.padding = "10px";
    flashMessage.style.marginTop = "10px";
    flashMessage.style.borderRadius = "5px";
    
    if (type === "success") {
        flashMessage.style.backgroundColor = "green";
    } else {
        flashMessage.style.backgroundColor = "red";
    }

    setTimeout(() => {
        flashMessage.style.display = "none";
        //for reloading
        location.reload();
        //for reloading
    },1);  // Hide after 3 seconds
}

// Function to get CSRF token from cookies
function getCSRFToken() {
    let cookieValue = null;
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.startsWith("csrftoken=")) {
            cookieValue = cookie.substring("csrftoken=".length, cookie.length);
            break;
        }
    }
    return cookieValue;
}






//for ADDING WORKER

document.addEventListener("DOMContentLoaded", function () {
    // Get the current URL
    let currentUrl = window.location.href;

    // Get all buttons
    let buttons = document.querySelectorAll(".btn-link .btn");

    buttons.forEach((button) => {
        let btnLink = button.parentElement.href; // Get <a> link
        
        // If the button link matches the current URL, add active class
        if (currentUrl === btnLink) {
            button.classList.add("active");
        }
    });
});
$(document).ready(function () {
    // Function to show flash messages
    function showFlashMessage(message, type = "success") {
        let flashDiv = $("#flash-message");
        flashDiv.html(message).removeClass().addClass("flash-message " + type).fadeIn();

        setTimeout(function () {
            flashDiv.fadeOut();
        }, 3000);
    }

    // Function to get available works as options
    function getWorksOptions() {
        let options = '<option value="">Ишни танланг</option>';
        worksData.forEach(work => {
            options += `<option value="${work.id}">${work.name} - ${work.price} so'm</option>`;
        });
        return options;
    }

    // Function to get all selected work IDs
    function getSelectedWorkIds() {
        return $("select[name='work']").map(function () {
            return $(this).val();
        }).get();
    }

    // Add new work selection dynamically
    $("#select-container").on("click", ".add-select", function () {
        let newGroup = `
            <div class="select-group">
                <select name="work" class="work-select">
                    ${getWorksOptions()}
                </select>
                <button type="button" class="add-select">+</button>
                <button type="button" class="remove-select">-</button>
            </div>`;

        $("#select-container").append(newGroup);
    });

    // Remove a work selection
    $("#select-container").on("click", ".remove-select", function () {
        if ($(".select-group").length > 1) {
            $(this).parent().remove();
        }
    });

    // Prevent duplicate work selection
    $("#select-container").on("change", ".work-select", function () {
        let selectedValue = $(this).val();
        let selectedWorks = getSelectedWorkIds();
        let prevValue = $(this).data("prev") || ""; // Store previous value

        if (selectedValue && selectedWorks.filter(work => work === selectedValue).length > 1) {
            showFlashMessage("Бу иш аллақачон танланган!", "error");
            $(this).val(prevValue); // Revert back to the previous selection
        } else {
            $(this).data("prev", selectedValue); // Store new valid value
        }
    });

    // Handle form submission using AJAX
    $("#worker-form").submit(function (e) {
        e.preventDefault(); // Prevent default form submission

        // Validate that all selected works are valid (not empty)
        let isValid = true;
        $(".work-select").each(function () {
            if (!$(this).val()) {
                isValid = false;
                showFlashMessage("Mavjud bo'lmagan ish tanlandi", "error");
                return false; // Exit loop
            }
        });

        if (!isValid) return; // Stop submission if validation fails

        let formData = $(this).serializeArray(); // Serialize form data

        $.ajax({
            type: "POST",
            url: workerFormUrl, // Use a global variable set in the template
            data: formData,
            success: function (response) {
                showFlashMessage("Ишчи ва Прогресс муваффақиятли яратилди!", "success");
                setTimeout(function () {
                    location.reload();
                }, 100);
            },
            error: function (xhr, status, error) {
                showFlashMessage("Хатолик юз берди: " + xhr.responseText, "error");
            }
        });
    });
});






$(document).ready(function () {
    // Function to show flash messages
    function showFlashMessage(message, type = "success") {
        let flashDiv = $("#flash-message");
        flashDiv.html(message).removeClass().addClass("flash-message " + type).fadeIn();
        setTimeout(function () {
            flashDiv.fadeOut();
        }, 3000);
    }

    // Open modal when clicking "Ishchi qo'shish"
    $(".adder").click(function () {
        console.log("Opening modal...");
        $("#modal-add-items").fadeIn();
    });

    // Close modal when clicking "X"
    $("#close-add-items").click(function () {
        console.log("Closing modal...");
        $("#modal-add-items").fadeOut();
    });

    // Handle form submission via AJAX
    $("#form-add-item").submit(function (event) {
        event.preventDefault();  

        console.log("Submitting form via AJAX...");
        
        let csrfToken = $("input[name=csrfmiddlewaretoken]").val();
        let url = $("#btn-save-item").data("url");  
        let selectedOption = $("#select-item-type").find("option:selected");

        let formData = {
            type_date: $("#hidden-item-date").val(),
            type_name: $("#input-item-name").val(),
            type_id: selectedOption.val() || "None", // If not selected, send "None"
        };

        // Validation
        if (!formData.type_name) {
            showFlashMessage("Барча майдонларни тўлдиринг!", "error");
            return;
        }

        $.ajax({
            type: "POST",
            url: url,
            headers: { "X-CSRFToken": csrfToken },
            data: JSON.stringify(formData),
            contentType: "application/json",
            success: function (response) {
                console.log("✅ AJAX Success:", response);
                showFlashMessage("Янги ишчи муваффақиятли қўшилди!", "success");
                $("#modal-add-items").fadeOut();
                setTimeout(function () {
                    location.reload();
                }, 1500);
            },
            error: function (xhr) {
                console.log("❌ AJAX Error:", xhr.responseText);
                showFlashMessage("Хатолик юз берди: " + xhr.responseText, "error");
            },
        });
    });
});
