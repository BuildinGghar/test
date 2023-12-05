$(document).ready(function() {
    var options = {}; // Declare options object outside the AJAX callback

    $('.payWithRazorpay').click(function(e) {
        e.preventDefault();
        var cname = $("[name='cname']").val();
        var location = $("[name='location']").val();
        var city = $("[name='city']").val();
        var state = $("[name='state']").val();
        var zipcode = $("[name='zipcode']").val();

        $.ajax({
            method: "GET",
            url: "/checkout/",
            dataType: "json",
            success: function(response) {
                console.log(response);
                options = {
                    "key": "rzp_test_oSUhuHMFkhRyVx",
                    "amount": response.totalamount,
                    "currency": "INR",
                    "name": "Building Ghar",
                    "description": "Thank you for buying from us.😊",
                    "image": "https://example.com/your_logo",
                    "handler": function(response) {
                        alert(response.razorpay_payment_id);
                    },
                    "prefill": {
                        "name": cname
                    },
                    "theme": {
                        "color": "#3399cc"
                    }
                };
                var rzp1 = new Razorpay(options);
                rzp1.open();
            }
        });
    });
});