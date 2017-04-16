from . import model_cloudsql as sql

#returns a tuple of type results, pageInt, length, num_pages
def matched_courses(search, order, page):
    fields = None
    fields = search.split()

    #find correct page number
    pageInt = 0
    if page.isdigit():
        pageInt = int(page)
        start = (pageInt-1) * 12
        end = pageInt * 12
    else:
        pageInt = 1
        start = 0
        end = 12

    #length is all classes (only updated if search is not null)
    length = len(sql.Course.query.all())
    if length < end:
        end = length
    num_pages = length // 12 + (length % 12 > 0)

    results = []
    if fields is not None:
        baseQuery = sql.Course.query
        if order == "dept":
            baseQuery = baseQuery.order_by(sql.Course.dept)
        elif order == "rating":
            baseQuery = baseQuery.order_by(sql.Course.avg_rating.desc())
        for field in fields:
            #search by distribution
            if field.upper() in ["STN", "STL", "EC", "EM", "HA", "LA", "SA", "QR"]:
                baseQuery = baseQuery.filter(sql.Course.distribution == field)
            #pdf
            elif field.upper() == "PDF":
                baseQuery = baseQuery.filter(sql.Course.grade_options.contains("Only"))
            #catalog number
            elif len(field) == 3 and all(char.isdigit() for char in field):
                baseQuery = baseQuery.filter(sql.Course.catalog_number.contains(field) | sql.Course.crosslistings.contains(field))
            #including specials like 206a
            elif len(field) == 4 and all(char.isdigit() for char in field[0:3]) and field[3].isalpha():
                baseQuery = baseQuery.filter(sql.Course.catalog_number.contains(field) | sql.Course.crosslistings.contains(field))
            #department
            elif len(field) == 3 and all(char.isalpha() for char in field):
                baseQuery = baseQuery.filter(sql.Course.dept.contains(field) | sql.Course.crosslistings.contains(field))
            #else look in title, description, or professor
            #elif len(field) > 4:
            elif len(field) > 2:
                #"cos126" mix of letters and numbers assumes combined dept-catalognum
                if any(char.isdigit() for char in field) and any(char.isalpha() for char in field):
                    baseQuery = baseQuery.filter(sql.Course.dept.contains(field[0:3]) | sql.Course.crosslistings.contains(field[0:3]))
                    baseQuery = baseQuery.filter(sql.Course.catalog_number.contains(field[3:]) | sql.Course.crosslistings.contains(field[3:]))
                #else search in title or description
                else:
                    baseQuery = baseQuery.filter(sql.Course.title.contains(field) | sql.Course.description.contains(field))
                    #baseQuery = baseQuery.filter(sql.Course.instructors.any().contains(field))
                #professors
                #still have to figure this out
            #invalid searches 
            else:
                baseQuery = baseQuery.filter(False)
        length = len(baseQuery.all())
        if length < end:
            end = length
        results = baseQuery.order_by(sql.Course.catalog_number)[start:end]
        num_pages = length // 12 + (length % 12 > 0)

    return (results, pageInt, length, num_pages)
