from application import application

if __name__ == '__main__':
    application.debug = True
    application.env = "development"
    application.run()
