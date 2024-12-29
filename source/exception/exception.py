import sys


def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred python script name [{0}] line number [{1}] error message [{2}]".format(file_name, exc_tb.tb_lineno, str(error))
    return error_message

class customexception(Exception):
    def __init__(self,error_message, error_detail:sys):       
        self.error_message=error_message
        _,_,exc_tb = error_detail.exc_info()
        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename  
   
    def __str__(self):
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
            self.file_name, self.lineno, str(self.error_message))


if __name__ =="__main__":
    try:
        a= 1/0
    except Exception as e:
        raise customexception(e,sys)
    

