from django.core.exceptions import ValidationError
from common.utils import n_spatial_moments as moments
from common.models import DomainUrl, HtmlVector
from batch.vectorize import HtmlVectorize
from sklearn import svm, linear_model
import numpy as np
import re
from . import BaseClassifier

class SvmClassifier(BaseClassifier):
    
    """
    Classifier for classifying URL for notice or not
    For that, this classifier is learned by SVM method
    
    For teaching the classifier 
    """
    
    class Meta:
        result_file_name = 'SVM_RESULT.sav'
    
    def __init__(self):
        super().__init__()
        self.vectorizor = HtmlVectorize(HtmlVector.VECTOR_INDICES)
    
    def set_model(self, kernel='rbf', deg=5, with_norm=True, m_flg=True, c_flg=True, n_flg=True):
        self.model = svm.SVC(kernel=kernel, gamma='scale')
        self.deg = deg
        self.with_norm = with_norm
        self.m_flg = m_flg
        self.c_flg = c_flg
        self.n_flg = n_flg
    
    def _pre_process(self, data):
        """
        preprocess by converting vector to moments
        
        `data` is raw data assumed with array of vector
        
        `deg` is degree of moments which non-negative integer
        
        `with_norm` is flag for normalization of data
        
        `m_flg` is flag for using spatial moments
        
        `c_flg` is flag for using central moments
        
        `n_flg` is flag for using central normalized moments
        """
        moms = moments(data, self.deg, with_norm=self.with_norm, with_label=True)
        data = []
        for key in moms.keys():
            if re.search(r'^nu[0-9]*', key):
                # central normalized moments
                if self.n_flg:
                    data.append(moms[key])
            if re.search(r'^m[0-9]*', key):
                # spatial moments
                if self.m_flg:
                    data.append(moms[key])
            if re.search(r'^mu[0-9]*', key):
                # central moments
                if self.c_flg:
                    data.append(moms[key])
        return np.array(data)
    
    def learn(self, pre_processed_data_set, result_set):
        self.model.fit(pre_processed_data_set, result_set)
        self.did_learn = True
    
    def teach(self, s_count=20, f_count=20):
        """
        learning process
        
        `data` is raw data assumed with array of vector
        
        `deg` is degree of moments which non-negative integer
        
        `with_norm` is flag for normalization of data
        
        `m_flg` is flag for using spatial moments
        
        `c_flg` is flag for using central moments
        
        `n_flg` is flag for using central normalized moments
        
        `s_count` is count of what times teach notice URL
        
        `f_count` is count of what times teach not-notice URL
        """
        pre_processed_data_set = []
        result_set = []
        for model in DomainUrl.objects.filter(is_notice__exact=1)[:s_count]:
            set = HtmlVector.objects.filter(url__exact=model)
            if not set.exists():
                continue
            self.vectorizor.reset_vector_set()
            self.vectorizor.vectorize(query_set=set)
            pre_processed_data_set.append(self._pre_process(self.vectorizor.get_vector_set()))
            result_set.append(1)
        
        for model in DomainUrl.objects.filter(is_notice__exact=0)[:f_count]:
            set = HtmlVector.objects.filter(url__exact=model)
            if not set.exists():
                continue
            self.vectorizor.reset_vector_set()
            self.vectorizor.vectorize(query_set=set)
            pre_processed_data_set.append(self._pre_process(self.vectorizor.get_vector_set()))
            result_set.append(0)
        
        self.learn(pre_processed_data_set, result_set)
    
    def classify(self, data):
        data = self._pre_process(data)
        result = self.model.predict([data])
        return result[0]
