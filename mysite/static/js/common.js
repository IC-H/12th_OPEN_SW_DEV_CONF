class CommonJs {
	static ajax(model) {
	    if (!(model instanceof ModelAjax)) {
	        alert('It is not a Model for ajax');
	        return false;
	    } else if (!model.isPrepared()) {
	        alert('This model is not prepared to send');
	        return false;
	    }
	    $.ajax({
	        type       : model.type,
	        url        : model.url,
	        dataType   : model.dataType,
	        data       : model.data
	    }).done(function(data) {
	        model.successCallBack(data);
	    }).fail(function(data) {
	        if (typeof model.failureCallBack === 'function') {
	            model.failureCallBack(data);
	        } else {
	            alert('fail to ajax');
	        }
	    });
	    return false;
	}
	
	static accordionClickEvent(element) {
	    var panel = $(element).parents('.accordion-row').find('.panel');
	    if (panel.is(':visible')) {
	        panel.hide();
	    } else {
	        panel.show();
	    }
	    return false;
	}
	
	static accordionPanelClickEvent(element) {
	    var panel = $(element);
	    if (panel.attr('checked')) {
	        panel.removeAttr('checked');
	    } else {
            panel.attr('checked', 'checked');
	    }
	}
}