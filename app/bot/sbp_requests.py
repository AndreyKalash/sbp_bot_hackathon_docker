from aiohttp import ClientSession


async def create_qr(data, headers):
    async with ClientSession() as session:
        response = await session.post(
            "https://pay-test.raif.ru/api/sbp/v2/qrs", json=data, headers=headers
        )

        qr_data = await response.json()
    return qr_data


async def qr_status(qr_id, headers):
    async with ClientSession() as session:
        resp = await session.get(
            f"https://pay-test.raif.ru/api/sbp/v1/qr/{qr_id}/payment-info",
            headers=headers,
        )
        resp_json = await resp.json()

    return resp_json
