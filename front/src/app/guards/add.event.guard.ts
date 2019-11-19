import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot } from '@angular/router';

import { UserService } from '../services/user.service';
import { CookieService } from '../services/cookie.service';


@Injectable()
export class AddEventGuard implements CanActivate {


    constructor(private router: Router, private userService: UserService) {
    }

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {

        if (this.userService.canAddEvent()) {
            // not logged in so redirect to login page with the return url
            // this.router.navigate(['/login']);
            return true;
        } else {
            // logged in so return true
            this.router.navigate(['/Forbidden'], { skipLocationChange: true });
            return false;
        }
    }
}
