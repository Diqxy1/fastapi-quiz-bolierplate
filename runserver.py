import uvicorn

from src.config.env import env

if __name__ == '__main__':
    reload = True if env.get_item(key='ENVIROMENT', default='production') == 'development' else False
    host = env.get_item(key='HOST', default='0.0.0.0')
    port = int(env.get_item(key='PORT', default=8000))

    uvicorn.run(
        "application:app",
        host=host,
        port=port,
        reload=reload
    )