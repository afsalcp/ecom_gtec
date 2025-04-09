let email_valid=false,password_valid=false,fullname_valid=false;
        $("#signup_submit").click(()=>{
            if(email_valid&&password_valid&&fullname_valid){
                $.ajax({
                    url:"/signup",
                    type:"post",
                    data:{
                        username:fullname_valid,
                        password:password_valid,
                        email:email_valid,
                        csrfmiddlewaretoken:csrfToken
                    },
                    success:(res)=>{
                    	console.log(res)
                        if(res.err){
                            $('#form_errors').html(`
                                ${
                                    res.msg.reduce((t,c)=>{
                                        return t+=`<span style="margin-top:10px">${c}</span>`
                                    },"")
                                }
                            `)
                        }else{
                            location.href=res.redirect
                        }
                    },
                    error:e=>{
                    	console.log(e)
                    }
                })
            }
        })

        $("input[name=fullname]").keyup(function(){
            var name=$(this).val()

            if(/^[a-zA-Z0-9]{4,20}$/.test(name)){
                fullname_valid=name
                $(this).next('span').removeClass('fa-circle-xmark').addClass("fa-circle-check").addClass('okey').removeClass('wrong')
            }else{
                fullname_valid=false
                $(this).next('span').removeClass('fa-circle-check').addClass("fa-circle-xmark").addClass('wrong').removeClass('okey')
            }
        })

        $("input[name=email]").keyup(function(){
            var email=$(this).val()

            if(/^(.+){3,}@(.+){2,20}\.(.+){2,10}$/.test(email)){
                email_valid=email
                $(this).next('span').removeClass('fa-circle-xmark').addClass("fa-circle-check").addClass('okey').removeClass('wrong')
            }else {
                email_valid=false
                $(this).next('span').removeClass('fa-circle-check').addClass("fa-circle-xmark").addClass('wrong').removeClass('okey')
            }
        })

        $("input[name=password]").keyup(function(){
            var password=$(this).val()

            if(password.length>=8&&/[a-z]/.test(password)&&/[A-Z]/.test(password)&&/[0-9]/.test(password)&&/[^a-zA-Z0-9]/.test(password)){
                password_valid=password;
                $(this).next('span').removeClass('fa-circle-xmark').addClass("fa-circle-check").addClass('okey').removeClass('wrong')
            }else{
                password_valid=false;
                $(this).next('span').removeClass('fa-circle-check').addClass("fa-circle-xmark").addClass('wrong').removeClass('okey')
            }
        })