function order(){
    if (confirm("Bạn có chắc muốn đặt đơn hàng này?") === true){
        fetch("/api/order", {
            method: "post"
        }).then(res => res.json()).then(data => {
            if (data.status == 200){
                alert("Đặt hàng thành công")
                location.reload()
            }
            else
                alert("Đặt hàng thất bại")
                console.log(data.err_msg)
        })
    }
}

function pay(){
    fetch("/create-checkout-session", {
        method: "post",
    }).then(res => res.json()).then(data => {
        if (data.status === 303){
            window.location = data.url
        }
    })
}