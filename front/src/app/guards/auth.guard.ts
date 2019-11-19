import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot } from '@angular/router';

import { UserService } from '../services/user.service';
import { CookieService } from '../services/cookie.service';


@Injectable()
export class AuthGuard implements CanActivate {


    constructor(private router: Router, private userService: UserService, private cookieService: CookieService) {
    }

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {

        if (!this.userService.currentUser && !this.cookieService.get('auth_tkt')) {
            // not logged in so redirect to login page with the return url
            this.router.navigate(['/login']);
            return false;
        } else if (!this.userService.currentUser && this.cookieService.get('auth_tkt')) {
            // return true;
            return this.userService.isLoggedUser();
        } else {
            // logged in so return true
            return true;
        }
    }
}
