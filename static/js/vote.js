$(function(){
    tzc = $('#tzc').twzipcode({
        'css': [
            'addr-county col-md-5 form-select', //縣市
            'addr-district col-md-5 form-select',  // 鄉鎮市區
        ],
    });
    county = $('#tzc').attr('county');
    district = $('#tzc').attr('district');
    if(county.length){
        $('[name="county"]').val(county).change()
    }
    if(district.length){
        $('[name="district"]').val(district)
    }
})