import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot } from '@angular/router';

import { UserService } from '../services/user.service';
import { CookieService } from '../services/cookie.service';


@Injectable()
export class AddPerturbationGuard implements CanActivate {


    constructor(private router: Router, private userService: UserService) {
    }

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {

        if (this.userService.canAddPerturbation()) {
            return true;
        } else {
            this.router.navigate(['/Forbidden'], { skipLocationChange: true });
            return false;
        }
    }
}
