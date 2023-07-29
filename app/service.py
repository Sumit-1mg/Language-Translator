from app.routes.routes import app

if __name__ == '__main__':
    app.run(auto_reload=True)

# TO DO: Use listeners to check api is available or not if api is not available then do not start server.
