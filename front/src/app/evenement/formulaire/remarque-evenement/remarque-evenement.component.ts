import { Component, OnInit, OnChanges, ViewChild } from '@angular/core';
import { EvenementFormService } from 'src/app/services/evenement-form.service';
import { EditorComponent } from '@progress/kendo-angular-editor';

@Component({
  selector: 'remarque-evenement',
  templateUrl: './remarque-evenement.component.html',
  styleUrls: ['./remarque-evenement.component.less']
})
export class RemarqueEvenementComponent implements OnInit {

  constructor(public evenementFormService: EvenementFormService) { }

  ngOnInit() {
  }

}
