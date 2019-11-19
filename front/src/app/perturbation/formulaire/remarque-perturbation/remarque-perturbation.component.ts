import { Component, OnInit, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { PerturbationFormService } from 'src/app/services/perturbation-form.service';

@Component({
  selector: 'remarque-perturbation',
  templateUrl: './remarque-perturbation.component.html',
  styleUrls: ['./remarque-perturbation.component.less']
})
export class RemarquePerturbationComponent implements OnInit {

  constructor(public perturbationFormService: PerturbationFormService) { }

  ngOnInit() {
  }

}
