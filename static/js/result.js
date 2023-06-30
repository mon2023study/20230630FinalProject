
$(function(){
    bgcs={
        '年齡':[
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
        ],
        '觀看政見':[
            'rgba(0, 204, 255, 0.2)', 
            'rgba(0, 0, 205, 0.2)',
            'rgba(50, 205, 50, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
        ],
        '觀看政見前':[
            'rgba(0, 204, 255, 0.2)', 
            'rgba(0, 0, 205, 0.2)',
            'rgba(50, 205, 50, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
        ],
        '觀看政見後':[
            'rgba(0, 204, 255, 0.2)', 
            'rgba(0, 0, 205, 0.2)',
            'rgba(50, 205, 50, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
        ],
        '教育程度':[
            'rgba(50, 205, 50, 0.2)',
            'rgba(0, 0, 205, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)', 
            'rgba(0, 204, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)',
        ],
        '性別':[
            'rgba(0, 204, 255, 0.2)', 
            'rgba(255, 99, 132, 0.2)',
        ],
        '主動查詢各候選人的政見':[
            'rgba(54, 162, 235, 0.8)', 
            'rgba(255, 99, 132, 0.8)',
        ],
        '媒體識讀能力':[
            'rgba(54, 162, 235, 0.8)', 
            'rgba(255, 99, 132, 0.8)',
        ],
        '查證新聞內容':[
            'rgba(54, 162, 235, 0.8)', 
            'rgba(255, 99, 132, 0.8)',
        ],
        '檢視各方看法並分析':[
            'rgba(54, 162, 235, 0.8)', 
            'rgba(255, 99, 132, 0.8)',
        ],
    }
    
    $.ajax({
        url:'/api/result',
        success:function(datas){
            bar = ['年齡','觀看政見']
            datas['年齡']={
                '20以下':datas['年齡']['20以下'],
                '20-29':datas['年齡']['20-29'],
                '30-39':datas['年齡']['30-39'],
                '40-49':datas['年齡']['40-49'],
                '50-59':datas['年齡']['50-59'],
                '60以上':datas['年齡']['60以上']
            }
            datas['性別'] = {
                '男':datas['性別']['男'],
                '女':datas['性別']['女'],
            }
            datas['教育程度'] = {
                '國小以下':datas['教育程度']['國小以下'],
                '國中':datas['教育程度']['國中'],
                '高中/職':datas['教育程度']['高中/職'],
                '大專院校':datas['教育程度']['大專院校'],
                '碩士':datas['教育程度']['碩士'],
                '博士':datas['教育程度']['博士'],
            }
            datas['觀看政見'] = {
                '柯文哲':datas['觀看政見']['柯文哲'],
                '侯友宜':datas['觀看政見']['侯友宜'],
                '賴清德':datas['觀看政見']['賴清德'],
            }
            datas['觀看政見前'] = {
                '民眾黨':datas['觀看政見前']['民眾黨'],
                '國民黨':datas['觀看政見前']['國民黨'],
                '民進黨':datas['觀看政見前']['民進黨'],
                '其他':datas['觀看政見前']['其他'],
            }
            datas['觀看政見後'] = {
                '民眾黨':datas['觀看政見後']['民眾黨'],
                '國民黨':datas['觀看政見後']['國民黨'],
                '民進黨':datas['觀看政見後']['民進黨'],
                '其他':datas['觀看政見後']['其他'],
            }
            datas['主動查詢各候選人的政見'] = {
                '有':datas['主動查詢各候選人的政見']['有'],
                '無':datas['主動查詢各候選人的政見']['無'],
            }
            datas['媒體識讀能力'] = {
                '有':datas['媒體識讀能力']['有'],
                '無':datas['媒體識讀能力']['無'],
            }
            datas['查證新聞內容'] = {
                '有':datas['查證新聞內容']['有'],
                '無':datas['查證新聞內容']['無'],
            }
            datas['檢視各方看法並分析'] = {
                '有':datas['檢視各方看法並分析']['有'],
                '無':datas['檢視各方看法並分析']['無'],
            }
            for(bk in bar){
                new Chart($('[chart="'+bar[bk]+'"]').get(0).getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: Object.keys(datas[bar[bk]]),
                        datasets: [{
                            label: bar[bk],
                            data: Object.values(datas[bar[bk]]),
                            backgroundColor: bgcs[bar[bk]],
                        }]
                    }
                });
            }
            pies=['性別','縣市','教育程度','觀看政見前','觀看政見後','主動查詢各候選人的政見','媒體識讀能力','查證新聞內容','檢視各方看法並分析'];
            for(pk in pies){
                new Chart($('[chart="'+pies[pk]+'"]').get(0).getContext('2d'), {
                    type: 'pie',
                    data: {
                        labels: Object.keys(datas[pies[pk]]),
                        datasets: [{
                            label: pies[pk],
                            data: Object.values(datas[pies[pk]]),
                            backgroundColor: bgcs[pies[pk]]
                        }]
                    }
                });
            }
            tes=['候選人評分1','候選人評分2']
            for(tk in tes){
                html_th = '';
                html_td1 = '';
                html_td2 = '';
                datas[tes[tk]] = {
                    '柯文哲':datas[tes[tk]]['柯文哲'],
                    '侯友宜':datas[tes[tk]]['侯友宜'],
                    '賴清德':datas[tes[tk]]['賴清德'],
                }
                for(tstk in datas[tes[tk]]){
                    tstv = datas[tes[tk]][tstk];
                    html_th += '<th colspan="5">'+tstk+'</th>';
                    html_td1+='<td>'+tstv[5]+'</td><td>'+tstv[4]+'</td><td>'+tstv[3]+'</td><td>'+tstv[2]+'</td><td>'+tstv[1]+'</td>';
                    html_td2+='<td colspan=5>均分：'+Math.floor(((tstv[5]*5+tstv[4]*4+tstv[3]*3+tstv[2]*2+tstv[1])/(tstv[5]+tstv[4]+tstv[3]+tstv[2]+tstv[1]))*10)/10+'</td>';
                }
                $('[table="'+tes[tk]+'"]').html('<table class="table table-striped table-bordered table-hover text-center"><tr>'+html_th+'</tr><tr><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td></tr><tr>'+html_td1+'</tr><tr>'+html_td2+'</tr></table>')
            }
        }
    })
})