$(function(){
    $.ajax({
        url:'/api/wiki',
        success:function(datas){
            html = "";
            for(k in datas){
                data = datas[k];
                if(data.length==0){html+='<tr><td colspan="8">等待新的民調公佈...</td></tr>'; continue;}
                html+='<tr><td>'+data[0]+'</td><td>'+data[1]+'</td><td>'+data[2]+'</td><td>'+data[3]+'</td><td>'+data[4]+'</td><td>'+data[5]+'</td><td>'+data[6]+'</td><td>'+data[7]+'</td></tr>';
            }
            $('#wiki').html('<table class="table table-striped table-hover" style="min-width:700px;"><tr><th>調查來源</th><th>調查日期</th><th>調查方法</th><th>樣本數目</th><th>賴清德</th><th>侯友宜</th><th>柯文哲</th><th>皆不支持/未決定/拒絕回答</th></tr>'+html+'</table>')
        }
    })
})