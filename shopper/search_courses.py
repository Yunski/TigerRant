from . import model_cloudsql as sql

#returns a tuple of type results, pageInt, length, num_pages
def SearchCourses(search, order, page):
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
            #department or catalog number
            elif len(field) == 3 or len(field) == 4:
                if not any(char.isdigit() for char in field):
                    baseQuery = baseQuery.filter(sql.Course.dept == field)
                else:
                    baseQuery = baseQuery.filter(sql.Course.catalog_number.contains(field))
            #else look in title, description, or professor
            elif len(field) > 4:
                #"cos126"
                if any(char.isdigit() for char in field) and (field.isupper() or field.islower()):
                    baseQuery = baseQuery.filter(sql.Course.dept == field[0:3])
                    baseQuery = baseQuery.filter(sql.Course.catalog_number.contains(field[3:]))
                #else search in title or description
                else:
                    baseQuery = baseQuery.filter(sql.Course.title.contains(field) | sql.Course.description.contains(field))
            #professors
            #still have to figure this out
        length = len(baseQuery.all())
        if length < end:
            end = length
        results = baseQuery.order_by(sql.Course.catalog_number)[start:end]
        num_pages = length // 12 + (length % 12 > 0)

    return (results, pageInt, length, num_pages)