from shopper.search_courses import matched_courses

def test():
    shopper.create_app(config).app_context().push()
    order = 'dept'
    search = 'cos'
    page = "1"
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    #print(len(results))
    #print("HLOOW)")

test()