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
}