from app import application
# instead of running the backend using flask we can run it with python using this file
if __name__ == '__main__':
    application.run(debug=True)