from js import Response, Headers, fetch

async def on_fetch(request, env, ctx):
    url:str = request.url
    response = await env.Assets.fetch(request)
    content_type = response.headers.get("content-type")
    headers = Headers.new()
    headers.append("content-type", content_type)
    return Response.new(response.body, headers=headers, status=response.status)