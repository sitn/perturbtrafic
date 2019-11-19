import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { IResultatEvenement } from 'src/app/models/evenement/IResultatEvenement';
import { CookieService } from 'src/app/services/cookie.service';

@Component({
    selector: 'liste-evenement',
    templateUrl: './liste-evenement.component.html',
    styleUrls: ['./liste-evenement.component.less']
})
export class ListeEvenementComponent implements OnInit {

    resultats: any;

    showPopup: boolean;

    constructor(private apiService: ApiService, private cookieService: CookieService, private ref: ChangeDetectorRef) {
        this.resultats = [];
        this.showPopup = false;
    }

    ngOnInit() {
        const cookie = this.cookieService.get('show-popup');
        console.log(cookie);
        if (cookie && cookie === 'yes') {
            this.showPopup = true;
            this.ref.detectChanges();
        }
    }

    onSearchChange(resultats: IResultatEvenement) {
        this.resultats = resultats;
        // this.apiService.searchEvenement().subscribe(data => this.resultats = data);
    }

}
