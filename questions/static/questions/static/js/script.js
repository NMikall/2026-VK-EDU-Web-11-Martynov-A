function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const likeButtons = document.querySelectorAll('button[data-id]')

for (const item of likeButtons) {
    item.addEventListener('click', (e) => {
        const {id, kind, type} = item.dataset
        const counter = document.querySelector(`span[data-like-counter="${kind}-${id}"]`)

        const request = new Request(
            `/like/${kind}/${id}/${type}/`,
            {
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                mode: 'same-origin' // Do not send CSRF token to another domain.
            }
        );
        fetch(request).then(function(response) {
            response.json().then((data) => {
                    counter.innerText = data.count
                }
            ).catch((error) => console.error(error))
        }).catch((error) => console.error(error))
    })
}


const bestCheckboxes = document.querySelectorAll('input[data-answer-id]')

for (const item of bestCheckboxes) {
    item.addEventListener('change', () => {
        const {questionId, answerId} = item.dataset

        const request = new Request(`/best/${questionId}/${answerId}/`, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin'
        })
        fetch(request).then((response) => {
            if (!response.ok) {
                item.checked = !item.checked
                return
            }
            for (const other of bestCheckboxes) {
                if (other !== item) other.checked = false
            }
        }).catch((error) => console.error(error))
    })
}