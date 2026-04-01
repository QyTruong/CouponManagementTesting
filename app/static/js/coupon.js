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
            location.reload()
        }
        else {
            alert(data.err_msg)
        }
    })
}

function detachCoupon(){
    fetch("/api/coupons", {
        method: "delete"
    }).then(res => res.json()).then(data => {
        if (data.status == 200){
            alert("Đã gỡ mã giảm giá ra khỏi đơn hàng")
            location.reload()
        }
        else
            alert("Gỡ mã thất bại")
    })
}
