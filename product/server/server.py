import uvicorn



if __name__ == '__main__':
        # run server for backend
        uvicorn.run("controllers.main:app", host="0.0.0.0", port=5000, reload=True)