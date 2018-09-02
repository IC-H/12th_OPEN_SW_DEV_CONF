NoticeUlrJsObj = {
    searchAjax : function() {
        var keyWords = $('#key-words');
        var url      = keyWords.data('url').request;
        searchModel  = new ModelAjax(url);
        searchModel.setData({
           keyWrods            : keyWords.val(),
           csrfmiddlewaretoken : $('input[name="csrfmiddlewaretoken"]').val()
       });
        searchModel.setSuccessCallBack(function(data) {
           console.info(data);
        });
        CommonJs.ajax(searchModel);
    },
};
