import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';

@Component({
    selector: 'liste-perturbation',
    templateUrl: './liste-perturbation.component.html',
    styleUrls: ['./liste-perturbation.component.less']
})
export class ListePerturbationComponent implements OnInit {


    resultats: any;

    constructor(private apiService: ApiService) {
        this.resultats = [];
    }

    ngOnInit() {

    }

    onSearchChange(resultats) {
        this.resultats = resultats;
    }

}
