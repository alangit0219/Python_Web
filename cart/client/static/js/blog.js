//針對log頁面定義一個對象
var log={
    startdt:"2020-3-19",
    enddt:"2021-3/19",
    upatedt:"2020-3-19",
    anchor:"Siri"
}
//由對象派生業務邏輯
log.submit={
    check:function(v){  //驗證某個值是否為空
        var _v=(v=="")?true:false;
        return _v;
    },
    autohide:function(obj){
        setTimeout(function(){
            obj.hide();
        },2000)
    }
}

//定義一個驗證內容是否為空的函數
function checkvalue(){
    //獲取元素對象，並保存在變量中
    var $username=$("#username");
    var $password=$("#password");
    var $err1=$("#err1");
    var $err2=$("#err2");
    //當用戶名和密碼不為空時
    if(!log.submit.check($username.val())&&!log.submit.check($password.val())){
        //直接提交
        return true;
    }else{
        //如果用戶名為空
        if($username.val()==""){
            //提示用戶名稱不惟空的錯誤信息顯示
            $err1.show();
            //2秒後自動隱藏
            log.submit.autohide($err1);
            //阻止提交
            return false;
        }else{//如果密碼為空時
            //題時密碼錯誤信息顯示
            $err2.show();
            //2秒後自動隱藏
            log.submit.autohide($err2);
            //阻止提交
            return false;
        }
    }
}  


//綁定按鈕單擊事件,標單提交時觸發
$(function(){
    var $form=$("form");
    var $btn=$(".btn>input");
})
//定義一個基於列表頁的業務邏輯
var lst={
    template:function(t,u,p1,p2){
        var _html="";
            _html+='<div class="item">';
            _html+='<div class="title">';
            _html+='    <h3>'+t+'</h3>';
            _html+='</div>';
            _html+='<div class="con">';
            _html+='    <div class="cleft">';
            _html+='        <img src="'+u+'" alt="">';
            _html+='    </div>';
            _html+='    <div class="cright">';
            _html+='        <p class="ptop">';
            _html+='            '+p1;
            _html+='        </p>';
            _html+='        <p class="pbottom">';
            _html+='            '+p2;
            _html+='        </p>';
            _html+='    </div>';
            _html+='</div>';
            _html+=' </div>'
            return _html;
    }
}
//使用數組保存展示的數組
var arrData=[
    {
        t:'Python語言的優勢',
        u:'imgs/b.jpg',
        p1:'本文探討了Python語言在AI領域的優勢與應用， 誰會成為AI和大數據時代的第一開發語言?這本已是一個不需要爭論的問題，如果說三年前,',
        p2:'初學路 學無上境 2021-3-21 34567閱讀 999'
    },{
        t:'Web語言的優勢',
        u:'imgs/b04.jpg',
        p1:'本文探討了Python語言在AI領域的優勢與應用， 誰會成為AI和大數據時代的第一開發語言?這本已是一個不需要爭論的問題，如果說三年前,',
        p2:'初學路 學無上境 2021-3-21 34567閱讀 999'
    },{
        t:'JavaScript語言的優勢',
        u:'imgs/b.jpg',
        p1:'本文探討了Python語言在AI領域的優勢與應用， 誰會成為AI和大數據時代的第一開發語言?這本已是一個不需要爭論的問題，如果說三年前,',
        p2:'初學路 學無上境 2021-3-21 34567閱讀 999'
    }]
//使用流程
//1.遍歷數組，獲取每一向元素對象
//2.將獲取的元素對象填充到模板中
//3.向頁面元素追加模板
for(var i=0;i<arrData.length;i++){
    //通過模板生成新的列表數據
    var _HTML=lst.template(arrData[i].t,arrData[i].u,arrData[i].p1,arrData[i].p2);
    //將數據追加到列表中
    $(".lst").append(_HTML);
}
//定義一個基於我的圖片頁的業務邏輯對象
var pics={
    template:function(u,n,t){
        var _html="";
            _html+='<div class="item">';
            _html+='<div class="imgs">';
            _html+='    <img src="'+u+'" alt="">';
            _html+='    <div class="tip">喜歡 | '+n+'</div>';
            _html+='</div>';
            _html+='<div class="title">';
            _html+='    <h3>'+t+'</h3>';
            _html+='</div>';
            _html+='</div>';
            return _html;
    }
}
//定義一個包含三個對象內容的圖片數組
var arrPics=[
    {
        u:'imgs/b04.jpg',
        n:666,
        t:'python中打開txt文件報錯'
    },{
        u:'imgs/banner03.jpg',
        n:777,
        t:'web頁面開發重要性'
    },{
        u:'imgs/banner01.jpg',
        n:878,
        t:'JavaScript開發時碰到的問題'
    }]
//使用流程
//1.遍歷數組，獲取每一向元素對象
//2.將獲取的元素對象填充到模板中
//3.向頁面元素追加模板
for(var j=0;j<arrPics.length;j++){
    //通過模板生成新的列表數據
    var _HTML=pics.template(arrPics[j].u,arrPics[j].n,arrPics[j].t);
    //將數據追加到列表中
    $("#pics").append(_HTML);
}