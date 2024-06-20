// set a function, so the function will run after the page is full load
$(function () {
    function bindCaptchaBtnClick() {
        $("#captcha_btn").click(function (event) {
            let $this = $(this)
            let email = $("input[name = 'email']").val();

            if (!email) {
                alert("Please enter valid email");
                return;
            }
            // if enter valid email, disable button
            $this.off('click');
            
            // send ajax request( visit url without reloading the page)
            $.ajax('/auth/captcha?email=' + email,{
                method: "GET",
                success: function(result){
                    if(result['code'] ===200){
                        alert("Verify code sent successfully");
                    }
                    else{
                        alert(result['message'])
                    }
                },
                fail: function(error){
                    console.log(error);
                }

            })

            // start count down
            let countdown = 6;
            let timer = setInterval(function () {
                if (countdown <= 0) {
                    $this.text('Receive code');
                    // if countdown less than 0, clear it
                    clearInterval(timer);
                    bindCaptchaBtnClick()
                } else {
                    countdown--;
                    $this.text(countdown + 's');
                }

            }, 1000)
        })
    }

   bindCaptchaBtnClick();
});