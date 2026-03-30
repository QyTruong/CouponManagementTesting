function applyCoupon(){
    const code = document.getElementById('code').value

    fetch("/api/coupons", {
        method: "post",
        body: JSON.stringify({
            code: code
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(res => res.json()).then(data => {
        if (data.status == 200){
            let basePrices = document.getElementsByClassName('base-price')
            for (let b of basePrices)
                b.innerText = data.base_price.toLocaleString('en') + " VNĐ"

            let discountValues = document.getElementsByClassName('discount-value')
            for (let d of discountValues)
                d.innerText = data.discount_value.toLocaleString('en') + " VNĐ"

            let totalPrices = document.getElementsByClassName('total-price')
            for (let t of totalPrices)
                t.innerText = data.total_price.toLocaleString('en') + " VNĐ"
        }
        else {
            console.log(data.err_msg)
        }
    })
}
