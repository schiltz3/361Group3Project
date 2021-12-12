from django.http.request import HttpRequest
from django.shortcuts import redirect


class RedirectUtil:
    def admin(request: HttpRequest, action: str, fallback):
        """
        Redirects all users that are not admins to their dashboards.
        @param request: the request that contains the logged in user
        @param action: a string that describes the admin action that the user anticipated to make
        @param fallback: the object to return if the logged in user is admin
        @pre: request must not be null
        @post: None
        @par: Side effect: Redirects you to login or dashboard depending on your group
        """
        if request.user.is_anonymous:
            return redirect("/", {"error": "User is not authorized to " + action})
        elif request.user.groups.filter(name="instructor").exists():
            return redirect(
                "/dashboard/instructor/",
                {"error": "Instructors are not authorized to " + action},
            )
        elif request.user.groups.filter(name="ta").exists():
            return redirect(
                "/dashboard/ta/", {"error": "TAs are not authorized to " + action}
            )
        else:
            return fallback

    def instructor(request: HttpRequest, action: str, fallback):
        """
        Redirects TAs to the TA dashboard, anounymous users to the login screen.
        @param request: the request that contains the logged in user
        @param action: a string that describes the instructor action that the user anticipated to make
        @param fallback: the object to return if the logged in user is an instructor or admin
        @pre: request must not be null
        @post: None
        @par: Side effect: Redirects TAs to the TA dashboard, and anonymous users to the login screen
        """
        if request.user.is_anonymous:
            return redirect("/", {"error": "User is not authorized to " + action})
        elif request.user.groups.filter(name="ta").exists():
            return redirect(
                "/dashboard/ta/", {"error": "TAs are not authorized to " + action}
            )
        else:
            return fallback

    def ta(request: HttpRequest, action: str, fallback):
        """
        Redirects anonymous users to the login screen.
        @param request: the request that contains the logged in user
        @param action: a string that describes the action that the user anticipated to make
        @param fallback: the object to return if the logged in as an autorized user
        @pre: request must not be null
        @post: None
        @par: Side effect: Redirects anonymous users to the login screen
        """
        if request.user.is_anonymous:
            return redirect("/", {"error": "User is not authorized to " + action})
        else:
            return fallback

