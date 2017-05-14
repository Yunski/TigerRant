from shopper.search_courses import matched_courses
import shopper
import config
import time
import sys

def test():
    shopper.create_app(config).app_context().push()
    begin = time.time()
    testsfailed = ""

    #test case 1
    order = 'dept'
    search = 'cos'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'COS109 COS126 COS217 COS226 COS318 COS324 COS326 COS333 COS340 COS397 COS418 COS429 ':
    	testsfailed += "TEST 1 FAILED (search was: 'cos')\n"


    #test case 2
    order = 'dept'
    search = 'phi em'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'CHV310 PHI306 PHI319 PHI337 PHI380 ':
    	testsfailed += "TEST 2 FAILED (search was: 'phi em')\n"


    #test case 3
    order = 'dept'
    search = 'stars'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'AST205 ':
    	testsfailed += "TEST 3 FAILED (search was: 'stars')\n"
    
    #test case 4
    order = 'dept'
    search = 'aaS Sa'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'AAS201 AAS301 LAS371 REL377 ':
    	testsfailed += "TEST 4 FAILED (search was: 'aaS Sa')\n"


    #test case 5
    order = 'dept'
    search = 'geo atmospheric'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'AOS527 CEE305 GEO427 ':
    	testsfailed += "TEST 5 FAILED (search was: 'geo atmospheric')\n"

    #test case 6
    order = 'dept'
    search = 'orf mat'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'ORF309 ':
    	testsfailed += "TEST 6 FAILED (search was: 'orf mat')\n"

    #test case 7
    order = 'rating'
    search = 'ecs'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'COM362 COM341 HIS364 GER308 ECS301 ECS311 ITA322 COM370 GER475 ':
    	testsfailed += "TEST 7 FAILED  (search was: 'ecs')\n"

    #test case 8
    order = 'rating'
    search = 'materialS maE'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'MSE501 MAE597 MAE324 ENE506 ':
    	testsfailed += "TEST 8 FAILED  (search was: 'materialS maE')\n"

    #test case 9
    order = 'dept'
    search = 'la urb'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'ARC205 SPA227 URB202 ':
    	testsfailed += "TEST 9 FAILED (search was: 'la urb')\n"

    #test case 10
    order = 'dept'
    search = 'pdf dan'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'DAN207 DAN210 DAN211 DAN213 DAN216 DAN319A DAN319B DAN320A DAN320B DAN419A DAN419B DAN420A ':
    	testsfailed += "TEST 10 FAILED (search was: 'pdf dan')\n"

    #also test 2nd page for case 10
    page = '2'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
    	result += course.dept + course.catalog_number + ' '
    if result != 'DAN420B ':
    	testsfailed += "TEST 11 FAILED (search was: 'pdf dan', page: 2)\n"

    #test case 12
    order = 'dept'
    search = 'ec'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
        result += course.dept + course.catalog_number + ' '
    if result != 'ANT326 CGS310 ECS311 GER306 GER308 LIN201 LIN260 LIN302 LIN310 LIN360 PHI203 PHI207 ':
        testsfailed += "TEST 12 FAILED (search was: 'ec')\n"

    #test case 13
    order = 'dept'
    search = 'cos qr phi em'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
        result += course.dept + course.catalog_number + ' '
    if len(result) != 0:
        testsfailed += "TEST 13 FAILED (search was: 'cos qr phi em')\n"

    #test case 14
    order = 'dept'
    search = 'ISC'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
        result += course.dept + course.catalog_number + ' '
    if result != 'ISC231 ISC232 ISC335 ':
        testsfailed += "TEST 14 FAILED (search was: 'ISC')\n"

    #test case 15
    order = 'dept'
    search = 'cos sa'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
        result += course.dept + course.catalog_number + ' '
    if result != '':
        testsfailed += "TEST 15 FAILED (search was: 'cos sa')\n"

    #test case 16
    order = 'dept'
    search = 'planets'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
        result += course.dept + course.catalog_number + ' '
    if result != 'AST205 GEO255A ':
        testsfailed += "TEST 16 FAILED (search was: 'planets')\n"

    #test case 17
    order = 'dept'
    search = 'ant          rel'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
        result += course.dept + course.catalog_number + ' '
    if result != 'ANT208 ':
        testsfailed += "TEST 17 FAILED (search was: 'ant          rel')\n"

    #test case 18
    order = 'dept'
    search = '     ec'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
        result += course.dept + course.catalog_number + ' '
    if result != 'ANT326 CGS310 ECS311 GER306 GER308 LIN201 LIN260 LIN302 LIN310 LIN360 PHI203 PHI207 ':
        testsfailed += "TEST 18 FAILED (search was: '     ec')\n"

    #test case 18
    order = 'dept'
    search = 'language identity power'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
        result += course.dept + course.catalog_number + ' '
    if result != 'ANT326 ':
        testsfailed += "TEST 19 FAILED (search was: 'language identity power')\n"

    #test case 18
    order = 'dept'
    search = 'JDS La'
    page = '1'
    results, pageInt, length, num_pages = matched_courses(search, order, page)
    result = ''
    for course in results:
        result += course.dept + course.catalog_number + ' '
    if result != 'COM202 REL330 ':
        testsfailed += "TEST 20 FAILED (search was: 'language identity power')\n"

    end = time.time()
    if testsfailed != "":
        sys.stdout.write(testsfailed)
    else:
        sys.stdout.write("All tests passed!\n")
    sys.stdout.write("Time elapsed: %.3f secs\n" % (end-begin))

test()