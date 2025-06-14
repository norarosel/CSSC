
search_event:

        # User that searchs a resource in the search bar
        "user": user_id,
        # Day and time they search
        "date": datetime.now(),
        # Time they spend on the search, until they click on a resource
        "elapsed_time": elapsed_time,
        # For each resource appeared in the search
        "title": resource_title,
        # Video, podcast, etc. To keep track of what they search for.
        "type": resource_type,
        # We keep a score of how many words in its title match the input in the search bar
        "similarity score": score,
        # We keep count of how many resources match 100% of the words inputted in the search bar
        "complete matches": score_1_count


login_event:

        # User that logs in
        "user": user_id,
        # Day and time of the log in
        "date": datetime.now(),
        # Time they spend logged in
        "elapsed_time": elapsed_time,



resource_type_event:

        # User that choose a resource type (video, podcast...)
        "user": user_id,
        # Day and time they choose
        "date": datetime.now(),
        # Time they spend on resources of that type, until they choose another resource type
        "elapsed_time": elapsed_time,
        # Video, podcast...
        "type": resource_type,


see_more_event:

        # User that clicks the "see more" button on a certain resource
        "user": user_id,
        # Day and time they click
        "date": datetime.now(),
        # Time they spend reading that resource
        "elapsed_time": elapsed_time,
        # Title of the resource they view
        "title": resource_id,
        # Video, podcast, etc. To keep track of what type of resources they spend more time on.
        "type": resource_type,



rating_event:

        # User that rates a certain resource
        "user": user_id,
        # Day and time of the rating
        "date": datetime.now(),
        # Title of the resource they rate
        "title": resource_id,
        # Video, podcast...
        "type": resource_type,
        # The 1 to 5 score they rate a resource with
        "score": score


pagination_event:

        # User that is browsing through a page
        "user": user_id,
        # Day and time
        "date": datetime.now(),
        # Type of the resource in the page they are looking at
        "type": resource_type,
        # Page they are at
        "page": page_number,
        # Time they spend looking at that page, until they click on "previous page", "next page" or "see more".
        "elapsed time": elapsed_time
