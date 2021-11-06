from application import application
from apps.crawller import sched

if __name__ == '__main__':
    sched.start()
    application.debug = True
    application.env = "development"
    application.run()
