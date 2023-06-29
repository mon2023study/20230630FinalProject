$(function(){
    $.ajax({
        url:'/api/result',
        success:function(datas){
            new Chart($('[chart="年齡"]').get(0).getContext('2d'), {
                type: 'bar',
                data: {
                    labels: Object.keys(datas['年齡']),
                    datasets: [{
                        label: '年齡',
                        data: Object.values(datas['年齡']),
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                    }]
                }
            });
            pies=['性別','縣市','教育程度','觀看政見前','觀看政見後','主動查詢各候選人的政見','媒體識讀能力','查證新聞內容','檢視各方看法並分析'];
            for(pk in pies){
                new Chart($('[chart="'+pies[pk]+'"]').get(0).getContext('2d'), {
                    type: 'pie',
                    data: {
                        labels: Object.keys(datas[pies[pk]]),
                        datasets: [{
                            label: pies[pk],
                            data: Object.values(datas[pies[pk]]),
                            backgroundColor: [
                                'rgba(255, 99, 132, 0.2)',
                                'rgba(54, 162, 235, 0.2)',
                                'rgba(255, 206, 86, 0.2)',
                                'rgba(75, 192, 192, 0.2)',
                                'rgba(153, 102, 255, 0.2)',
                                'rgba(255, 159, 64, 0.2)'
                            ],
                        }]
                    }
                });
            }
            tes=['候選人評分1','候選人評分2']
            for(tk in tes){
                html = '';
                for(tstk in datas[tes[tk]]){
                    tstv = datas[tes[tk]][tstk];
                    html+='<td>'+tstv[1]+'</td><td>'+tstv[2]+'</td><td>'+tstv[3]+'</td><td>'+tstv[4]+'</td><td>'+tstv[5]+'</td>';
                }
                $('[table="'+tes[tk]+'"]').html('<table class="table table-striped table-bordered table-hover text-center"><tr><th colspan="5">柯文哲</th><th colspan="5">侯友宜</th><th colspan="5">賴清德</th></tr><tr><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td></tr><tr>'+html+'</tr></table>')
            }
        }
    })
})