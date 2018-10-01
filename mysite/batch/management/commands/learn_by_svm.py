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
            classifier = SvmClassifier()
            result_prop = 0
            for kernel in ['sigmoid', 'rbf']:
                for deg in range(0, 7):
                    for with_norm in [True, False]:
                        for m_flg in [True, False]:
                            for c_flg in [True, False]:
                                for n_flg in [True, False]:
                                    for s_count in range(10, 20, 2):
                                        for f_count in [int(s_count/2), s_count, s_count*2]:
                                            if not m_flg and not c_flg and not n_flg:
                                                # If three flag are False then data set will be empty
                                                continue
                                            elif deg < 2 and not m_flg:
                                                # with deg < 2 other flag has no power
                                                continue
                                            classifier.set_model(kernel, deg=deg, with_norm=with_norm, m_flg=m_flg, c_flg=c_flg, n_flg=n_flg)
                                            classifier.teach(s_count=s_count, f_count=f_count)
                                            st_count, ss_count, ft_count, fs_count = classifier.test_result(s_count, f_count)
                                            tmp_result_prop = (ss_count + fs_count)/(st_count+ ft_count) *100
                                            if result_prop < tmp_result_prop:
                                                classifier.save_result()
        except CommandError as e:
            print(e)
        except ValidationError as e:
            print(e)
        except (IntegrityError, DatabaseError) as e:
            print(e)
