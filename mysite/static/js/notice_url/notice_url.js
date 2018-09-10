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
           var urlListHtml   = $('.url-list');
           var domainList    = data.domain_list;
           urlListHtml.find('.accordion-row').hide();
           urlListHtml.find('.panel').hide();
           $.each(domainList, function(key, value) {
               var tmpAccordion = urlListHtml.find('.accordion-row p:contains(' + value.domain + ')').parents('.accordion-row');
               tmpAccordion.show();
               $.each(value.url_list, function(key, url) {
                   tmpAccordion.find('.panel p:contains(' + url + ')').parents('.panel').show();
               });
           });
        });
        CommonJs.ajax(searchModel);
    },
    submitToUrlRegister : function(event) {
        event.preventDefault();
        var formObj     = $('#notice-search-form');
        var checkedList = $('.accordion-row .panel[checked="checked"]');
        checkedList.each(function(key, element) {
            formObj.append('<input type="hidden" name="url_id_list[]" value="' + $(element).data('key') + '"/>');
        });
        formObj.submit();
    }
};
