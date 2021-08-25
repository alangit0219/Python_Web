// common.js
function makeHeader(username){
    //username   有登陸的用戶
    var header_body = ''
    header_body += '<!-- 設計頁面導航條元素 -->';
    header_body += '<div id="nav">';
    header_body += '<div class="box1">';
    header_body += '<!-- 標題元素 -->';
    header_body += '<div class="title">';
    header_body += '<a href="/index"><h3>東園咖啡</h3></a>';
    header_body += '</div>';
    header_body += '</div>';
    header_body += '<div class="box2">';
    header_body += '<!-- 列表元素 -->';
    header_body += '<div class="list">';
    header_body += '<ul>';
    header_body += '<li><a href="/introduction">商店介紹</a></li>';
    header_body += '<li><a href="/products">所有商品</a></li>';
    header_body += '<li><a href="/shipping">運送政策</a></li>';
    if (username){
        header_body += '<li><a href="/user/' + username + '">會員中心</a></li>';
    }else{
        header_body += '<li><a href="/login">會員登錄/註冊</a></li>'
    }
    if (username){
        header_body += '<li><a href="/carts">購物車</a></li>';
    }
    if (username){
        header_body += '<li><a href="javascript:;" id="loginOut">登出</a></li>';
    }
    header_body += '</ul>';
    header_body += '</div>';
    header_body += '</div>';
    header_body += '</div>';
    return header_body
}


function makeFooter(){
    var footer_body = '';
    footer_body += '<div id="clear"></div>';
    footer_body += '<div style="height: 300px;">';
    footer_body += '</div>';
    footer_body += '<div id="footer">';
    footer_body += '<div>門市電話/(03)xxxx-xxxx</div>';
    footer_body += '<div>地址:桃園市中壢區九和二街xx號</div>';
    footer_body += '<div class="mail">信箱:xiedong0219@gmail.com</div>';
    footer_body += '</div>';
    return footer_body
}


function loginOut(){

    $("#loginOut").click(function(){
            if(confirm("確定登出嗎？")){
                window.localStorage.removeItem('cart_token');
                window.localStorage.removeItem('cart_user');
                window.location.href= '/index';
            }
        }
    )

}
