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
           var accordionHtml = $('#hidden-accordion .accordion-row');
           var panelHtml     = accordionHtml.find('.panel');
           var urlListHtml   = $('.url-list');
           var domainList    = data.domain_list;
           urlListHtml.find('.accordion-row').remove();
           $.each(domainList, function(key, value) {
               tmpAccordion = accordionHtml.clone();
               tmpAccordion.find('.panel').remove();
               tmpAccordion.find('.accordion p').text(value.domain);
               value.url_list.forEach(function(url) {
                   tmpPanel     = panelHtml.clone();
                   tmpPanel.find('p').text(url);
                   tmpAccordion.append(tmpPanel);
               });
               urlListHtml.append(tmpAccordion);
           });
           
        });
        CommonJs.ajax(searchModel);
    },
};
