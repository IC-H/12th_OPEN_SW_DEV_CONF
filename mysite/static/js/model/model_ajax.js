class ModelAjax {
    constructor(url, type='POST') {
        this.url              = url;
        this.type             = type;
        this.dataType         = 'json';
        this.data             = {};
        this.successCallBack  = null;
        this.failureCallBack  = null; 
        this.httpMethods      = ['POST', 'GET', 'PUT'];
    }

    setData(data) {
        var obj = {};
        if (Array.isArray(data)) {
            data.forEach(function(value, index) {
                obj[index] = value;
            });
        } else if (typeof data === 'object') {
            obj = data;
        }
        this.data = obj;
    }

    setSuccessCallBack(callback) {
        var func = null;
        if (typeof callback === 'function') {
            func = callback;
        }
        this.successCallBack = func;
    }
    
    setFailureCallBack(callback) {
        var func = null;
        if (typeof callback === 'function') {
            func = callback;
        }
        this.failureCallBack = func;
    }
    
    isPrepared() {
        if (typeof this.url !== 'string' || StringUtil.isEmpty(this.url)) {
            return false;
        }
        if (typeof this.type !== 'string' || this.httpMethods.indexOf(this.type) === -1) {
            return false;
        }
        if (typeof this.successCallBack !== 'function') {
            return false;
        }
        if (this.failureCallBack !== null && typeof this.failureCallBack !== 'function') {
            return false;
        }
        return true;
    }
};
