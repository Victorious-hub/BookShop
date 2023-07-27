
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




let btns1 = document.querySelectorAll(".Remove button")
btns1.forEach(btn=>{
    btn.addEventListener("click", removeFromCart)
})

function removeFromCart(e){
    let product_id = e.target.value
    let url = "/remove_from_cart"

    let data = {id:product_id}

    fetch(url, {
        method: "POST",
        headers: {"Content-Type":"application/json", 'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)
    })
    .then(res=>res.json())
    .then(data => {
    document.getElementById("num_of_items").innerHTML = data.num_of_items;
    document.getElementById("total_price").innerHTML = data.price;
    console.log(data);
})
    .catch(error=>{
        console.log(error)
    })
}


let btns2 = document.querySelectorAll(".RemoveAll button")
btns2.forEach(btn=>{
    btn.addEventListener("click", removeAll)
})

function removeAll(e){
    let product_id = e.target.value
    let url = "/remove_all"

    let data = {id:product_id}

    fetch(url, {
        method: "POST",
        headers: {"Content-Type":"application/json", 'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)
    })
    .then(res=>res.json())
    .then(data => {
    document.getElementById("num_of_items").innerHTML = data.num_of_items;
    document.getElementById("total_price").innerHTML = data.price;
    console.log(data);
})
    .catch(error=>{
        console.log(error)
    })
}


let btns4 = document.querySelectorAll(".RemoveFromList button")
btns4.forEach(btn=>{
    btn.addEventListener("click", removeFromWishList)
})

function removeFromWishList(e){
    let product_id = e.target.value
    let url = "/remove_wishlist"

    let data = {id:product_id}

    fetch(url, {
        method: "POST",
        headers: {"Content-Type":"application/json", 'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)
    })
    .then(res=>res.json())
    .then(data => {
    document.getElementById("wish").innerHTML = data;
    console.log(data);
})
    .catch(error=>{
        console.log(error)
    })
}






let btns3 = document.querySelectorAll(".addwishlist button")
btns3.forEach(btn=>{
    btn.addEventListener("click",addWishlist)
})

function addWishlist(e){
    let product_id = e.target.value
    let url = "/add_to_wishlist"

    let data = {id:product_id}

    fetch(url, {
        method: "POST",
        headers: {"Content-Type":"application/json", 'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)
    })
    .then(res=>res.json())
    .then(data => {
    console.log(data);
})
    .catch(error=>{
        console.log(error)
    })
}

