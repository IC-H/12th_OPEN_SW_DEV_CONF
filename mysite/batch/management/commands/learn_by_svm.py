from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DatabaseError
from batch.learning import SvmClassifier
import re

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('thread_num', nargs='?', type=int, default=10)
    
    def handle(self, *args, **options):
        try:
            test_case = []
            id_list = [74, 140, 505]
            for kernel in ['sigmoid', 'rbf']:
                for deg in range(0, 1):
                    for with_norm in [True, False]:
                        for m_flg in [True, False]:
                            for c_flg in [True, False]:
                                for n_flg in [True, False]:
                                    for id_len in range(2, len(id_list)):
                                        for f_leng in [int(id_len/2), id_len - 1, id_len + 1 , id_len*2]:
                                            classifier = SvmClassifier(kernel=kernel)
                                            classifier.teach(deg=deg, with_norm=with_norm, m_flg=m_flg, c_flg=c_flg,
                                                             n_flg=n_flg, id_list=id_list[:id_len], f_leng=f_leng)
                                            st_count, ss_count, sf_count, ft_count, fs_count, ff_count = classifier.test_result(id_list=id_list[:id_len], f_leng=f_leng)
                                            tmp ={}
                                            tmp['deg'] = deg
                                            tmp['with_norm'] = with_norm
                                            tmp['m_flg'] = m_flg
                                            tmp['c_flg'] = c_flg
                                            tmp['n_flg'] = n_flg
                                            tmp['id_list'] = len(id_list[:id_len])
                                            tmp['f_leng'] = f_leng
                                            tmp['st_count'] = st_count
                                            tmp['ss_count'] = ss_count
                                            tmp['sf_count'] = sf_count
                                            tmp['ft_count'] = ft_count
                                            tmp['fs_count'] = fs_count
                                            tmp['ff_count'] = ff_count
                                            test_case.append(tmp)
            f_d = open('test_result.csv', 'a+')
            str = ''
            for case_label in test_case[0].keys():
                str = str + case_label + ','
            str = re.sub(',$', '\n', str)
            for case in test_case:
                for value in case.values():
                    str = str + str(value) + ','
                str = re.sub(',$', '\n', str)
            f_d.close()
        except CommandError as e:
            print(e)
        except ValidationError as e:
            print(e)
        except (IntegrityError, DatabaseError) as e:
            print(e)
        except Exception as e:
            print(e)
