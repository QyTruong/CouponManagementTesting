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
                alert(data.err_msg)
        })
    }
}

function pay(order_id){
    fetch(`/payment/${order_id}`, {
        method: "post",
    }).then(res => res.json()).then(data => {
        if (data.status === 303){
            console.log("hello")
            window.location.href = data.url
        }
        else {
            console.log('bruh')
            console.log(data.error)
        }
    })
}