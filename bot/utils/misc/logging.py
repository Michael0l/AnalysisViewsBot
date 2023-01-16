import logging

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    filename='logging.log',
                    filemode='a',
                    level=logging.WARNING,
                    )
