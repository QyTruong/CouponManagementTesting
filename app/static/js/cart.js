
function addToCart(id, name, price){
    fetch("/api/cart", {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        let elems = document.getElementsByClassName('cart-counter')
        for (let e of elems)
            e.innerText = data.total_quantity

        let basePrices = document.getElementsByClassName('total-price')
        for (let b of basePrices)
            b.innerText = data.total_price.toLocaleString('en') + " VNĐ"

        let discountValues = document.getElementsByClassName('discount-value')
        for (let d of discountValues)
            d.innerText = data.discount_value.toLocaleString('en') + " VNĐ"

        let totalPrices = document.getElementsByClassName('final-price')
        for (let t of totalPrices)
            t.innerText = data.final_price.toLocaleString('en') + " VNĐ"
    })
}

function deleteFromCart(id){
    if (confirm("Bạn có chắc chắn xóa sản phẩm này ?") === true){
        fetch(`/api/cart/${id}`, {
            method: "delete"
        }).then(res => res.json()).then(data => {
            let elems = document.getElementsByClassName('cart-counter')
            for (let e of elems)
                e.innerText = data.total_quantity

            let basePrices = document.getElementsByClassName('total-price')
            for (let b of basePrices)
                b.innerText = data.total_price.toLocaleString('en') + " VNĐ"

            let discountValues = document.getElementsByClassName('discount-value')
            for (let d of discountValues)
                d.innerText = data.discount_value.toLocaleString('en') + " VNĐ"

            let totalPrices = document.getElementsByClassName('final-price')
            for (let t of totalPrices)
                t.innerText = data.final_price.toLocaleString('en') + " VNĐ"

            let item = document.getElementById(`cart${id}`)
            item.style.display = "none"
        })
    }
}

function updateCart(id, object){
    fetch(`/api/cart/${id}`, {
        method: "put",
        body: JSON.stringify({
            "quantity": object.value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        elems = document.getElementsByClassName('cart-counter')
        for (let e of elems)
            e.innerText = data.total_quantity

        let basePrices = document.getElementsByClassName('total-price')
        for (let b of basePrices)
            b.innerText = data.total_price.toLocaleString('en') + " VNĐ"

        let discountValues = document.getElementsByClassName('discount-value')
        for (let d of discountValues)
            d.innerText = data.discount_value.toLocaleString('en') + " VNĐ"

        let totalPrices = document.getElementsByClassName('final-price')
        for (let t of totalPrices)
            t.innerText = data.final_price.toLocaleString('en') + " VNĐ"
    })
}