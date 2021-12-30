from aiohttp import web
import atomic_store

async def getTemp(request):
    with atomic_store.open('src/resources/digital_twin.json', default=dict()) as store:
        dt = store.value
        props = dt["features"]["measurements"]["properties"]
        return web.json_response({"temp": props["temperature"]["data"]})


async def getHum(request):
    with atomic_store.open('src/resources/digital_twin.json', default=dict()) as store:
        dt = store.value
        props = dt["features"]["measurements"]["properties"]
        return web.json_response({"hum": props["humidity"]["data"]})


async def getPress(request):
    with atomic_store.open('src/resources/digital_twin.json', default=dict()) as store:
        dt = store.value
        props = dt["features"]["measurements"]["properties"]
        return web.json_response({"press": props["pressure"]["data"]})


async def getCO2TVOCs(request):
    with atomic_store.open('src/resources/digital_twin.json', default=dict()) as store:
        dt = store.value
        props = dt["features"]["measurements"]["properties"]
        return web.json_response({"co2": props["co2"]["data"], "tvoc": props["tvoc"]["data"]})


async def getQuality(request):
    with atomic_store.open('src/resources/digital_twin.json', default=dict()) as store:
        dt = store.value
        props = dt["features"]["measurements"]["properties"]
        return web.json_response({"qual": props["quality"]["data"]})


async def getRain(request):
    with atomic_store.open('src/resources/digital_twin.json', default=dict()) as store:
        dt = store.value
        props = dt["features"]["measurements"]["properties"]
        return web.json_response({"rain": props["rain"]["data"]})


async def getUV(request):
    with atomic_store.open('src/resources/digital_twin.json', default=dict()) as store:
        dt = store.value
        props = dt["features"]["measurements"]["properties"]
        return web.json_response({"uv": props["uv"]["data"]})


async def getWind(request):
    with atomic_store.open('src/resources/digital_twin.json', default=dict()) as store:
        dt = store.value
        props = dt["features"]["measurements"]["properties"]
        return web.json_response({"wind": props["wind"]["data"]})

app = web.Application()
app.add_routes([web.get('/api/temp', getTemp),
                web.get('/api/hum', getHum),
                web.get('/api/press', getPress),
                web.get('/api/co2TVOC', getCO2TVOCs),
                web.get('/api/qual', getQuality),
                web.get('/api/rain', getRain),
                web.get('/api/uv', getUV),
                web.get('/api/wind', getWind)])


if __name__ == '__main__':
    web.run_app(app)