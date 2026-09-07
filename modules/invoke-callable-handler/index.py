def invoke_callable_handler(func, args=(), kwargs=None) -> dict:
    if not callable(func):
        return {"result": None, "success": False, "error": "Đối tượng truyền vào không phải là callable"}

    if kwargs is None:
        kwargs = {}

    try:
        res = func(*args, **kwargs)
        return {"result": res, "success": True, "error": None}
    except Exception as e:
        return {"result": None, "success": False, "error": str(e)}
