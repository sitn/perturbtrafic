import { Component, OnInit } from '@angular/core';
import { UserService } from '../services/user.service';

@Component({
  selector: 'constante-main',
  templateUrl: './constante.component.html',
  styleUrls: ['./constante.component.less']
})
export class ConstanteComponent implements OnInit {

  constructor(public userService: UserService) { }

  ngOnInit() {
  }

  onTabSelect(e) {
    console.log(e);
  }

}
