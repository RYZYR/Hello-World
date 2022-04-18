$(document).ready(function() {
    var $img = $("#contain .box .img ul li");
    var $checkout = $("#contain .box .checkout ul li");
    var $left = $("#contain .box .btn .left_btn");
    var $right = $("#contain .box .btn .right_btn");
    var index = 0;
    var timer = null;


    //鼠标进入进出显示/隐藏切换按钮
    $("#contain").hover(function() {
        clearInterval(timer);
        $("#contain .btn").show();

    }, function() {
        autoplay();
        $("#contain .btn").hide();
    });

    //封装播放函数
    function play() {
        $img.eq(index).addClass("on").siblings().removeClass("on");
        $checkout.eq(index).addClass("this").siblings().removeClass("this");
    }

    //自动播放
    function autoplay() {
        timer = setInterval(function() {
            index++;
            if (index > 4) {
                index = 0;
            }
            play();
        }, 2000);
    }
    autoplay();

    //手动切换
    $left.click(function() {
        index--;
        if (index < 0) {
            index = 4;
        }
        play();
    });
    $right.click(function() {
        index++;
        if (index > 4) {
            index = 0;
        }
        play();
    });

    //点击下标切换
    $checkout.click(function() {
        index = $(this).index();
        play();
    });
});