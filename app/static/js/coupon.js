function applyCoupon(){
    const code = document.getElementById('select-coupon')

    fetch("/api/coupons", {
        method: "post",
        body: JSON.stringify({
            code: code.value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(res => res.json()).then(data => {
        if (data.status == 200){
            location.reload()
        }
        else if (data.status == 401) {
            alert(data.err_msg)
        }
    })
}
