const csrftoken = document.cookie.match(/csrftoken=([^;]+)/)[1];

function deleteTodo(event) {
    if (confirm("Желаете ли вы удалить?")) {
        event.preventDefault();
        url = event.target.getAttribute("href-data");
        axios.post(url, null, {
            headers: {
                'X-CSRFToken': csrftoken,
            },
        }).then(response => {
            if (response['status'] == 200) {
                document.getElementById('id_todo_' + event.target.getAttribute('data-id')).setAttribute("hidden", "");
            }
        })
    }
}

function updateComplete(event) {
    const checkbox = event.target;
    const completed_ = checkbox.checked
    const url = checkbox.getAttribute("href-data");
    const params = new URLSearchParams();
    params.append('completed', completed_);
    axios.post(url, params.toString(), {
        headers: {
            "X-CSRFToken": csrftoken
        }
    }).then(response => {
        console.log(response.data["todo_update"]["completed"]);
    })
        .catch(error => {
            // Обработка ошибки er-axios-

        });
}

window.onload = function () {
    document.querySelectorAll(".btn-delete").forEach(btn => btn.addEventListener("click", deleteTodo))
    document.querySelectorAll('.complete-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', updateComplete);
    });
}


