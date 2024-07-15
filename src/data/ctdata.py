import os
from data import srdata

class CTDATA(srdata.SRData):
    def __init__(self, args, name='CTDATA', train=True, benchmark=False):
        data_range = [r.split('-') for r in args.data_range.split('/')]
        if train:
            data_range = data_range[0]
        else:
            if args.test_only and len(data_range) == 1:
                data_range = data_range[0]
            else:
                data_range = data_range[1]

        self.begin, self.end = list(map(lambda x: int(x), data_range))
        #  If data_range is [['0', '255'], ['0', '255']], after this line of code, self.begin will be 0 and self.end will be 255.
        super(CTDATA, self).__init__(
            args, name=name, train=train, benchmark=benchmark
        )

    def _scan(self):
        names_hr, names_lr = super(CTDATA, self)._scan()
        names_hr = names_hr[self.begin - 1:self.end]
        names_lr = [n[self.begin - 1:self.end] for n in names_lr]

        return names_hr, names_lr

    def _set_filesystem(self, dir_data):
        super(CTDATA, self)._set_filesystem(dir_data)
        self.dir_hr = os.path.join(self.apath, 'CTDATA_train_HR')
        self.dir_lr = os.path.join(self.apath, 'CTDATA_train_LR_bicubic')
        if self.input_large: self.dir_lr += 'L'
# The purpose of this method is to build file paths for high and low resolution images based on root directories and data set names for subsequent data loading and processing