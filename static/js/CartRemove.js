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

let btns1 = document.querySelectorAll(".Remove button");
btns1.forEach(btn => {
    btn.addEventListener("click", removeFromCart);
});

function removeFromCart(e) {
    let product_id = e.target.value;
    let url = "/remove_from_cart";

    let data = { id: product_id };

    fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
        body: JSON.stringify(data),
    })
        .then((res) => res.json())
        .then((data) => {
            let num_of_items_element = document.getElementById("num_of_items" + product_id);
            num_of_items_element.innerHTML = data;
            console.log(data);
        })
        .catch((error) => {
            console.log(error);
        });
}

let btns = document.querySelectorAll(".container1 button")
btns.forEach(btn=>{
    btn.addEventListener("click", addToCart)
})

function addToCart(e){
    let product_id = e.target.value
    let url = "/add_to_cart"

    let data = {id:product_id}

    fetch(url, {
        method: "POST",
        headers: {"Content-Type":"application/json", 'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)
    })
    .then(res=>res.json())
    .then(data=>{
        document.getElementById("num_of_items").innerHTML = data
        console.log(data)
    })
    .catch(error=>{
        console.log(error)
    })
}
