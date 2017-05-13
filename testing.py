from shopper.search_courses import matched_courses
import shopper
import config

def test():
    shopper.create_app(config).app_context().push()

    #test case 1
    order = 'dept'
    search = 'cos'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'COS109 COS126 COS217 COS226 COS318 COS324 COS326 COS333 COS340 COS397 COS418 COS429 ':
    	print("TEST 1 FAILED")


    #test case 2
    order = 'dept'
    search = 'phi em'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'CHV310 PHI306 PHI319 PHI337 PHI380 ':
    	print("TEST 2 FAILED")


    #test case 3
    order = 'dept'
    search = 'stars'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'AST205 ':
    	print("TEST 3 FAILED")
    
    #test case 4
    order = 'dept'
    search = 'aaS Sa'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'AAS201 AAS301 LAS371 REL377 ':
    	print("TEST 4 FAILED")


    #test case 5
    order = 'dept'
    search = 'geo atmospheric'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'AOS527 CEE305 GEO427 ':
    	print("TEST 5 FAILED")

    #test case 6
    order = 'dept'
    search = 'orf mat'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'ORF309 ':
    	print("TEST 6 FAILED")

    #test case 7
    order = 'rating'
    search = 'ecs'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'COM362 COM341 HIS364 GER308 ECS301 ECS311 ITA322 COM370 GER475 ':
    	print("TEST 7 FAILED")

    #test case 8
    order = 'rating'
    search = 'materialS maE'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'MSE501 MAE597 MAE324 ENE506 ':
    	print("TEST 8 FAILED")

    #test case 9
    order = 'dept'
    search = 'la urb'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'ARC205 SPA227 URB202 ':
    	print("TEST 9 FAILED")

    #test case 10
    order = 'dept'
    search = 'pdf dan'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'DAN207 DAN210 DAN211 DAN213 DAN216 DAN319A DAN319B DAN320A DAN320B DAN419A DAN419B DAN420A ':
    	print("TEST 10 FAILED")

    #also test 2nd page for case 10
    page = '2'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'DAN420B ':
    	print("TEST 11 FAILED")

    #test case 12
    order = 'dept'
    search = 'ec'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
        result += course.dept + course.catalog_number + ' '
    if result != 'ANT326 CGS310 ECS311 GER306 GER308 LIN201 LIN260 LIN302 LIN310 LIN360 PHI203 PHI207 ':
        print("TEST 12 FAILED")

    #test case 13
    order = 'dept'
    search = 'cos qr phi em'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
        result += course.dept + course.catalog_number + ' '
    if len(result) != 0:
        print("TEST 13 FAILED")

    #test case 14
    order = 'dept'
    search = 'ISC'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
        result += course.dept + course.catalog_number + ' '
    if result != 'ISC231 ISC232 ISC335 ':
        print("TEST 14 FAILED")

    #test case 15
    order = 'dept'
    search = 'cos sa'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
        result += course.dept + course.catalog_number + ' '
    if result != '':
        print("TEST 15 FAILED")

test()