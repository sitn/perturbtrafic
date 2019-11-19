import { Component, OnInit, HostListener } from '@angular/core';
import { ApiService } from '../services/api.service';
import { CookieService } from '../services/cookie.service';
import { UserService } from '../services/user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.less']
})
export class LoginComponent implements OnInit {

  user: string;
  password: string;
  showError: boolean;

  @HostListener('document:keyup', ['$event'])
  saveOnClickEnter(e) {
    if (e.keyCode === 13) {
      this.login();
    }
  }

  constructor(private apiService: ApiService, private cookieService: CookieService, private userService: UserService,
    private router: Router) { }

  ngOnInit() {
    this.showError = false;
  }

  login() {
    if (this.user && this.password) {
      this.showError = false;
      this.apiService.login(this.user, this.password).subscribe(user => {
        const error = (user as any).error;
        if (!error) {
          console.log(user);
          if (user.entites && user.entites.length > 0) {
            user.currentEntity = user.entites[0];
            this.cookieService.set('idEntity', user.entites[0].id.toString());
          } else {
            user.entites = [];
          }
          this.userService.getUserAutorisations().subscribe(autorisations => {
            this.userService.setAutorisations(autorisations);
          });
          this.userService.setUser(user);
          this.router.navigate(['/evenements']);
          this.cookieService.set('show-popup', 'yes');

        } else {
          this.showError = true;
        }
      });
    }
  }

}
