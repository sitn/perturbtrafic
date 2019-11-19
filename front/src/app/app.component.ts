import { Component, OnInit, HostListener, ViewChild, ElementRef } from '@angular/core';
import { Router } from '@angular/router';
import { ConfigService } from './services/config.service';
import { Subscription } from 'rxjs';
import { UserService } from './services/user.service';
import { IUser } from './models/IUser';
import { Align, Margin } from '@progress/kendo-angular-popup';
import { ApiService } from './services/api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {




  constructor() {

  }

  ngOnInit() {
  }


}
