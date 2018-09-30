from django.core.exceptions import ValidationError
from common.utils import n_spatial_moments as moments
from common.models import DomainUrl, HtmlVector
from batch.model_converter import HtmlVectorModelConverter
from batch.vectorize import HtmlVectorize
from sklearn import svm, linear_model
import numpy as np
import re

class SvmClassifier:
    def __init__(self, kernel='rbf'):
        self._did_learn = False
        self.vectorizor = HtmlVectorize(HtmlVector.VECTOR_INDICES)
        self.clf = svm.SVC(kernel='rbf', gamma='scale')
        print('learn through svm with %s kernel' %kernel)
        # self.reg = linear_model.Ridge(alpha = .5)
    
    @property
    def did_learn(self):
        return self._did_learn
    
    @did_learn.setter
    def did_learn(self, flg):
        if not isinstance(flg, bool):
            raise TypeError('flg has to be bool')
        self._did_learn = flg
    
    def _pre_process(self, data, deg=5, with_norm=True, m_flg=True, c_flg=True, n_flg=True):
        moms = moments(data, deg, with_norm=with_norm, with_label=True)
        data = []
        for key in moms.keys():
            if re.search(r'^nu[0-9]*', key):
                if n_flg:
                    data.append(moms[key])
            if re.search(r'^m[0-9]*', key):
                if m_flg:
                    data.append(moms[key])
                pass
            if re.search(r'^mu[0-9]*', key):
                if c_flg:
                    data.append(moms[key])
                pass
        return np.array(data)
    
    def _question_to_teacher(self, data):
        return 0
    
    def learn(self, pre_processed_data_set, result_set):
        self.clf.fit(pre_processed_data_set, result_set)
        # self.reg.fit(pre_processed_data_set, result_set)
        self.did_learn = True
    
    def teach(self, deg=5, with_norm=True, m_flg=True, c_flg=True, n_flg=True,
              id_list=[74, 505, 506, 507, 508, 510, 521, 678, 683, 684, 685, 686, 687, 689, 690, 691],
              f_leng=16):
        pre_processed_data_set = []
        result_set = []
        '''
        print('%s deg' % str(deg))
        
        print('%s normalize' % ('with' if with_norm  else 'without'))
        
        print('%s c_flg' % ('with' if c_flg  else 'without'))
        
        print('%s n_flg' % ('with' if n_flg  else 'without'))
        
        print('%s m_flg' % ('with' if m_flg  else 'without'))
        '''
        for model in DomainUrl.objects.filter(is_notice__exact=1).filter(pk__in = id_list):
            set = HtmlVector.objects.filter(url__exact=model)
            if not set.exists():
                continue
            self.vectorizor.reset_vector_set()
            self.vectorizor.vectorize(query_set=set)
            pre_processed_data_set.append(self._pre_process(self.vectorizor.get_vector_set(),deg=5, with_norm=True, m_flg=True, c_flg=True, n_flg=True))
            result_set.append(1)
        len_pr_for_s = len(pre_processed_data_set)
        print('notice sample\'s length is %s ' % str(len_pr_for_s))
        
        for model in DomainUrl.objects.filter(is_notice__exact=0)[:f_leng]:
            set = HtmlVector.objects.filter(url__exact=model)
            if not set.exists():
                continue
            self.vectorizor.reset_vector_set()
            self.vectorizor.vectorize(query_set=set)
            pre_processed_data_set.append(self._pre_process(self.vectorizor.get_vector_set(),deg=5, with_norm=True, m_flg=True, c_flg=True, n_flg=True))
            result_set.append(0)
        
        print('not notice sample\'s length is %s ' % str(len(pre_processed_data_set) - len_pr_for_s))
        
        '''
        for model in DomainUrl.objects.all().order_by('id')[:650]:
            set = HtmlVector.objects.filter(url__exact=model)
            if not set.exists():
                continue
            self.vectorizor.reset_vector_set()
            self.vectorizor.vectorize(query_set=set)
            pre_processed_data_set.append(self._pre_process(self.vectorizor.get_vector_set()))
            result_set.append(model.is_notice)
        
        sr = 0;
        fr = 0;
        for r in result_set:
            if r == 1:
                sr += 1
            else:
                fr += 1
        print('sr is %s ' % str(sr))
        print('fr is %s ' % str(fr))
        '''
        self.learn(pre_processed_data_set, result_set)
    
    def classify(self, data):
        if not self._did_learn:
            raise ValidationError('befor classify you have to learn the classifier')
        data = self._pre_process(data)
        result = self.clf.predict([data])
        # print(self.reg.predict([data]))
        return result[0]
    
    def test_result(self, id_list=[74, 505, 506, 507, 508, 510, 521, 678, 683, 684, 685, 686, 687, 689, 690, 691],
                    f_leng = 16):
        
        st_count = 0
        ss_count = 0;
        sf_count = 0;
        for model in DomainUrl.objects.filter(is_notice__exact=1).exclude(pk__in = id_list):
            set = HtmlVector.objects.filter(url__exact=model)
            if not set.exists():
                continue
            st_count += 1
            self.vectorizor.reset_vector_set()
            self.vectorizor.vectorize(query_set=set)
            result = self.classify(self.vectorizor.get_vector_set())
            if result:
                ss_count += 1
            else:
                sf_count += 1
        
        print('ss_prop is %s' % str(ss_count/st_count*100))
        print('sf_prop is %s' % str(sf_count/st_count*100))
        
        ft_count = 0
        fs_count = 0;
        ff_count = 0;
        
        for model in DomainUrl.objects.filter(is_notice__exact=0)[f_leng : f_leng*2]:
            set = HtmlVector.objects.filter(url__exact=model)
            if not set.exists():
                continue
            ft_count += 1
            self.vectorizor.reset_vector_set()
            self.vectorizor.vectorize(query_set=set)
            result = self.classify(self.vectorizor.get_vector_set())
            if not result:
                fs_count += 1
            else:
                ff_count += 1
        '''
        print('fs_prop is %s' % str(fs_count/ft_count*100))
        print('ff_prop is %s' % str(ff_count/ft_count*100))
        
        print('s_prop is %s' % str((fs_count + ss_count)/(st_count + ft_count)*100))
        print('f_prop is %s' % str((sf_count + ff_count)/(st_count + ft_count)*100))
        '''
        '''
        t_count = 0
        s_count = 0;
        f_count = 0;
        for model in DomainUrl.objects.all().order_by('id')[650:]:
            set = HtmlVector.objects.filter(url__exact=model)
            if not set.exists():
                continue
            t_count += 1
            self.vectorizor.reset_vector_set()
            self.vectorizor.vectorize(query_set=set)
            result = self.classify(self.vectorizor.get_vector_set())
            if model.is_notice == 1:
                print('success !')
            if result == model.is_notice:
                s_count += 1
            else:
                f_count += 1
        print('ss_prop is %s' % str(s_count/t_count*100))
        print('sf_prop is %s' % str(f_count/t_count*100))
        '''
        return (st_count, ss_count, sf_count, ft_count, fs_count, ff_count)
        
