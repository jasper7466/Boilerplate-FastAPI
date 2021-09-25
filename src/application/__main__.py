if __name__ == '__main__':
    import uvicorn
    uvicorn.run('application.app:app', port=5000, debug=True)
