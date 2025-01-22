def get_num_workers():
    import multiprocessing

    return (multiprocessing.cpu_count() * 2) + 1


bind = "0.0.0.0:8000"
# workers= get_num_workers()
workers = 1
