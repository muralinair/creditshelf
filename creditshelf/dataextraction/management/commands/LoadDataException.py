class LoadDataExeception(Exception):
    def __init__(self,mesg,errObj=None):
        self.mesg = mesg
        self.errObj = errObj
