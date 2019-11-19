import { Component, OnInit } from '@angular/core';
import { EvenementFormService } from 'src/app/services/evenement-form.service';

@Component({
  selector: 'attributs-manifestation-evenement',
  templateUrl: './attributs-manifestation-evenement.component.html',
  styleUrls: ['./attributs-manifestation-evenement.component.less']
})
export class AttributsManifestationEvenementComponent implements OnInit {

  constructor(public evenementFormService: EvenementFormService) { }

  ngOnInit() {
  }

}
