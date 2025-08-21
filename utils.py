from math import ceil

# Dummy function, replace with real DB channel search
async def get_search_results(channel_id, query):
    # This should return a list of objects with file_name, file_size, language, file_id
    # Example:
    return [
        type("File", (), {"file_name": "Avatar (2009)", "file_size": 1572864000, "language": "EN", "file_id": 12345})(),
        type("File", (), {"file_name": "Avatar 2 (2022)", "file_size": 2254857830, "language": "EN/FR", "file_id": 12346})()
    ]

def get_size(size_bytes):
    # Convert bytes to human-readable
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(ceil((len(str(size_bytes))-1)/3))
    p = pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"
