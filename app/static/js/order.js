function order(){
    if (confirm("Bạn có chắc muốn đặt đơn hàng này?") === true){
        fetch("/api/order", {
            method: "post"
        }).then(res => res.json()).then(data => {
            if (data.status == 200){
                coupon_err_msg = ""
                if (data.coupon_err_msg) coupon_err_msg = data.coupon_err_msg
                alert("[Thành công] Đặt hàng thành công" + "\n\n[Lỗi] Mã không áp dụng được vì: " + coupon_err_msg)
                location.reload()
            }
            else
                alert(data.err_msg)
        })
    }
}

function pay(order_id){
    fetch(`/payment/${order_id}`, {
        method: "post",
    }).then(res => res.json()).then(data => {
        if (data.status === 303){
            window.location.href = data.url
        }
        else {
            console.log(data.error)
        }
    })
}